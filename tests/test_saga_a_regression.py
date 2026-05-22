"""Saga A non-LLM regression tests for safety/benchmark infrastructure."""

from __future__ import annotations

import json
from pathlib import Path

from src import abstraction, triage


ROOT = Path(__file__).resolve().parent.parent


def test_saga_a_reports_can_be_sanitized_for_demo_mode():
    report_path = ROOT / "data" / "analysis_reports" / "michael_analysis.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    analysis = report["analysis"]
    protected_terms = list(analysis.get("privacy_kept", [])) + ["Michael", "Rachel", "信託文件"]

    sanitized = abstraction.sanitize_for_privacy(analysis, protected_terms=protected_terms)
    rendered = json.dumps(sanitized, ensure_ascii=False)

    assert "信託文件" not in rendered
    assert "Michael" not in rendered
    assert "Rachel" not in rendered
    assert "privacy_kept" in sanitized


def test_saga_a_dimension_scores_drive_triage_without_llm(monkeypatch):
    def fake_complete_json(**kwargs):
        return {"escalate": False, "escalation_type": "none", "urgency": "low"}

    monkeypatch.setattr(triage.llm, "complete_json", fake_complete_json)
    result = triage.should_escalate({"student_id": "shen_you"})

    assert result["guardrail_applied"] is True
    assert result["escalate"] is True
    assert result["urgency"] in {"medium", "high", "critical"}
