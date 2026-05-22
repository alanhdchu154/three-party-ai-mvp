"""UI mode separation tests."""

from __future__ import annotations

import app


def test_demo_mode_hides_raw_conversations_by_default(monkeypatch):
    monkeypatch.delenv("APP_MODE", raising=False)
    monkeypatch.delenv("SHOW_RAW_CONVERSATIONS", raising=False)
    monkeypatch.delenv("UMI_DEV_MODE", raising=False)

    assert app._app_mode() == "demo"
    assert app._raw_conversation_view_enabled() is False


def test_dev_mode_requires_explicit_raw_flag(monkeypatch):
    monkeypatch.setenv("APP_MODE", "dev")
    monkeypatch.delenv("SHOW_RAW_CONVERSATIONS", raising=False)
    monkeypatch.delenv("UMI_DEV_MODE", raising=False)

    assert app._app_mode() == "dev"
    assert app._raw_conversation_view_enabled() is False

    monkeypatch.setenv("SHOW_RAW_CONVERSATIONS", "1")
    assert app._raw_conversation_view_enabled() is True


def test_pilot_mode_never_uses_raw_flag(monkeypatch):
    monkeypatch.setenv("APP_MODE", "pilot")
    monkeypatch.setenv("SHOW_RAW_CONVERSATIONS", "1")
    monkeypatch.delenv("UMI_DEV_MODE", raising=False)

    assert app._app_mode() == "pilot"
    assert app._raw_conversation_view_enabled() is False


def test_source_label_marks_synthetic_data():
    assert app._source_label("llm_generated") == "Synthetic benchmark data"
    assert app._source_label("pilot_real_anonymized") == "Pilot anonymized data"
