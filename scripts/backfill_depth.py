"""backfill_depth.py — 給既有對話補 depth 欄位。

既有 corpus 全部是 depth 系統建立之前生的深度對話（stress_test / privacy_test /
hand-crafted deep arc），所以一律標成 deep。已有 depth 的不動（冪等）。

跑一次：python scripts/backfill_depth.py
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA = PROJECT_ROOT / "data"
GEN_DIR = DATA / "generated_conversations"
SD_PATH = DATA / "synthetic_dataset.json"

# scenario_type -> depth 對照（既有的 type 全都是 deep 類）
DEEP_TYPES = {"stress_test", "privacy_test", "deep_arc", "simulated", "crisis"}
SHALLOW_TYPES = {"mundane_help", "quick_vent", "logistics", "testing_ai",
                 "off_topic", "misuse_attempt", "parent_logistics"}
MEDIUM_TYPES = {"moderate_issue", "mixed", "privacy_probe"}


def infer_depth(conv: dict) -> str:
    """已有 depth 就用既有的；否則從 scenario_type 推；再不行用 turn 數。"""
    if conv.get("depth"):
        return conv["depth"]
    st = conv.get("scenario_type", "")
    if st in SHALLOW_TYPES:
        return "shallow"
    if st in MEDIUM_TYPES:
        return "medium"
    if st in DEEP_TYPES:
        return "deep"
    # fallback: 用 turn 數
    n = len(conv.get("turns", []))
    if n <= 10:
        return "shallow"
    if n <= 22:
        return "medium"
    return "deep"


def backfill_generated() -> tuple[int, int]:
    updated = skipped = 0
    for f in sorted(GEN_DIR.glob("sim_*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        if data.get("depth"):
            skipped += 1
            continue
        data["depth"] = infer_depth(data)
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        updated += 1
    return updated, skipped


def backfill_index() -> int:
    idx = GEN_DIR / "index.json"
    if not idx.exists():
        return 0
    index = json.loads(idx.read_text(encoding="utf-8"))
    updated = 0
    # 建立 id -> depth map（從剛 backfill 的檔案）
    depth_map: dict[str, str] = {}
    for f in GEN_DIR.glob("sim_*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("id") and d.get("depth"):
            depth_map[d["id"]] = d["depth"]
    for c in index.get("conversations", []):
        if not c.get("depth") and c.get("id") in depth_map:
            c["depth"] = depth_map[c["id"]]
            updated += 1
    idx.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return updated


def backfill_synthetic_dataset() -> int:
    if not SD_PATH.exists():
        return 0
    sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
    updated = 0
    for c in sd.get("conversations", []):
        if not c.get("depth"):
            c["depth"] = infer_depth(c)
            updated += 1
    SD_PATH.write_text(json.dumps(sd, ensure_ascii=False, indent=2), encoding="utf-8")
    return updated


def main() -> int:
    print("Backfilling depth fields...")
    gen_updated, gen_skipped = backfill_generated()
    idx_updated = backfill_index()
    sd_updated = backfill_synthetic_dataset()
    print(f"  generated_conversations: {gen_updated} updated, {gen_skipped} already had depth")
    print(f"  index.json: {idx_updated} entries updated")
    print(f"  synthetic_dataset.json: {sd_updated} conversations updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
