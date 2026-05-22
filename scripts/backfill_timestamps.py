"""backfill_timestamps.py — 給既有對話加上 occurred_at 欄位（in-world saga 時間）。

設計：
- Saga「現在」是 2026-05-20
- 每段對話按敘事邏輯放在過去 3 週
- 每個 persona 有「上線習慣」時段
- 保留 generated_at（meta-tracking），新增 occurred_at（in-world）

跑一次：python scripts/backfill_timestamps.py
冪等：重跑會覆寫 occurred_at（如果已存在就更新）
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA = PROJECT_ROOT / "data"
SD_PATH = DATA / "synthetic_dataset.json"
GEN_DIR = DATA / "generated_conversations"


# 對話 ID → occurred_at 對應表
# 時間考量：
# - Saga 現在 = 2026-05-20
# - 每個 persona 有上線時段（青少年深夜、家長下午、老師放學後...）
# - 對話按敘事邏輯排序（family gathering 觸發 Michael philosophy_burn 等）
OCCURRED_AT_MAP: dict[str, str] = {
    # === Michael ===
    "conv_a01":                                "2026-05-13T23:42:00",  # philosophy_burn after gathering
    "conv_a02":                                "2026-05-14T00:18:00",  # rachel_eye_contact (next night)
    "sim_saga_a_michael__philosophy_burn":     "2026-05-13T23:50:00",  # Groq version, same scene
    "sim_saga_a_michael__mom_crying":          "2026-05-17T23:12:00",  # heard mom cry night before
    "sim_saga_a_michael__shen_you_question":   "2026-05-19T00:36:00",  # 沈又's LINE same day evening

    # === Michael 媽 ===
    "conv_a03":                                       "2026-05-10T14:38:00",  # ex_divorce_calc, ongoing weeks
    "sim_saga_a_michael_mom__michael_pulled_away":    "2026-05-18T14:22:00",  # after Michael said 不要煩

    # === 後爸 ===
    "sim_saga_a_stepdad__failed_bonding_attempt":     "2026-05-16T09:14:00",  # Saturday morning, day after dinner

    # === 可兒 ===
    "conv_a07":                                "2026-05-08T21:18:00",  # brother_fake_smile, mid-week
    "sim_saga_a_keer__class_remark":           "2026-05-19T21:43:00",  # classmate said yesterday

    # === 大伯 ===
    "conv_a09":                                "2026-04-30T15:32:00",  # earlier, admitting plan
    "sim_saga_a_uncle__brother_health_scare":  "2026-05-17T15:18:00",  # next day after report

    # === Rachel ===
    "conv_a04":                                       "2026-05-06T22:54:00",  # anonymous_essay_followup
    "sim_saga_a_rachel__study_room_alone":            "2026-05-14T22:18:00",  # same family gathering night
    "sim_saga_a_rachel__father_board_meeting":        "2026-05-19T22:48:00",  # board meeting same day

    # === 沈又 ===
    "conv_a05":                                       "2026-05-11T02:36:00",  # 段考被處理, late night
    "sim_saga_a_shen_you__mom_announces_giis":        "2026-05-19T02:14:00",  # mom announced at lunch, came at night

    # === 沈媽 ===
    "conv_a06":                                       "2026-05-12T16:42:00",  # cried after lunch with Michael 媽
    "sim_saga_a_shen_mom__husband_separation_proposal": "2026-05-18T16:28:00",  # day after husband proposed

    # === Alan 老師 ===
    "conv_a08":                                       "2026-05-08T18:14:00",  # cognitive_load
    "sim_saga_a_alan_teacher__jieni_offer":           "2026-05-15T17:48:00",  # Wednesday, offer due Friday
    "sim_saga_a_alan_teacher__rachel_corridor":       "2026-05-19T18:22:00",  # Rachel came today after school
}


def backfill_synthetic_dataset() -> int:
    """Backfill conv_a01..a09 in synthetic_dataset.json."""
    if not SD_PATH.exists():
        return 0
    sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
    updated = 0
    for c in sd.get("conversations", []):
        cid = c.get("id")
        if cid in OCCURRED_AT_MAP:
            c["occurred_at"] = OCCURRED_AT_MAP[cid]
            updated += 1
    SD_PATH.write_text(json.dumps(sd, ensure_ascii=False, indent=2), encoding="utf-8")
    return updated


def backfill_generated() -> int:
    """Backfill sim_*.json in generated_conversations/."""
    if not GEN_DIR.exists():
        return 0
    updated = 0
    for f in sorted(GEN_DIR.glob("sim_*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        cid = data.get("id")
        if cid in OCCURRED_AT_MAP:
            data["occurred_at"] = OCCURRED_AT_MAP[cid]
            f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            updated += 1
    return updated


def backfill_index() -> int:
    """Update index.json with occurred_at too."""
    index_path = GEN_DIR / "index.json"
    if not index_path.exists():
        return 0
    index = json.loads(index_path.read_text(encoding="utf-8"))
    updated = 0
    for c in index.get("conversations", []):
        cid = c.get("id")
        if cid in OCCURRED_AT_MAP:
            c["occurred_at"] = OCCURRED_AT_MAP[cid]
            updated += 1
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return updated


def main() -> int:
    print("📅 Backfilling occurred_at fields...")
    sd_count = backfill_synthetic_dataset()
    gen_count = backfill_generated()
    idx_count = backfill_index()
    print(f"   ✅ synthetic_dataset.json: {sd_count} conversations updated")
    print(f"   ✅ generated_conversations/*.json: {gen_count} files updated")
    print(f"   ✅ index.json: {idx_count} entries updated")

    # Diagnostics: 列出 map 裡但找不到對應檔案的
    found_ids: set[str] = set()
    if SD_PATH.exists():
        sd = json.loads(SD_PATH.read_text(encoding="utf-8"))
        found_ids.update(c.get("id", "") for c in sd.get("conversations", []))
    if GEN_DIR.exists():
        for f in GEN_DIR.glob("sim_*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            found_ids.add(data.get("id", ""))

    missing_in_map = found_ids - set(OCCURRED_AT_MAP.keys())
    map_not_found = set(OCCURRED_AT_MAP.keys()) - found_ids
    if missing_in_map:
        print(f"\n   ⚠️  在檔案裡有但 map 沒涵蓋的（需手動加 timestamp）：")
        for cid in sorted(missing_in_map):
            print(f"      - {cid}")
    if map_not_found:
        print(f"\n   ℹ️  Map 裡有但找不到對應檔案的（可忽略）：")
        for cid in sorted(map_not_found):
            print(f"      - {cid}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
