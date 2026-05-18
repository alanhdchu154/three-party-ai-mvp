"""Streamlit 入口——學生 AI + Coordinator + Triage 的視覺化介面。

執行：streamlit run app.py
"""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from src import abstraction, coordinator, llm, profile_store, student_agent, triage

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
    if "history" not in st.session_state:
        # 對話 history 只存在 session 裡——刻意不寫檔（隱私牆）
        st.session_state.history = []
    if "last_profile" not in st.session_state:
        st.session_state.last_profile = None


# ----------------------------------------------------------------------------
# Sidebar：選 / 新建學生
# ----------------------------------------------------------------------------

def render_sidebar():
    st.sidebar.title("三方 AI · MVP")
    st.sidebar.caption("Phase 1 Lean MVP · 學生端 + Coordinator")

    existing = profile_store.list_profiles()

    choice = st.sidebar.selectbox(
        "選一個學生",
        options=["（新建）"] + existing,
        index=0 if st.session_state.current_student is None else
              (existing.index(st.session_state.current_student) + 1
               if st.session_state.current_student in existing else 0),
    )

    if choice == "（新建）":
        new_id = st.sidebar.text_input("學生 ID（例：alice_g9）")
        if st.sidebar.button("建立") and new_id.strip():
            st.session_state.current_student = new_id.strip()
            st.session_state.history = []
            st.session_state.last_profile = None
            st.rerun()
    else:
        if choice != st.session_state.current_student:
            st.session_state.current_student = choice
            st.session_state.history = []
            st.session_state.last_profile = profile_store.load_profile(choice)
            st.rerun()

    st.sidebar.divider()

    if st.session_state.current_student:
        st.sidebar.markdown(f"**目前學生：** `{st.session_state.current_student}`")
        if st.sidebar.button("清空當前對話（不影響 profile）"):
            st.session_state.history = []
            st.rerun()
        if st.sidebar.button("⚠️ 刪除這個學生 profile"):
            profile_store.delete_profile(st.session_state.current_student)
            st.session_state.current_student = None
            st.session_state.history = []
            st.session_state.last_profile = None
            st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("⚙️ 模型：" + llm.DEFAULT_MODEL)


# ----------------------------------------------------------------------------
# Tab 1：聊天
# ----------------------------------------------------------------------------

def render_chat_tab():
    st.subheader("💬 學生 ↔ 學生 AI")
    if not st.session_state.current_student:
        st.info("先在左側選一個學生（或新建）。")
        return

    # 顯示 history
    for turn in st.session_state.history:
        role = turn["role"]
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(turn["content"])

    # 輸入
    user_msg = st.chat_input("以學生身份輸入訊息……")
    if user_msg:
        st.session_state.history.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            with st.spinner("AI 在想……"):
                try:
                    reply = student_agent.chat(
                        user_msg, history=st.session_state.history[:-1]
                    )
                except llm.LLMConfigError as e:
                    st.error(str(e))
                    return
                except Exception as e:  # noqa: BLE001
                    st.error(f"出錯了：{e}")
                    return
            st.markdown(reply)
        st.session_state.history.append({"role": "assistant", "content": reply})

    st.divider()
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("📝 更新 Profile", disabled=not st.session_state.history):
            with st.spinner("抽象化中……"):
                try:
                    profile = abstraction.extract_profile(st.session_state.history)
                    profile_store.save_profile(
                        st.session_state.current_student, profile
                    )
                    st.session_state.last_profile = profile
                    st.success("Profile 已更新。切到「Profile」分頁看結果。")
                except llm.LLMConfigError as e:
                    st.error(str(e))
                except Exception as e:  # noqa: BLE001
                    st.error(f"抽象化失敗：{e}")
    with col2:
        st.caption(
            "提示：對話結束後按「更新 Profile」，讓抽象化模組把這次對話"
            "整理成 profile JSON。對話原話不會被儲存到磁碟。"
        )


# ----------------------------------------------------------------------------
# Tab 2：Profile
# ----------------------------------------------------------------------------

def render_profile_tab():
    st.subheader("🔐 學生 Profile（抽象化後）")
    if not st.session_state.current_student:
        st.info("先選一個學生。")
        return

    profile = st.session_state.last_profile or profile_store.load_profile(
        st.session_state.current_student
    )
    if not profile:
        st.warning("還沒有 profile。在「聊天」分頁聊幾句後按『更新 Profile』。")
        return

    # 隱私牆健檢
    if st.session_state.history:
        leaked = abstraction.validate_no_raw_quotes(profile, st.session_state.history)
        if leaked:
            st.error(
                f"⚠️ 隱私牆檢測到 {len(leaked)} 句原話可能被洩漏到 profile："
                f"{leaked[:3]}"
            )
        else:
            st.success("✅ 隱私牆檢測通過：profile 不含對話原話。")

    st.json(profile)


# ----------------------------------------------------------------------------
# Tab 3：Coordinator
# ----------------------------------------------------------------------------

