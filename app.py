"""Streamlit 入口——學生 AI + Coordinator + Triage 的視覺化介面。

執行：streamlit run app.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st

from src import (
    abstraction,
    coordinator,
    llm,
    party_agent,
    profile_store,
    source_types,
    student_agent,
    triage,
)

DATA_DIR = Path(__file__).resolve().parent / "data"
DUMMY_INPUTS_PATH = DATA_DIR / "dummy_inputs.json"


# ----------------------------------------------------------------------------
# 通用工具
# ----------------------------------------------------------------------------

def _check_api_key() -> bool:
    """檢查當前 LLM_MODEL 對應的 API key，沒設就在畫面上提示。"""
    import os

    from src.llm import DEFAULT_MODEL, _PROVIDER_KEY_MAP, _provider_of

    provider = _provider_of(DEFAULT_MODEL)
    if provider == "ollama":
        return True  # Ollama 本地不需要 key

    key_name = _PROVIDER_KEY_MAP.get(provider)
    if not key_name:
        # 未知 provider，讓 LiteLLM 自己回錯誤
        return True

    val = os.getenv(key_name, "")
    if not val or val.startswith("your-") or val.startswith("sk-ant-xxxxxxxx"):
        st.error(
            f"⚠️ 還沒設定 `{key_name}`（當前 `LLM_MODEL={DEFAULT_MODEL}` 需要這個）。\n\n"
            "請在專案根目錄：\n\n"
            "```\ncp .env.example .env\n```\n"
            f"然後編輯 `.env` 把 `{key_name}` 填進去，再重新啟動 `streamlit run app.py`。\n\n"
            "想換 provider？把 `.env` 裡的 `LLM_MODEL` 改成別的（例如 `ollama/llama3.2` 不用 key）。"
        )
        return False
    return True


def _load_dummy_scenarios() -> list[dict]:
    if not DUMMY_INPUTS_PATH.exists():
        return []
    try:
        data = json.loads(DUMMY_INPUTS_PATH.read_text(encoding="utf-8"))
        return data.get("scenarios", [])
    except json.JSONDecodeError:
        return []


def _init_session_state():
    if "current_student" not in st.session_state:
        st.session_state.current_student = None
    if "current_session_kind" not in st.session_state:
        st.session_state.current_session_kind = None
    if "history" not in st.session_state:
        # 對話 history 只存在 session 裡——刻意不寫檔（隱私牆）
        st.session_state.history = []
    if "party_histories" not in st.session_state:
        st.session_state.party_histories = {
            "student": st.session_state.history,
            "parent": [],
            "teacher": [],
        }
    if "last_profile" not in st.session_state:
        st.session_state.last_profile = None
    if "last_party_profiles" not in st.session_state:
        st.session_state.last_party_profiles = {"parent": None, "teacher": None}


def _raw_conversation_view_enabled() -> bool:
    """Dev-only switch for viewing raw conversations in the app."""
    return _app_mode() == "dev" and (
        os.getenv("SHOW_RAW_CONVERSATIONS", "").strip().lower()
        in {"1", "true", "yes", "on"}
        or os.getenv("UMI_DEV_MODE", "").strip().lower()
        in {"1", "true", "yes", "on"}
    )


def _app_mode() -> str:
    """Explicit UI mode: dev, demo, or pilot. Defaults to demo."""
    if os.getenv("UMI_DEV_MODE", "").strip().lower() in {"1", "true", "yes", "on"}:
        return "dev"
    mode = os.getenv("APP_MODE", "demo").strip().lower()
    return mode if mode in {"dev", "demo", "pilot"} else "demo"


def _is_dev_mode() -> bool:
    return _app_mode() == "dev"


def _source_label(source_type: str | None = None) -> str:
    source = source_types.normalize_source_type(source_type)
    if source_types.is_pilot_source(source):
        return "Pilot anonymized data"
    return "Synthetic benchmark data"


def _analysis_protected_terms(data: dict, analysis: dict) -> list[str]:
    terms: list[str] = []
    terms.extend(analysis.get("privacy_kept") or [])
    profile = data.get("student_profile") or {}
    terms.extend(profile.get("do_not_share") or [])
    terms.extend([data.get("student", ""), data.get("persona_id", "")])
    return [term for term in terms if term]


def _list_demo_live_profiles() -> dict[str, dict]:
    """Return Saga A analysis profiles that can seed a live session."""
    if not REPORTS_DIR.exists():
        return {}
    profiles: dict[str, dict] = {}
    for path in sorted(REPORTS_DIR.glob("*_analysis.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        student_id = str(data.get("student") or path.stem.replace("_analysis", ""))
        profile = data.get("student_profile") or {}
        if not student_id or not profile:
            continue
        profiles[student_id] = {
            **profile,
            "student_id": student_id,
            "character_id": data.get("persona_id") or student_id,
            "source_type": source_types.normalize_source_type(data.get("source_type")),
            "_demo_profile_source": str(path.relative_to(DATA_DIR.parent)),
        }
    return profiles


def _current_profile() -> dict | None:
    if not st.session_state.current_student:
        return None
    return st.session_state.last_profile or profile_store.load_profile(
        st.session_state.current_student
    )


def _current_party_profile(party: str) -> dict | None:
    if not st.session_state.current_student:
        return None
    cached = st.session_state.last_party_profiles.get(party)
    return cached or profile_store.load_party_profile(
        st.session_state.current_student, party
    )


def _reset_live_histories() -> None:
    st.session_state.history = []
    st.session_state.party_histories = {"student": [], "parent": [], "teacher": []}


def _set_active_context(student_id: str, kind: str, demo_profiles: dict[str, dict]) -> None:
    st.session_state.current_student = student_id
    st.session_state.current_session_kind = kind
    _reset_live_histories()
    if kind == "live":
        st.session_state.last_profile = profile_store.load_profile(student_id)
    else:
        st.session_state.last_profile = demo_profiles.get(student_id)
    st.session_state.last_party_profiles = {
        "parent": profile_store.load_party_profile(student_id, "parent"),
        "teacher": profile_store.load_party_profile(student_id, "teacher"),
    }


# ----------------------------------------------------------------------------
# Active context selector
# ----------------------------------------------------------------------------

def render_active_context_picker():
    st.markdown("### 🎛 Active Case Workspace")
    st.caption(
        "先在這裡選或建立一個 active case。下面的學生 / 家長 / 老師 live chat、"
        "Profile、Coordinator、Triage 都會跟著同一個 case。"
    )
    existing = profile_store.list_profiles()
    demo_profiles = _list_demo_live_profiles()

    options = ["new"]
    options.extend(f"live:{student_id}" for student_id in existing)
    options.extend(
        f"demo:{student_id}"
        for student_id in demo_profiles
        if student_id not in existing
    )
    options.extend(
        f"demo:{student_id}"
        for student_id in demo_profiles
        if student_id in existing
    )

    def _label(option: str) -> str:
        if option == "new":
            return "（新建 live session）"
        kind, student_id = option.split(":", 1)
        if kind == "live":
            return f"Live profile · {student_id}"
        return f"Saga A demo profile · {student_id}"

    current_option = "new"
    if st.session_state.current_student:
        preferred = (
            f"{st.session_state.current_session_kind}:"
            f"{st.session_state.current_student}"
        )
        if preferred in options:
            current_option = preferred
        elif f"live:{st.session_state.current_student}" in options:
            current_option = f"live:{st.session_state.current_student}"
        elif f"demo:{st.session_state.current_student}" in options:
            current_option = f"demo:{st.session_state.current_student}"

    choice = st.selectbox(
        "選 active case",
        options=options,
        index=options.index(current_option) if current_option in options else 0,
        format_func=_label,
        key="active_context_choice",
        help=(
            "Live profile 是你用聊天產生並存下來的 profile；"
            "Saga A demo profile 會用既有歷史分析資料先幫你 seed 一個 session。"
        ),
    )

    if choice == "new":
        cols = st.columns([3, 1])
        new_id = cols[0].text_input("學生 ID（例：alice_g9）", key="new_student_id")
        if cols[1].button("建立", use_container_width=True) and new_id.strip():
            _set_active_context(new_id.strip(), "live", demo_profiles)
            st.rerun()
    else:
        kind, student_id = choice.split(":", 1)
        if (
            student_id != st.session_state.current_student
            or kind != st.session_state.current_session_kind
        ):
            _set_active_context(student_id, kind, demo_profiles)
            st.rerun()

    if st.session_state.current_student:
        c1, c2, c3 = st.columns([2, 2, 1])
        c1.metric("Active case", st.session_state.current_student)
        c2.metric("Mode", st.session_state.current_session_kind or "new")
        if c3.button("清空 live 對話", use_container_width=True):
            _reset_live_histories()
            st.rerun()
        if st.session_state.current_session_kind == "demo":
            st.info(
                "目前使用 Saga A demo profile。右邊 Profile / Coordinator / Triage "
                "會跟著這個案例；聊天會知道這個抽象 profile，但新的對話只存在記憶體，不會改動歷史資料。"
            )
        elif st.session_state.current_session_kind == "live":
            st.info(
                "目前使用 live profile。新聊天只存在目前 Streamlit session；"
                "只有按「更新 Profile」才會把抽象 profile 寫入磁碟。"
            )
        if st.button(
            "⚠️ 刪除這個學生 profile",
            disabled=st.session_state.current_session_kind == "demo",
        ):
            profile_store.delete_profile(st.session_state.current_student)
            st.session_state.current_student = None
            st.session_state.current_session_kind = None
            _reset_live_histories()
            st.session_state.last_profile = None
            st.session_state.last_party_profiles = {"parent": None, "teacher": None}
            st.rerun()


# ----------------------------------------------------------------------------
# Sidebar：狀態摘要
# ----------------------------------------------------------------------------

def render_sidebar():
    st.sidebar.title("三方 AI · MVP")
    st.sidebar.caption("AI Student Success & Support Layer")
    st.sidebar.caption(f"UI mode: `{_app_mode()}`")

    st.sidebar.divider()
    st.sidebar.markdown("### Current Status")
    if st.session_state.current_student:
        st.sidebar.markdown(f"**Active case:** `{st.session_state.current_student}`")
        st.sidebar.caption(f"Session kind: `{st.session_state.current_session_kind}`")
        st.sidebar.caption(
            "主要操作已移到中間的 `💬 三方 Live` tab；左欄只保留狀態，避免 selector 跟主面板打架。"
        )
    else:
        st.sidebar.info("到 `💬 三方 Live` tab 選一個 demo case 或建立 live session。")

    st.sidebar.divider()
    st.sidebar.caption("⚙️ 模型：" + llm.DEFAULT_MODEL)


# ----------------------------------------------------------------------------
# Tab 1：三方 live workspace
# ----------------------------------------------------------------------------

def render_chat_tab():
    st.subheader("💬 三方 Live Workspace")
    render_active_context_picker()
    st.divider()

    if not st.session_state.current_student:
        st.info("先在上方選一個 Saga A demo case，或建立新的 live session。")
        return

    st.caption(
        "這裡是 product loop 的入口：三方各自跟自己的 AI 說話，"
        "再各自抽象化成 profile。Raw turns 只留在目前 session，不寫入磁碟。"
    )

    party_tabs = st.tabs(["👤 學生 AI", "👨‍👩‍👧 家長 AI", "👨‍🏫 老師 AI"])
    with party_tabs[0]:
        _render_party_live_chat("student")
    with party_tabs[1]:
        _render_party_live_chat("parent")
    with party_tabs[2]:
        _render_party_live_chat("teacher")


def _render_party_live_chat(party: str) -> None:
    labels = {
        "student": ("學生", "以學生身份輸入訊息……"),
        "parent": ("家長", "以家長身份輸入訊息……"),
        "teacher": ("老師", "以老師身份輸入訊息……"),
    }
    label, placeholder = labels[party]
    student_profile = _current_profile()
    party_profile = _current_party_profile(party) if party in {"parent", "teacher"} else None

    if party == "student":
        st.markdown("#### 👤 學生 ↔ 學生 AI")
        st.info(
            "學生 AI 只使用抽象 context 做 continuity；更新 Profile 時只保存抽象化學生 profile。"
        )
    else:
        st.markdown(f"#### {label} ↔ {label} AI")
        st.info(
            f"{label} AI 會幫{label}整理擔心與可行動支持。更新 Profile 時只保存抽象化 party profile，"
            "不保存 raw turns，也不揭露學生秘密。"
        )

    history = st.session_state.party_histories.setdefault(party, [])
    if party == "student":
        st.session_state.history = history

    for turn in history:
        role = turn["role"]
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(turn["content"])

    user_msg = st.chat_input(placeholder, key=f"{party}_chat_input")
    if user_msg:
        history.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            with st.spinner("AI 在想……"):
                try:
                    if party == "student":
                        reply = student_agent.chat(
                            user_msg,
                            history=history[:-1],
                            context_profile=student_profile,
                        )
                    else:
                        reply = party_agent.chat(
                            party,
                            user_msg,
                            history=history[:-1],
                            party_profile=party_profile,
                            student_profile=student_profile,
                        )
                except llm.LLMConfigError as e:
                    st.error(str(e))
                    if llm.DEFAULT_MODEL.startswith("ollama/"):
                        st.caption(
                            "Ollama 第一次載入模型可能需要一點時間。等模型載好後，"
                            "同一句話再送一次通常就會正常。"
                        )
                    return
                except Exception as e:  # noqa: BLE001
                    st.error(f"出錯了：{e}")
                    return
            st.markdown(reply)
        history.append({"role": "assistant", "content": reply})
        if party == "student":
            st.session_state.history = history

    st.divider()
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button(f"📝 更新 {label} Profile", disabled=not history, key=f"update_{party}_profile"):
            with st.spinner("抽象化中……"):
                try:
                    if party == "student":
                        profile = abstraction.extract_profile(history)
                        profile_store.save_profile(
                            st.session_state.current_student, profile
                        )
                        st.session_state.last_profile = profile
                    else:
                        profile = abstraction.extract_party_profile_with_fallback(
                            party,
                            history,
                            source_type="pilot" if _app_mode() == "pilot" else "synthetic",
                            protected_terms=(student_profile or {}).get("do_not_share", []),
                            use_llm=not llm.DEFAULT_MODEL.startswith("ollama/"),
                        )
                        profile_store.save_party_profile(
                            st.session_state.current_student, party, profile
                        )
                        st.session_state.last_party_profiles[party] = profile
                    st.success(f"{label} Profile 已更新。切到「Profile」分頁看結果。")
                except llm.LLMConfigError as e:
                    st.error(str(e))
                except Exception as e:  # noqa: BLE001
                    st.error(f"抽象化失敗：{e}")
    with col2:
        if party == "student":
            st.caption("學生 profile 使用 LLM abstraction + Privacy Wall；raw turns 不寫入磁碟。")
        else:
            st.caption(
                f"{label} profile 目前使用 deterministic privacy-safe abstraction baseline；"
                "保存 broad categories，不保存原話。"
            )


# ----------------------------------------------------------------------------
# Tab 2：Profile
# ----------------------------------------------------------------------------

def render_profile_tab():
    st.subheader("🔐 三方 Profiles（抽象化後）")
    if not st.session_state.current_student:
        st.info("先到「💬 三方 Live」選一個 active case。")
        return

    profile = _current_profile()
    parent_profile = _current_party_profile("parent")
    teacher_profile = _current_party_profile("teacher")

    # 隱私牆健檢
    if profile and st.session_state.party_histories.get("student"):
        leaked = abstraction.validate_no_raw_quotes(profile, st.session_state.history)
        if leaked:
            st.error(
                f"⚠️ 隱私牆檢測到 {len(leaked)} 句原話可能被洩漏到 profile："
                f"{leaked[:3]}"
            )
        else:
            st.success("✅ 學生 profile 隱私牆檢測通過：不含學生對話原話。")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 👤 Student Profile")
        if profile:
            st.json(profile)
        else:
            st.warning("還沒有學生 profile。到「💬 三方 Live」的學生 AI 按更新。")
    with c2:
        st.markdown("#### 👨‍👩‍👧 Parent Profile")
        if parent_profile:
            st.json(abstraction.party_profile_view(parent_profile, audience="internal_reviewer"))
        else:
            st.warning("還沒有家長 profile。到「💬 三方 Live」的家長 AI 按更新。")
    with c3:
        st.markdown("#### 👨‍🏫 Teacher Profile")
        if teacher_profile:
            st.json(abstraction.party_profile_view(teacher_profile, audience="internal_reviewer"))
        else:
            st.warning("還沒有老師 profile。到「💬 三方 Live」的老師 AI 按更新。")


# ----------------------------------------------------------------------------
# Tab 3：Coordinator
# ----------------------------------------------------------------------------

def render_coordinator_tab():
    st.subheader("🤝 Coordinator：三方協調")
    if not st.session_state.current_student:
        st.info("先到「💬 三方 Live」選一個 active case。")
        return

    profile = _current_profile()
    if not profile:
        st.warning("沒有學生 profile 可用。先到「💬 三方 Live」的學生 AI 產生一個。")
        return

    saved_parent_profile = _current_party_profile("parent")
    saved_teacher_profile = _current_party_profile("teacher")
    scenarios = _load_dummy_scenarios()
    labels = ["（使用已保存 parent/teacher profiles）", "（自訂 raw inputs）"] + [
        s["label"] for s in scenarios
    ]
    default_index = 0 if saved_parent_profile or saved_teacher_profile else 1
    pick = st.selectbox("選 coordinator 輸入來源", labels, index=default_index)

    parent_profile = saved_parent_profile
    teacher_profile = saved_teacher_profile
    parent_input: str | dict = parent_profile or ""
    teacher_input: str | dict = teacher_profile or ""

    if pick == "（使用已保存 parent/teacher profiles）":
        if not parent_profile and not teacher_profile:
            st.warning("目前還沒有已保存的 parent/teacher profile。可以先用自訂 raw inputs，或去三方 Live 更新。")
        with st.expander("查看 coordinator 會使用的三方抽象 profile"):
            st.markdown("**Student profile**")
            st.json(profile)
            st.markdown("**Parent profile**")
            st.json(parent_profile or {})
            st.markdown("**Teacher profile**")
            st.json(teacher_profile or {})
    elif pick == "（自訂 raw inputs）":
        parent_input = st.text_area("家長輸入", height=120)
        teacher_input = st.text_area("老師輸入", height=120)
        parent_profile = None
        teacher_profile = None
    else:
        chosen = scenarios[labels.index(pick) - 2]
        parent_input = st.text_area("家長輸入", value=chosen["parent_input"], height=120)
        teacher_input = st.text_area("老師輸入", value=chosen["teacher_input"], height=120)
        parent_profile = None
        teacher_profile = None

    if st.button("產出協調方案"):
        with st.spinner("Coordinator 正在合成……"):
            try:
                plan = coordinator.synthesize(
                    profile,
                    parent_input,
                    teacher_input,
                    parent_profile=parent_profile,
                    teacher_profile=teacher_profile,
                )
            except llm.LLMConfigError as e:
                st.error(str(e))
                return
            except Exception as e:  # noqa: BLE001
                st.error(f"出錯了：{e}")
                return

        st.markdown("### 📋 整體方案")
        st.write(plan.get("overall_plan", ""))

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**→ 給學生**")
            st.info(plan.get("message_to_student", ""))
        with c2:
            st.markdown("**→ 給家長**")
            st.info(plan.get("message_to_parent", ""))
        with c3:
            st.markdown("**→ 給老師**")
            st.info(plan.get("message_to_teacher", ""))

        watch = plan.get("watch_for", [])
        if watch:
            st.markdown("### 👀 後續留意")
            for w in watch:
                st.markdown(f"- {w}")


# ----------------------------------------------------------------------------
# Tab：三方分析報告（讀 data/analysis_reports/*.json 顯示）
# ----------------------------------------------------------------------------

REPORTS_DIR = DATA_DIR / "analysis_reports"
DIMENSION_DIR = DATA_DIR / "dimension_scores"

DIM_LABELS = {
    "emotional_safety":   "🫀 情緒安全",
    "academic_load":      "📚 學業負擔",
    "family_dynamics":    "🏠 家庭關係",
    "social_development": "👥 社交發展",
    "identity":           "🪞 身分認同",
    "financial_pressure": "💰 經濟壓力",
    "future_planning":    "🧭 未來規劃",
}


def _list_analysis_reports() -> list[tuple[str, Path]]:
    """回傳 [(student_label, path), ...]。"""
    if not REPORTS_DIR.exists():
        return []
    out = []
    for f in sorted(REPORTS_DIR.glob("*_analysis.json")):
        name = f.stem.replace("_analysis", "")
        out.append((name, f))
    return out


def _load_dimension_scores(student_short: str) -> dict | None:
    """讀 data/dimension_scores/{student}.json。"""
    if not DIMENSION_DIR.exists():
        return None
    path = DIMENSION_DIR / f"{student_short}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _render_dimension_scorecard(scores: dict) -> None:
    """畫七維度 scorecard。"""
    cumulative = scores.get("cumulative_strain", 0)
    highest = scores.get("highest_concern_dimension", "")
    trend = scores.get("trend_notes", "")

    top_cols = st.columns(3)
    top_cols[0].metric("Cumulative Strain", f"{cumulative}/21")
    top_cols[1].metric("最高關注維度", DIM_LABELS.get(highest, highest))
    top_cols[2].metric("已評估對話", scores.get("n_conversations_evaluated", 0))

    if trend:
        st.caption(f"📈 趨勢：{trend}")

    st.markdown("#### 七維度評分")

    dimensions = scores.get("dimensions", {})
    for dim_key, label in DIM_LABELS.items():
        dim_data = dimensions.get(dim_key, {})
        level = dim_data.get("level", 0)
        signals = dim_data.get("signals_observed", [])
        reasoning = dim_data.get("reasoning", "")

        # 顏色 by level
        color = ["🟢", "🟡", "🟠", "🔴"][min(level, 3)]
        bar = "█" * level + "░" * (3 - level)

        with st.container(border=True):
            cols = st.columns([3, 1, 6])
            cols[0].markdown(f"**{label}**")
            cols[1].markdown(f"{color} **{level}/3**")
            cols[2].markdown(f"`{bar}` _{reasoning}_")
            if signals:
                with st.expander(f"觀察到的訊號（{len(signals)}）"):
                    for s in signals:
                        st.markdown(f"- {s}")


def render_analysis_tab():
    st.subheader("📋 三方分析報告")
    st.caption("由 coordinator 從學生 / 家長 / 老師三方 AI 對話合成。"
               "原話不會跨方流動 — 隱私牆已執行。")

    with st.expander("🤔 這個 UI 到底可以做什麼？（第一次來看這個）"):
        st.markdown("""
