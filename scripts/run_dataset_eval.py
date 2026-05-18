"""跑整個 synthetic dataset 的回歸評測。

用途：
- 改完 prompt 後跑一次，看 abstraction / triage 在 dataset 上的表現
- 產出 markdown 報告到 stdout（也可導到檔案）

執行：
    python -m scripts.run_dataset_eval
    python -m scripts.run_dataset_eval > eval_report.md
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# 讓 `python scripts/run_dataset_eval.py` 也能跑
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import abstraction, triage  # noqa: E402

DATASET_PATH = ROOT / "data" / "synthetic_dataset.json"


def _check_key() -> None:
    """檢查當前 LLM_MODEL 對應的 key 是否已設。Ollama 本地不需要。"""
    from src.llm import DEFAULT_MODEL, _PROVIDER_KEY_MAP, _provider_of

    provider = _provider_of(DEFAULT_MODEL)
    if provider == "ollama":
        return
    key_name = _PROVIDER_KEY_MAP.get(provider)
    if not key_name:
        return
    val = os.getenv(key_name, "")
    if not val or val.startswith("your-") or val.startswith("sk-ant-xxxxxxxx"):
        print(
            f"❌ 沒設 {key_name}（model={DEFAULT_MODEL} 需要）。\n"
            "先 cp .env.example .env 並填入 key。",
            file=sys.stderr,
        )
        sys.exit(1)


def _load_dataset() -> dict:
    if not DATASET_PATH.exists():
        print(f"❌ 找不到 dataset：{DATASET_PATH}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    if not data.get("conversations"):
        print("❌ dataset 是空的。請先從 dataset 任務複製資料過來。", file=sys.stderr)
        sys.exit(1)
    return data


def evaluate(data: dict, limit: int | None = None) -> dict:
    """跑 dataset，回傳 metrics。"""
    convs = data["conversations"]
    if limit:
        convs = convs[:limit]

    results = []
    leak_count = 0
    triage_correct = 0
    triage_total = 0

    for conv in convs:
        cid = conv.get("id", "?")
        print(f"[{cid}] 跑 abstraction……", file=sys.stderr)
        try:
            profile = abstraction.extract_profile(conv["turns"])
        except Exception as e:  # noqa: BLE001
            results.append({"conv_id": cid, "status": "abstraction_error", "error": str(e)})
            continue

        leaked = abstraction.validate_no_raw_quotes(profile, conv["turns"])
        if leaked:
            leak_count += 1

        print(f"[{cid}] 跑 triage……", file=sys.stderr)
        try:
            tri = triage.should_escalate(profile)
        except Exception as e:  # noqa: BLE001
            results.append({"conv_id": cid, "status": "triage_error", "error": str(e)})
            continue

        expected = conv.get("should_trigger_triage")
        triage_match = expected is None or (bool(tri["escalate"]) == bool(expected))
        if expected is not None:
            triage_total += 1
            if triage_match:
                triage_correct += 1

        results.append({
            "conv_id": cid,
            "scenario_type": conv.get("scenario_type"),
            "expected_trigger": expected,
            "got_trigger": tri["escalate"],
            "got_escalation_type": tri["escalation_type"],
            "got_urgency": tri["urgency"],
            "leaked_quotes": leaked,
            "risk_flags": profile.get("risk_flags", []),
        })

    return {
        "total": len(convs),
        "privacy_leak_count": leak_count,
        "triage_accuracy": (triage_correct / triage_total) if triage_total else None,
        "triage_total": triage_total,
        "triage_correct": triage_correct,
        "details": results,
    }


def render_markdown(report: dict) -> str:
    lines = []
    lines.append("# Dataset 評測報告\n")
    lines.append(f"- Total 對話：{report['total']}")
    lines.append(f"- 隱私洩漏：{report['privacy_leak_count']} / {report['total']}")
    acc = report["triage_accuracy"]
    if acc is not None:
        lines.append(f"- Triage 正確率：{acc:.1%} ({report['triage_correct']}/{report['triage_total']})")
    else:
        lines.append("- Triage 正確率：（dataset 沒標 expected）")

    lines.append("\n## 細節\n")
    lines.append("| conv_id | 類型 | 預期升級 | 實際升級 | 類別 | urgency | 洩漏 |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in report["details"]:
        if r.get("status"):
            lines.append(f"| {r['conv_id']} | ⚠️ {r['status']} | - | - | - | - | - |")
            continue
        lines.append(
            f"| {r['conv_id']} | {r.get('scenario_type', '')} "
            f"| {r.get('expected_trigger')} | {r.get('got_trigger')} "
            f"| {r.get('got_escalation_type')} | {r.get('got_urgency')} "
            f"| {'⚠️ ' + str(len(r['leaked_quotes'])) if r.get('leaked_quotes') else '✅'} |"
        )

    return "\n".join(lines)


def main() -> None:
    _check_key()
    data = _load_dataset()

    limit_env = os.getenv("EVAL_LIMIT")
    limit = int(limit_env) if limit_env and limit_env.isdigit() else None

    report = evaluate(data, limit=limit)
    print(render_markdown(report))


if __name__ == "__main__":
    main()