def render_coordinator_tab():
    st.subheader("🤝 Coordinator：三方協調")
    if not st.session_state.current_student:
        st.info("先選一個學生。")
        return

    profile = st.session_state.last_profile or profile_store.load_profile(
        st.session_state.current_student
    )
    if not profile:
        st.warning("沒有 profile 可用。先到「聊天」分頁產生一個。")
        return

    scenarios = _load_dummy_scenarios()
    labels = ["（自訂）"] + [s["label"] for s in scenarios]
    pick = st.selectbox("選一個 dummy 家長/老師輸入", labels)

    if pick == "（自訂）":
        parent_input = st.text_area("家長輸入", height=120)
        teacher_input = st.text_area("老師輸入", height=120)
    else:
        chosen = scenarios[labels.index(pick) - 1]
        parent_input = st.text_area("家長輸入", value=chosen["parent_input"], height=120)
        teacher_input = st.text_area("老師輸入", value=chosen["teacher_input"], height=120)

    if st.button("產出協調方案"):
        with st.spinner("Coordinator 正在合成……"):
            try:
                plan = coordinator.synthesize(profile, parent_input, teacher_input)
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


def _list_analysis_reports() -> list[tuple[str, Path]]:
    """回傳 [(student_label, path), ...]。"""
    if not REPORTS_DIR.exists():
        return []
    out = []
    for f in sorted(REPORTS_DIR.glob("*_analysis.json")):
        name = f.stem.replace("_analysis", "")
        out.append((name, f))
    return out


def render_analysis_tab():
    st.subheader("📋 三方分析報告")
    st.caption("由 coordinator 從學生 / 家長 / 老師三方 AI 對話合成。"
               "原話不會跨方流動 — 隱私牆已執行。")

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
    meta_cols = st.columns(3)
    meta_cols[0].metric("學生", data.get("student", pick))
    meta_cols[1].metric("資料來源對話數", data.get("n_conversations", 0))
    if analysis.get("needs_external_intervention"):
        meta_cols[2].error("🚨 需要外部專業介入")
    else:
        meta_cols[2].success("✅ 系統可處理範圍")

    st.divider()

    # 🎯 真正在發生的事
    st.markdown("### 🎯 真正在發生的事")
    whats = analysis.get("whats_really_happening", "")
    if whats:
        st.info(whats)
    else:
        st.caption("（沒有 whats_really_happening 欄位）")

    # 🔀 三方各自知道什麼
    st.markdown("### 🔀 三方各自知道什麼")
    wkw = analysis.get("who_knows_what", {})
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
    privacy_kept = analysis.get("privacy_kept", [])
    if privacy_kept:
        with st.expander(f"🔒 系統保護的事項（{len(privacy_kept)} 項不會傳給家長 / 老師）"):
            for p in privacy_kept:
                st.markdown(f"- {p}")

    st.divider()

    # 💬 這禮拜該做的事
    st.markdown("### 💬 這禮拜該做的事")
    week = analysis.get("this_week", {})
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
    watch = analysis.get("watch_for", [])
    if watch:
        st.divider()
        st.markdown("### 👀 下週要 notice 的訊號")
        for w in watch:
            st.markdown(f"- {w}")

    # 原始資料（給 dev 看的，藏在 expander）
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

    # List conversations for this persona
    st.markdown(f"### 此 persona 的 {len(by_persona[chosen_pid])} 段對話")
    for i, conv in enumerate(by_persona[chosen_pid], 1):
        conv_id = conv.get("id", f"#{i}")
        n_turns = len(conv.get("turns", []))
        scen = conv.get("scenario_seed_id") or conv.get("scenario_type", "")
        source = conv.get("_source", "")
        with st.expander(f"💬 {conv_id} · {n_turns} turns · scenario: {scen} · _{source}_"):
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
        dates = sorted({c.get("generated_at", "?")[:10] for c in persona_convs if c.get("generated_at")})
        rows.append({
            "persona": pid,
            "name": p.get("name_or_pseudonym", "?"),
            "role": p.get("role", "?"),
            "n_conversations": len(persona_convs),
            "n_turns_total": total_turns,
            "scenarios": " · ".join(scenarios),
            "models": " · ".join(models),
            "dates": " · ".join(dates) if dates else "—",
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
            st.caption(f"📌 scenarios: {row['scenarios']}")
            st.caption(f"🤖 models: {row['models']}")
            st.caption(f"📅 dates: {row['dates']}")

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


# ----------------------------------------------------------------------------
# Tab 4：Triage
# ----------------------------------------------------------------------------

def render_triage_tab():
    st.subheader("🚦 Triage：是否升級？")
    if not st.session_state.current_student:
        st.info("先選一個學生。")
        return

    profile = st.session_state.last_profile or profile_store.load_profile(
        st.session_state.current_student
    )
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
        "📋 三方分析",
        "📚 對話庫",
        "📊 歷史資訊",
        "💬 聊天 (live)",
        "🔐 Profile",
        "🤝 Coordinator (live)",
        "🚦 Triage",
    ])
    with tabs[0]:
        render_analysis_tab()
    with tabs[1]:
        render_corpus_tab()
    with tabs[2]:
        render_history_tab()
    with tabs[3]:
        render_chat_tab()
    with tabs[4]:
        render_profile_tab()
    with tabs[5]:
        render_coordinator_tab()
    with tabs[6]:
        render_triage_tab()


if __name__ == "__main__":
    main()
