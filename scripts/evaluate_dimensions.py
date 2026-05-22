"""evaluate_dimensions.py — 七維度評分 evaluator。

對每個學生跑：
  1. Load 他所有對話（synthetic_dataset.json + generated_conversations/）
  2. 把對話內容 + dimension_evaluator.txt rubric 餵 LLM
  3. LLM 回 JSON：7 個維度的 level (0-3) + signals + reasoning
  4. 計算 cumulative_strain（7 個 level 加總）
  5. 存到 data/dimension_scores/{student}.json

Usage:
    # 只評一個學生
    python scripts/evaluate_dimensions.py --student michael

    # 評全部學生 personas
    python scripts/evaluate_dimensions.py --all

    # 只評 role=student 的（默認排除家長/老師 personas）
    python scripts/evaluate_dimensions.py --all --students-only
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import warnings
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 滅噪
os.environ["LITELLM_LOG"] = "ERROR"
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", module="litellm")

from src import llm  # noqa: E402


# ----------------------------------------------------------------------------
# Rate-limit retry wrapper (處理 Groq TPM / RPM limit)
# ----------------------------------------------------------------------------

def _extract_retry_seconds(err_msg: str) -> float | None:
    """從錯誤訊息抓 retry delay。
    Groq 格式：'Please try again in 3.136s'
    Gemini 格式：'Please retry in 4.6s' 或 '"retryDelay":"4s"'
    """
    m = re.search(r"try again in ([\d.]+)s", err_msg)
    if m:
        return float(m.group(1))
    m = re.search(r"retry in ([\d.]+)s", err_msg)
    if m:
        return float(m.group(1))
    m = re.search(r'"retryDelay":\s*"(\d+)s"', err_msg)
    if m:
        return float(m.group(1))
    return None


def complete_json_with_retry(
    system: str,
    messages: list[dict[str, str]],
    *,
    max_retries: int = 6,
    base_backoff: float = 10.0,
    **kwargs: Any,
) -> dict:
    """呼叫 llm.complete_json，遇 rate limit 自動 sleep 重試。"""
    for attempt in range(max_retries):
        try:
            return llm.complete_json(system=system, messages=messages, **kwargs)
        except llm.LLMConfigError as e:
            msg = str(e)
            if ("RateLimit" not in msg
                and "rate_limit" not in msg
                and "RESOURCE_EXHAUSTED" not in msg
                and "429" not in msg):
                raise
            wait = _extract_retry_seconds(msg) or (base_backoff * (2 ** attempt))
            wait = min(wait + 1.0, 90.0)  # +1s buffer, max 90s
            print(f"    ⏳ rate limited, sleeping {wait:.1f}s (attempt {attempt + 1}/{max_retries})...",
                  flush=True)
            time.sleep(wait)
    raise llm.LLMConfigError(f"重試 {max_retries} 次仍 rate limited，放棄這個 call")

DATA = PROJECT_ROOT / "data"
SD_PATH = DATA / "synthetic_dataset.json"
GEN_DIR = DATA / "generated_conversations"
OUTPUT_DIR = DATA / "dimension_scores"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# 學生短 ID → persona_id 對應（給 --student 用）
STUDENT_SHORT_NAMES = {
    "michael": "saga_a_michael",
    "michael_mom": "saga_a_michael_mom",
    "stepdad": "saga_a_stepdad",
    "keer": "saga_a_keer",
    "uncle": "saga_a_uncle",
    "rachel": "saga_a_rachel",
    "shen_you": "saga_a_shen_you",
    "shen_mom": "saga_a_shen_mom",
    "alan_teacher": "saga_a_alan_teacher",
}


def load_all_conversations(persona_id: str) -> list[dict]:
    """從兩個 source 撈 persona 的所有對話。"""
    convs: list[dict] = []

    if SD_PATH.exists():
        sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
        for c in sd.get("conversations", []):
            if c.get("persona_id") == persona_id:
                convs.append(c)

    if GEN_DIR.exists():
        for f in sorted(GEN_DIR.glob(f"sim_{persona_id}__*.json")):
            convs.append(json.loads(f.read_text(encoding="utf-8")))

    return convs


def load_persona_info(persona_id: str) -> dict:
    if not SD_PATH.exists():
        return {}
    sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
    for p in sd.get("personas", []):
        if p["id"] == persona_id:
            return p
    return {}


def format_conversations_for_eval(convs: list[dict]) -> str:
    """把多段對話格式化成 LLM 可讀的單一 input。"""
    parts = []
    for i, conv in enumerate(convs, 1):
        scen = conv.get("scenario_seed_id", conv.get("scenario_type", "?"))
        scen_seed = conv.get("scenario_seed", "")
        parts.append(f"=== 對話 {i} | scenario: {scen} ===")
        if scen_seed:
            parts.append(f"情境：{scen_seed}\n")
        for turn in conv.get("turns", []):
            role = turn.get("role", "?")
            content = turn.get("content", "")
            speaker = "學生" if role == "user" else "AI"
            parts.append(f"{speaker}：{content}")
        parts.append("")
    return "\n".join(parts)


def evaluate_persona(persona_id: str, verbose: bool = True) -> dict | None:
    """跑一個 persona 的七維度評分。"""
    persona_info = load_persona_info(persona_id)
    name = persona_info.get("name_or_pseudonym", persona_id)
    role = persona_info.get("role", "?")

    print(f"\n{'=' * 60}")
    print(f"📐 評分：{name}（{persona_id}, role={role}）")
    print(f"{'=' * 60}")

    convs = load_all_conversations(persona_id)
    if not convs:
        print(f"   ❌ 找不到對話")
        return None
    print(f"   📂 載入 {len(convs)} 段對話")

    conv_text = format_conversations_for_eval(convs)
    print(f"   📏 對話總長度：{len(conv_text):,} 字元")

    system = llm.load_prompt("dimension_evaluator")
    user_msg = (
        f"以下是 {name}（{persona_id}）總共 {len(convs)} 段對話。"
        f"請按七維度 rubric 評分。\n\n"
        f"{conv_text}\n\n"
        "請輸出嚴格 JSON。"
    )

    print(f"   🤖 跑 LLM ({llm.DEFAULT_MODEL})...", flush=True)
    try:
        result = complete_json_with_retry(
            system=system,
            messages=[{"role": "user", "content": user_msg}],
            max_tokens=3000,
            temperature=0.3,
        )
    except Exception as e:
        print(f"   ❌ LLM 失敗：{e}")
        return None

    # 補齊欄位
    result.setdefault("student_persona_id", persona_id)
    result.setdefault("n_conversations_evaluated", len(convs))
    result.setdefault("dimensions", {})
    for dim in ["emotional_safety", "academic_load", "family_dynamics",
                "social_development", "identity", "financial_pressure",
                "future_planning"]:
        result["dimensions"].setdefault(dim, {"level": 0, "signals_observed": [], "reasoning": ""})

    # 計算 cumulative
    levels = [result["dimensions"][d].get("level", 0) for d in result["dimensions"]]
    result["cumulative_strain"] = sum(levels)
    result.setdefault("highest_concern_dimension", "")
    result.setdefault("trend_notes", "")
    result["evaluated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    result["model"] = llm.DEFAULT_MODEL

    # 存
    short_name = next((k for k, v in STUDENT_SHORT_NAMES.items() if v == persona_id), persona_id)
    out_path = OUTPUT_DIR / f"{short_name}.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # 印 summary
    print(f"\n   📊 維度評分：")
    dim_labels = {
        "emotional_safety": "情緒安全",
        "academic_load":    "學業負擔",
        "family_dynamics":  "家庭關係",
        "social_development": "社交發展",
        "identity":         "身分認同",
        "financial_pressure": "經濟壓力",
        "future_planning":  "未來規劃",
    }
    for dim, label in dim_labels.items():
        level = result["dimensions"].get(dim, {}).get("level", 0)
        bar = "●" * level + "○" * (3 - level)
        print(f"      {label}    {bar}  {level}/3")

    print(f"\n   累計 strain: {result['cumulative_strain']}/21")
    print(f"   最高 concern: {result.get('highest_concern_dimension')}")
    if result.get("trend_notes"):
        print(f"   趨勢：{result['trend_notes']}")
    print(f"\n   📁 存到 {out_path.relative_to(PROJECT_ROOT)}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--student", help="只評一個學生（short name 例如 michael）")
    parser.add_argument("--persona", help="或直接給 persona_id（例如 saga_a_michael）")
    parser.add_argument("--all", action="store_true", help="評全部 personas")
    parser.add_argument("--students-only", action="store_true",
                        help="搭配 --all 使用；只評 role=student 的")
    args = parser.parse_args()

    # 決定要評誰
    targets: list[str] = []
    if args.student:
        targets = [STUDENT_SHORT_NAMES.get(args.student, args.student)]
    elif args.persona:
        targets = [args.persona]
    elif args.all:
        sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
        all_personas = sd.get("personas", [])
        if args.students_only:
            targets = [p["id"] for p in all_personas if p.get("role") == "student"]
        else:
            targets = [p["id"] for p in all_personas]
    else:
        print("請指定 --student <name> 或 --persona <id> 或 --all")
        return 1

    print(f"\n🚀 跑七維度評分。模型：{llm.DEFAULT_MODEL}。Targets: {len(targets)}")

    results = []
    for pid in targets:
        r = evaluate_persona(pid)
        if r:
            results.append(r)
        # Groq free tier 30K TPM、每 persona ~6K token，sleep 15s 確保平均 24K TPM 安全範圍
        time.sleep(15)

    # Aggregate summary
    print(f"\n\n{'=' * 60}")
    print(f"✨ 完成。{len(results)} 個 personas 評分")
    print(f"{'=' * 60}")
    if results:
        sorted_results = sorted(results, key=lambda r: r["cumulative_strain"], reverse=True)
        print(f"\n按 cumulative_strain 排序（高到低）：")
        for r in sorted_results:
            pid = r["student_persona_id"]
            short = next((k for k, v in STUDENT_SHORT_NAMES.items() if v == pid), pid)
            print(f"  {r['cumulative_strain']:>2}/21  {short:<14}  最高 concern: {r.get('highest_concern_dimension', '?')}")

    print(f"\n📁 所有報告在 {OUTPUT_DIR.relative_to(PROJECT_ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
