"""Audit log tests."""

from __future__ import annotations

from src import audit_log


def test_append_and_load_events(tmp_path):
    path = tmp_path / "run" / "audit_log.jsonl"

    audit_log.append_event(path, event_type="started", payload={"student_id": "michael"})
    audit_log.append_event(path, event_type="completed", payload={"ok": True})

    events = audit_log.load_events(path)

    assert [event["event_type"] for event in events] == ["started", "completed"]
    assert events[0]["payload"]["student_id"] == "michael"
    assert events[1]["payload"]["ok"] is True
    assert all(event["timestamp"].endswith("Z") for event in events)


def test_load_missing_audit_log_returns_empty_list(tmp_path):
    assert audit_log.load_events(tmp_path / "missing.jsonl") == []
