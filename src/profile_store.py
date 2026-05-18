"""學生 profile 的本機 JSON 儲存。

設計選擇：
- 每個學生一個 JSON 檔，檔名 = student_id
- 寫入時 atomic（先寫 tmp、再 rename），避免半寫壞檔
- 不存對話原話，只存 profile（隱私牆）
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

PROFILES_DIR = Path(__file__).resolve().parent.parent / "data" / "student_profiles"


def _safe_id(student_id: str) -> str:
    """避免 path traversal / 特殊字元。"""
    cleaned = re.sub(r"[^A-Za-z0-9_\-]", "_", student_id.strip())
    if not cleaned:
        raise ValueError("student_id 不能為空。")
    return cleaned


def _path_for(student_id: str) -> Path:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    return PROFILES_DIR / f"{_safe_id(student_id)}.json"


def list_profiles() -> list[str]:
    """列出所有 profile 的 student_id（不含副檔名）。"""
    if not PROFILES_DIR.exists():
        return []
    return sorted(p.stem for p in PROFILES_DIR.glob("*.json"))


def load_profile(student_id: str) -> dict[str, Any] | None:
    """讀取 profile。沒有則回 None。"""
    path = _path_for(student_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # 壞檔不要 crash，給上層決定怎麼辦
        return None


def save_profile(student_id: str, profile: dict[str, Any]) -> Path:
    """寫入 profile（atomic）。會自動加上 updated_at。"""
    path = _path_for(student_id)
    payload = {
        **profile,
        "student_id": _safe_id(student_id),
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    os.replace(tmp, path)
    return path


def delete_profile(student_id: str) -> bool:
    path = _path_for(student_id)
    if path.exists():
        path.unlink()
        return True
    return False
