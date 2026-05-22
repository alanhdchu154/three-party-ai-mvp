"""Three-party abstraction tests."""

from __future__ import annotations

import json

from src import abstraction, coordinator, profile_store


def test_normalize_parent_text_into_party_profile():
    profile = abstraction.normalize_party_profile(
        "parent",
        "我怕我越問他越不跟我說話，但我又怕我什麼都不做。",
    )

    assert profile["party"] == "parent"
    assert profile["expressed_concerns"]
    assert profile["safe_summary_for_coordinator"]
    assert profile["what_not_to_share"] == []
    assert profile["confidence_level"] == "low"


def test_party_profile_view_hides_what_not_to_share_by_default():
    profile = abstraction.normalize_party_profile(
        "teacher",
        {
            "expressed_concerns": ["學生最近比較沉默"],
            "what_not_to_share": ["我其實怕家長投訴我偏心"],
            "safe_summary_for_coordinator": "老師觀察到參與下降。",
            "confidence_level": "medium",
        },
    )

    outside_view = abstraction.party_profile_view(profile, audience="parent_safe")
    internal_view = abstraction.party_profile_view(profile, audience="internal_reviewer")

    assert "what_not_to_share" not in outside_view
    assert "what_not_to_share" in internal_view


def test_extract_party_profile_does_not_store_raw_turns():
    raw = "我昨天晚上問了他三次成績，他直接把門關上，說再問就不讀了。"
    profile = abstraction.extract_party_profile(
        "parent",
        [
            {"role": "user", "content": raw},
            {"role": "assistant", "content": "先降低追問頻率。"},
        ],
    )
    rendered = json.dumps(profile, ensure_ascii=False)

    assert profile["party"] == "parent"
    assert profile["expressed_concerns"]
    assert "communication or trust concern" in profile["expressed_concerns"]
    assert raw not in rendered


def test_coordinator_accepts_party_profiles_and_sanitizes_adult_secrets(monkeypatch):
    def fake_complete_json(**kwargs):
        user_payload = kwargs["messages"][0]["content"]
        assert "家長 profile" in user_payload
        assert "老師 profile" in user_payload
        return {
            "whats_really_happening": "家長怕學校覺得自己失敗，老師怕家長投訴，所以都把焦點放在學業表現。",
            "who_knows_what": {
                "parent_sees": "家長看到學生沉默。",
                "teacher_sees": "老師看到參與下降。",
                "student_knows_alone": "學生知道自己正在失去信任。",
            },
            "privacy_kept": ["家長怕學校覺得自己失敗", "老師怕家長投訴"],
            "this_week": {
                "for_student": {"do": ["寫一句想被理解的事"], "dont": []},
                "for_parent": {"do": ["少問成績一次"], "dont": ["不要逼問"]},
                "for_teacher": {"do": ["給一個低壓選項"], "dont": []},
            },
            "watch_for": [],
            "needs_external_intervention": False,
        }

    monkeypatch.setattr(coordinator.llm, "complete_json", fake_complete_json)

    parent_profile = abstraction.normalize_party_profile(
        "parent",
        {
            "safe_summary_for_coordinator": "家長很焦慮但想幫忙。",
            "what_not_to_share": ["家長怕學校覺得自己失敗"],
        },
    )
    teacher_profile = abstraction.normalize_party_profile(
        "teacher",
        {
            "safe_summary_for_coordinator": "老師看到參與下降。",
            "what_not_to_share": ["老師怕家長投訴"],
        },
    )

    plan = coordinator.synthesize(
        {"do_not_share": [], "source_type": "synthetic"},
        "",
        "",
        parent_profile=parent_profile,
        teacher_profile=teacher_profile,
    )
    rendered = json.dumps(plan, ensure_ascii=False)

    assert "家長怕學校覺得自己失敗" not in rendered
    assert "老師怕家長投訴" not in rendered
    assert plan["_privacy_audit"]["needs_rewrite"] is True


def test_party_profile_store_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(profile_store, "PARTY_PROFILES_DIR", tmp_path / "party_profiles")
    profile = abstraction.extract_party_profile(
        "teacher",
        [{"role": "user", "content": "學生最近作業少交，我擔心是不是壓力太大。"}],
    )

    profile_store.save_party_profile("student/../a", "teacher", profile)
    loaded = profile_store.load_party_profile("student/../a", "teacher")

    assert loaded is not None
    assert loaded["student_id"] == "student____a"
    assert loaded["party"] == "teacher"
    assert loaded["expressed_concerns"]


def test_extract_party_profile_llm_sanitizes_risky_output(monkeypatch):
    def fake_complete_json(**kwargs):
        return {
            "party": "parent",
            "role_context": "家長",
            "expressed_concerns": ["Michael 看到信託文件後壓力很大"],
            "underlying_needs": ["需要支持"],
            "fears_or_constraints": [],
            "communication_style": "焦慮",
            "blind_spots": [],
            "what_they_can_offer": ["陪伴"],
            "safe_summary_for_coordinator": "Michael 看到信託文件",
            "what_not_to_share": [],
            "confidence_level": "medium",
        }

    monkeypatch.setattr(abstraction.llm, "complete_json", fake_complete_json)

    profile = abstraction.extract_party_profile_llm(
        "parent",
        [{"role": "user", "content": "我擔心孩子。"}],
        protected_terms=["Michael", "信託文件"],
    )
    rendered = json.dumps(profile, ensure_ascii=False)

    assert "Michael" not in rendered
    assert "信託文件" not in rendered
    assert profile["_privacy_audit"]["needs_rewrite"] is True