**這個產品的核心循環：**

1. 學生、家長、老師各自跟自己的 AI 對話（在 `📚 對話庫` tab 可以看到所有對話原話）
2. AI 把每段對話**抽象化**成 profile（隱私牆：絕對不含原話）
3. **Coordinator** 看三方的 profile，找出：
   - 真正在發生的事（水面下的）
   - 三方各自的盲點
   - 給三方各自具體的 do/dont 建議
4. **這個 tab** 就是把上面 step 3 的結果用卡片呈現給使用者看

**每個 tab 用途：**
- 📋 **三方分析**（這個）— 主要 value view，看 coordinator 的合成結果
- 📚 **對話庫** — 看每段原始對話（dev / Alan 的視角，使用者看不到）
- 📊 **歷史資訊** — 每個 persona 的對話統計與覆蓋
- 💬 **三方 Live** — active case 工作區；學生、家長、老師各自跟自己的 AI 對話並更新 profile
- 🔐 **Profile** — 把聊天抽象化成 profile，看隱私牆有沒有 work
- 🤝 **Coordinator (live)** — live LLM 跑 coordinator（vs 預先 hand-craft 的）
- 🚦 **Triage** — 升級判斷

**Active case 選擇器已移到 `💬 三方 Live` tab**。
左邊 sidebar 現在只顯示狀態，不再控制主要工作區，避免跟這個 tab 的報告選擇器混淆。
        """)

    reports = _list_analysis_reports()
    if not reports:
        st.warning(
            "還沒有任何分析報告。先跑：\n\n"
            "```\npython scripts/run_analysis.py --student michael\n```\n\n"
            "或檢視 `data/analysis_reports/` 目錄。"
        )
        return

    labels = [name for name, _ in reports]
    pick = st.selectbox("選一個學生看報告", labels)
    chosen_path = next(p for name, p in reports if name == pick)

    try:
        data = json.loads(chosen_path.read_text(encoding="utf-8"))
    except Exception as e:
        st.error(f"讀檔失敗：{e}")
        return

    analysis = data.get("analysis", {})
    display_analysis = (
        analysis if _is_dev_mode() else
        abstraction.sanitize_for_privacy(
            analysis,
            protected_terms=_analysis_protected_terms(data, analysis),
        )
    )
    source_label = _source_label(data.get("source_type"))
    meta_cols = st.columns(3)
    meta_cols[0].metric("學生", data.get("student", pick))
    meta_cols[1].metric("資料來源對話數", data.get("n_conversations", 0))
    meta_cols[1].caption(source_label)
    if display_analysis.get("needs_external_intervention"):
        meta_cols[2].error("🚨 需要外部專業介入")
    else:
        meta_cols[2].success("✅ 系統可處理範圍")
    st.caption(f"資料模式：{source_label} · UI mode: `{_app_mode()}`")

    # 📐 七維度評分（如果有）
    dim_scores = _load_dimension_scores(pick)
    if dim_scores:
        st.divider()
        st.markdown("### 📐 七維度評分")
        _render_dimension_scorecard(dim_scores)
    else:
        st.caption(f"💡 還沒有七維度評分。跑：`python scripts/evaluate_dimensions.py --student {pick}`")

    st.divider()

    # 🎯 真正在發生的事
    st.markdown("### 🎯 真正在發生的事")
    whats = display_analysis.get("whats_really_happening", "")
    if whats:
        st.info(whats)
    else:
        st.caption("（沒有 whats_really_happening 欄位）")

    # 🔀 三方各自知道什麼
    st.markdown("### 🔀 三方各自知道什麼")
    wkw = display_analysis.get("who_knows_what", {})
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**👨‍👩‍👧 家長看到**")
        st.write(wkw.get("parent_sees", "（無）"))
    with c2:
        st.markdown("**👨‍🏫 老師看到**")
        st.write(wkw.get("teacher_sees", "（無）"))
    with c3:
        st.markdown("**🤐 學生獨自知道**")
        st.write(wkw.get("student_knows_alone", "（無）"))

    # 🔒 系統保護的事項（subtle expander）
    privacy_kept = display_analysis.get("privacy_kept", [])
    if privacy_kept:
        if _is_dev_mode():
            with st.expander(f"🔒 系統保護的事項（{len(privacy_kept)} 項不會傳給家長 / 老師）"):
                for p in privacy_kept:
                    st.markdown(f"- {p}")
        else:
            st.caption(f"🔒 系統已保護 {len(privacy_kept)} 類敏感事項；demo/pilot UI 不顯示具體內容。")

    st.divider()

    # 💬 這禮拜該做的事
    st.markdown("### 💬 這禮拜該做的事")
    week = display_analysis.get("this_week", {})
    cc1, cc2, cc3 = st.columns(3)
    party_meta = [
        ("for_student", "👤 學生本人", cc1),
        ("for_parent", "👨‍👩‍👧 家長", cc2),
        ("for_teacher", "👨‍🏫 老師", cc3),
    ]
    for key, label, col in party_meta:
        with col:
            st.markdown(f"**{label}**")
            actions = week.get(key, {})
            for item in actions.get("do", []):
                st.success(f"✅ {item}")
            for item in actions.get("dont", []):
                st.error(f"❌ {item}")
            if not actions.get("do") and not actions.get("dont"):
                st.caption("（無建議）")

    # 👀 後續留意
    watch = display_analysis.get("watch_for", [])
    if watch:
        st.divider()
        st.markdown("### 👀 下週要 notice 的訊號")
        for w in watch:
            st.markdown(f"- {w}")

    if _is_dev_mode():
        # 原始資料只給 dev mode。
        with st.expander("🔧 看原始 JSON / profile"):
            sub_tabs = st.tabs(["分析輸出", "學生 profile", "家長輸入", "老師輸入"])
            with sub_tabs[0]:
                st.json(analysis)
            with sub_tabs[1]:
                st.json(data.get("student_profile", {}))
            with sub_tabs[2]:
                st.write(data.get("parent_input", ""))
            with sub_tabs[3]:
                st.write(data.get("teacher_input", ""))


# ----------------------------------------------------------------------------
# Tab：對話庫 + 歷史資訊
# ----------------------------------------------------------------------------

GEN_DIR = DATA_DIR / "generated_conversations"
SD_PATH = DATA_DIR / "synthetic_dataset.json"


def _load_all_conversations() -> list[dict]:
    """從兩個來源 load 所有對話。每個 dict 加 _source 標記。"""
    convs = []
    # synthetic_dataset.json 的 hand-crafted
    if SD_PATH.exists():
        sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
        for c in sd.get("conversations", []):
            c["_source"] = "synthetic_dataset.json"
            convs.append(c)
    # generated_conversations/
    if GEN_DIR.exists():
        for f in sorted(GEN_DIR.glob("sim_*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            data["_source"] = f"generated/{f.name}"
            convs.append(data)
    return convs


def _load_personas() -> dict[str, dict]:
    if not SD_PATH.exists():
        return {}
    sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
    return {p["id"]: p for p in sd.get("personas", [])}


def render_corpus_tab():
    st.subheader("📚 對話庫")
    if not _raw_conversation_view_enabled():
        st.warning(
            "Raw conversation view 目前關閉。這裡會顯示學生 / 家長 / 老師的原始對話，"
            "只適合 Alan 或開發者在本機 debug 時使用。"
        )
        st.caption(
            "需要查看時，重啟 app 前設定 `SHOW_RAW_CONVERSATIONS=1` "
            "或 `UMI_DEV_MODE=1`。Pilot / demo 給外部看時請保持關閉。"
        )
        return

    st.caption("所有學生 / 家長 / 老師跟自己 AI 的對話。原話只在此 tab 顯示給 dev / Alan 看 — 不會經由 coordinator 流到其他方。")

    convs = _load_all_conversations()
    personas = _load_personas()

    if not convs:
        st.warning("還沒有對話。先跑 simulation script 或 hand-craft。")
        return

    # 統計
    st.markdown(f"**總對話數：{len(convs)}**　|　持有 personas：{len({c.get('persona_id') for c in convs})}")

    # 按 persona 分組
    by_persona: dict[str, list[dict]] = {}
    for c in convs:
        pid = c.get("persona_id", "unknown")
        by_persona.setdefault(pid, []).append(c)

    # Sidebar style picker
    persona_options = sorted(by_persona.keys())
    persona_labels = [
        f"{pid} — {personas.get(pid, {}).get('name_or_pseudonym', '?')}（{len(by_persona[pid])} 段）"
        for pid in persona_options
    ]
    pick_idx = st.selectbox("選一個 persona", range(len(persona_options)),
                            format_func=lambda i: persona_labels[i])
    chosen_pid = persona_options[pick_idx]

    # Persona info card
    p = personas.get(chosen_pid)
    if p:
        with st.expander("ℹ️ Persona 背景"):
            st.markdown(f"**角色**：{p.get('role', '?')} — {p.get('grade_or_position', '')}")
            st.markdown(f"**Background**：{p.get('background', '')}")
            st.markdown(f"**Secret truth**：{p.get('secret_truth', '')}")
            tags = p.get("metadata", {}).get("tags", [])
            if tags:
                st.markdown("**Tags**：" + " · ".join(f"`{t}`" for t in tags))

    # List conversations for this persona — 按 occurred_at 排序（最新在上）
    persona_convs = by_persona[chosen_pid]
    persona_convs_sorted = sorted(
        persona_convs,
        key=lambda c: c.get("occurred_at", "0000"),
        reverse=True,
    )
    st.markdown(f"### 此 persona 的 {len(persona_convs_sorted)} 段對話（按發生時間，最新在上）")

    for i, conv in enumerate(persona_convs_sorted, 1):
        conv_id = conv.get("id", f"#{i}")
        n_turns = len(conv.get("turns", []))
        scen = conv.get("scenario_seed_id") or conv.get("scenario_type", "")
        source = conv.get("_source", "")
        occurred = conv.get("occurred_at", "?")
        # 格式化時間更人類可讀
        time_label = occurred[:16].replace("T", " ") if occurred and occurred != "?" else "未標記"

        with st.expander(f"🕐 {time_label} · {conv_id} · {n_turns} turns · scenario: {scen}"):
            cols = st.columns([1, 1])
            cols[0].caption(f"📅 in-saga 發生時間：{occurred}")
            cols[1].caption(f"💾 generated_at: {conv.get('generated_at', '?')} · {source}")

            scen_seed = conv.get("scenario_seed")
            if scen_seed:
                st.caption(f"📌 Scenario seed: {scen_seed}")

            risk_flags = conv.get("expected_risk_flags", [])
            if risk_flags:
                st.caption("🚩 expected_risk_flags: " + ", ".join(risk_flags))

            for turn in conv.get("turns", []):
                role = turn.get("role", "?")
                content = turn.get("content", "")
                if role == "user":
                    st.markdown(f"**🗣️ {p.get('name_or_pseudonym', 'User') if p else 'User'}：** {content}")
                elif role == "assistant":
                    st.markdown(f"**🤖 AI：** {content}")
                else:
                    st.caption(f"_{role}_: {content}")


def render_history_tab():
    st.subheader("📊 歷史資訊")
    st.caption("每個 persona 的對話統計、scenario 覆蓋、資料來源、產生時間。")

    convs = _load_all_conversations()
    personas = _load_personas()
    if not convs:
        st.warning("沒有對話資料。")
        return

    # Aggregate per persona
    rows = []
    for pid, p in personas.items():
        persona_convs = [c for c in convs if c.get("persona_id") == pid]
        if not persona_convs:
            continue
        total_turns = sum(len(c.get("turns", [])) for c in persona_convs)
        scenarios = sorted({c.get("scenario_seed_id") or c.get("scenario_type", "?")
                            for c in persona_convs})
        models = sorted({c.get("model", "hand-crafted") for c in persona_convs})
        # in-saga 時間範圍（依 occurred_at）
        occurred_dates = sorted([c.get("occurred_at", "")[:16] for c in persona_convs if c.get("occurred_at")])
        time_range = ""
        if occurred_dates:
            if len(occurred_dates) > 1:
                time_range = f"{occurred_dates[0]} → {occurred_dates[-1]}"
            else:
                time_range = occurred_dates[0]
        rows.append({
            "persona": pid,
            "name": p.get("name_or_pseudonym", "?"),
            "role": p.get("role", "?"),
            "n_conversations": len(persona_convs),
            "n_turns_total": total_turns,
            "scenarios": " · ".join(scenarios),
            "models": " · ".join(models),
            "time_range": time_range or "—",
        })

    # 顯示 personas 沒對話的
    no_data = [p for pid, p in personas.items()
               if not any(c.get("persona_id") == pid for c in convs)]

    st.markdown(f"### 已有對話的 personas ({len(rows)} / {len(personas)})")
    for row in rows:
        cols = st.columns([2, 1, 1, 4])
        cols[0].markdown(f"**{row['name']}** _{row['role']}_")
        cols[1].metric("對話", row["n_conversations"])
        cols[2].metric("總 turns", row["n_turns_total"])
        with cols[3]:
            if _is_dev_mode():
                st.caption(f"📌 scenarios: {row['scenarios']}")
            else:
                st.caption("📌 scenarios hidden in demo/pilot mode")
            st.caption(f"🕐 in-saga 時間範圍: {row['time_range']}")
            st.caption(f"🤖 models: {row['models']}")

    if no_data:
        st.divider()
        st.markdown(f"### ⚠️ 還沒有對話的 personas ({len(no_data)})")
        for p in no_data:
            st.caption(f"  • {p['id']} — {p.get('name_or_pseudonym', '?')} _{p.get('role', '?')}_")

    # Bottom: aggregate stats
    st.divider()
    st.markdown("### 📈 全部資料統計")
    total_cols = st.columns(4)
    total_cols[0].metric("總 personas", len(personas))
    total_cols[1].metric("有對話的 personas", len(rows))
    total_cols[2].metric("總對話數", len(convs))
    total_cols[3].metric("總 turns", sum(r["n_turns_total"] for r in rows))

    # 全部對話按 in-saga 時間排序的時間軸
    st.divider()
    st.markdown("### 🕐 In-Saga 時間軸（按 occurred_at 排序）")
    st.caption("Synthetic benchmark timeline. Scenario labels are hidden outside dev mode.")

    convs_with_time = [c for c in convs if c.get("occurred_at")]
    convs_sorted = sorted(convs_with_time, key=lambda c: c.get("occurred_at", ""))

    # 簡單按日分組
    from collections import defaultdict
    by_date: dict[str, list[dict]] = defaultdict(list)
    for c in convs_sorted:
        date = c.get("occurred_at", "?")[:10]
        by_date[date].append(c)

    for date in sorted(by_date.keys()):
        st.markdown(f"**📅 {date}**")
        for c in sorted(by_date[date], key=lambda x: x.get("occurred_at", "")):
            time_str = c.get("occurred_at", "?")[11:16]
            pid = c.get("persona_id", "?")
            name = personas.get(pid, {}).get("name_or_pseudonym", pid)
            scen = c.get("scenario_seed_id", "") if _is_dev_mode() else "hidden"
            n_t = len(c.get("turns", []))
            st.caption(f"　🕐 {time_str} · **{name}** × `{scen}` · {n_t} turns")


# ----------------------------------------------------------------------------
# Tab 4：Triage
# ----------------------------------------------------------------------------

def render_triage_tab():
    st.subheader("🚦 Triage：是否升級？")
    if not st.session_state.current_student:
        st.info("先選一個學生。")
        return

    profile = _current_profile()
    if not profile:
        st.warning("沒有 profile 可用。")
        return

    extra = st.text_area("額外觀察（可選）", height=80, placeholder="例：最近 3 次對話都提到失眠")
    if st.button("跑 Triage"):
        with st.spinner("判斷中……"):
            try:
                result = triage.should_escalate(profile, recent_signals=extra or None)
            except llm.LLMConfigError as e:
                st.error(str(e))
                return
            except Exception as e:  # noqa: BLE001
                st.error(f"出錯了：{e}")
                return

        urgency = result.get("urgency", "low")
        color = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(urgency, "⚪")

        st.markdown(f"### {color} 升級判斷")
        c1, c2 = st.columns(2)
        c1.metric("是否升級", "是" if result.get("escalate") else "否")
        c2.metric("緊急程度", urgency)
        st.markdown(f"**升級類別：** `{result.get('escalation_type')}`")
        st.markdown(f"**理由：** {result.get('reason')}")
        st.markdown(f"**建議行動：** {result.get('recommended_action')}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="三方 AI 教育協調 · MVP", layout="wide")
    _init_session_state()

    if not _check_api_key():
        st.stop()

    render_sidebar()

    tabs = st.tabs([
        "💬 三方 Live",
        "📋 三方分析",
        "📚 對話庫",
        "📊 歷史資訊",
        "🔐 Profile",
        "🤝 Coordinator (live)",
        "🚦 Triage",
    ])
    with tabs[0]:
        render_chat_tab()
    with tabs[1]:
        render_analysis_tab()
    with tabs[2]:
        render_corpus_tab()
    with tabs[3]:
        render_history_tab()
    with tabs[4]:
        render_profile_tab()
    with tabs[5]:
        render_coordinator_tab()
    with tabs[6]:
        render_triage_tab()


if __name__ == "__main__":
    main()
