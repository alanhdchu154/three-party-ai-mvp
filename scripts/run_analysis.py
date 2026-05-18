"""run_analysis.py — 三方分析 pipeline 整合 runner。

對一個學生跑完整流程：
  1. Load 該學生的所有對話（hand-crafted + simulated）
  2. abstraction.py 抽 profile（隱私牆）
  3. validate_no_raw_quotes 健檢
  4. 從 dummy_inputs.json 拉對應的家長 + 老師輸入
  5. coordinator.synthesize 產出分析報告
  6. 印出 + 存到 data/analysis_reports/

Usage:
    python scripts/run_analysis.py --student michael
    python scripts/run_analysis.py --student rachel
    python scripts/run_analysis.py --student shen_you

    # 跑全部學生
    python scripts/run_analysis.py --all
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import warnings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 滅噪
os.environ["LITELLM_LOG"] = "ERROR"
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", module="litellm")

from src import abstraction, coordinator, llm  # noqa: E402

DATA = PROJECT_ROOT / "data"
GEN = DATA / "generated_conversations"
SD_PATH = DATA / "synthetic_dataset.json"
DUMMY_PATH = DATA / "dummy_inputs.json"
REPORTS = DATA / "analysis_reports"
REPORTS.mkdir(parents=True, exist_ok=True)

# 學生 ID 對應
STUDENT_MAP = {
    "michael":  {"persona_id": "saga_a_michael",  "dummy_scenario": "scenario_michael"},
    "rachel":   {"persona_id": "saga_a_rachel",   "dummy_scenario": "scenario_rachel"},
    "shen_you": {"persona_id": "saga_a_shen_you", "dummy_scenario": "scenario_shen_you"},
    "keer":     {"persona_id": "saga_a_keer",     "dummy_scenario": None},
}


def load_all_conversations(persona_id: str) -> list[dict]:
    """從兩個來源 load 該 persona 的所有對話：
    1. synthetic_dataset.json（hand-crafted gold standard）
    2. generated_conversations/（simulation 跟 hand-crafted reference）
    """
    convs: list[dict] = []

    # Source 1
    if SD_PATH.exists():
        sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
        for c in sd.get("conversations", []):
            if c.get("persona_id") == persona_id:
                convs.append(c)

    # Source 2
    if GEN.exists():
        for f in sorted(GEN.glob(f"sim_{persona_id}__*.json")):
            convs.append(json.loads(f.read_text(encoding="utf-8")))

    return convs


def merge_conversation_turns(convs: list[dict]) -> list[dict]:
    """把多段對話 turns 串起來餵給 abstraction。每段之間插個分隔。"""
    merged: list[dict] = []
    for i, conv in enumerate(convs):
        if i > 0:
            merged.append({"role": "user", "content": "（換場景 — 不同時間的對話）"})
        merged.extend(conv.get("turns", []))
    return merged


def load_dummy_inputs(scenario_id: str | None) -> tuple[str, str]:
    """從 dummy_inputs.json 拉家長 + 老師輸入。"""
    if not scenario_id or not DUMMY_PATH.exists():
        return "（沒有家長輸入）", "（沒有老師輸入）"
    data = json.loads(DUMMY_PATH.read_text(encoding="utf-8"))
    for s in data.get("scenarios", []):
        if s.get("id") == scenario_id:
            return s.get("parent_input", "") or "（沒有家長輸入）", \
                   s.get("teacher_input", "") or "（沒有老師輸入）"
    return "（找不到對應 scenario）", "（找不到對應 scenario）"


def analyze_student(short_id: str) -> dict:
    """跑完整 pipeline，回傳 analysis report。"""
    info = STUDENT_MAP[short_id]
    persona_id = info["persona_id"]
    print(f"\n{'=' * 60}")
    print(f"📊 分析學生：{short_id}（persona_id = {persona_id}）")
    print(f"{'=' * 60}")

    # 1. Load conversations
    convs = load_all_conversations(persona_id)
    if not convs:
        print(f"   ❌ 找不到 {persona_id} 的對話。先跑 simulation 或 hand-craft。")
        return {}
    print(f"\n📂 載入 {len(convs)} 段對話")
    for c in convs:
        print(f"   - {c.get('id', '?')}（{len(c.get('turns', []))} turns）")

    # 2. Abstraction
    merged_turns = merge_conversation_turns(convs)
    print(f"\n🔐 跑 abstraction（隱私牆）...")
    try:
        profile = abstraction.extract_profile(merged_turns)
    except Exception as e:
        print(f"   ❌ Abstraction 失敗：{e}")
        return {}
    print(f"   ✅ profile 抽出，emotional_state: {profile.get('emotional_state', '?')}")

    # 3. Privacy wall check
    leaked = abstraction.validate_no_raw_quotes(profile, merged_turns)
    if leaked:
        print(f"   ⚠️  隱私牆檢測到 {len(leaked)} 句疑似洩漏：{leaked[:2]}")
    else:
        print(f"   ✅ 隱私牆通過（profile 不含對話原話）")

    # 4. Load parent + teacher input
    parent_input, teacher_input = load_dummy_inputs(info["dummy_scenario"])
    print(f"\n👨‍👩‍👧 載入家長 + 老師輸入（from {info['dummy_scenario']}）")

    # 5. Coordinator
    print(f"\n🤝 跑 Coordinator 三方分析...")
    try:
        plan = coordinator.synthesize(profile, parent_input, teacher_input)
    except Exception as e:
        print(f"   ❌ Coordinator 失敗：{e}")
        return {}

    # 6. Output
    report = {
        "student": short_id,
        "persona_id": persona_id,
        "n_conversations": len(convs),
        "conversation_ids": [c.get("id") for c in convs],
        "student_profile": profile,
        "parent_input": parent_input,
        "teacher_input": teacher_input,
        "analysis": plan,
    }

    out_path = REPORTS / f"{short_id}_analysis.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📁 完整報告存到：{out_path.relative_to(PROJECT_ROOT)}")

    # Pretty print（新 schema）
    print(f"\n{'─' * 60}")
    print(f"🎯 真正在發生的事")
    print(f"{'─' * 60}")
    print(plan.get("whats_really_happening", ""))

    wkw = plan.get("who_knows_what", {})
    print(f"\n{'─' * 60}")
    print(f"🔀 三方各自知道什麼")
    print(f"{'─' * 60}")
    print(f"  👨‍👩‍👧 家長看到：{wkw.get('parent_sees', '')}")
    print(f"  👨‍🏫 老師看到：{wkw.get('teacher_sees', '')}")
    print(f"  🤐 學生獨自知道：{wkw.get('student_knows_alone', '')}")

    pk = plan.get("privacy_kept", [])
    if pk:
        print(f"\n{'─' * 60}")
        print(f"🔒 系統保護的事項（不會傳給家長 / 老師）")
        print(f"{'─' * 60}")
        for p in pk:
            print(f"  • {p}")

    week = plan.get("this_week", {})
    for party_key, party_label, emoji in [
        ("for_student", short_id, "💬"),
        ("for_parent", "家長", "👨‍👩‍👧"),
        ("for_teacher", "老師", "👨‍🏫"),
    ]:
        actions = week.get(party_key, {})
        do_items = actions.get("do", [])
        dont_items = actions.get("dont", [])
        if not do_items and not dont_items:
            continue
        print(f"\n{'─' * 60}")
        print(f"{emoji} 這禮拜 {party_label} 該做的事")
        print(f"{'─' * 60}")
        for item in do_items:
            print(f"  ✅ {item}")
        for item in dont_items:
            print(f"  ❌ {item}")

    watch = plan.get("watch_for", [])
    if watch:
        print(f"\n{'─' * 60}")
        print(f"👀 下一週要 notice 的訊號")
        print(f"{'─' * 60}")
        for w in watch:
            print(f"  • {w}")

    if plan.get("needs_external_intervention"):
        print(f"\n{'─' * 60}")
        print(f"🚨 需要外部專業介入")
        print(f"{'─' * 60}")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--student", choices=list(STUDENT_MAP.keys()),
                        help="只跑這個學生的分析")
    parser.add_argument("--all", action="store_true",
                        help="跑所有有 dummy_inputs 的學生（除 keer）")
    args = parser.parse_args()

    if not args.student and not args.all:
        print("請指定 --student <name> 或 --all")
        return 1

    targets = (
        [s for s in STUDENT_MAP if STUDENT_MAP[s]["dummy_scenario"]]
        if args.all else [args.student]
    )

    print(f"\n🚀 跑 {len(targets)} 個學生分析，模型：{llm.DEFAULT_MODEL}")

    for short_id in targets:
        try:
            analyze_student(short_id)
        except Exception as e:
            print(f"\n❌ {short_id} 分析失敗：{e}")
            continue

    print(f"\n\n✨ 完成。所有報告在 {REPORTS.relative_to(PROJECT_ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
