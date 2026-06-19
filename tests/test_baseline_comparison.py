"""Baseline comparison heuristic tests."""

from __future__ import annotations

from scripts import run_baseline_comparison


def test_conditional_reviewer_language_is_not_shallow_over_escalation():
    metrics = run_baseline_comparison._escalation_metrics(
        "Escalate to the assigned reviewer if risk increases.",
        "shallow",
    )

    assert metrics["over_escalation_flag"] is False
    assert metrics["under_escalation_flag"] is False


def test_high_severity_language_is_shallow_over_escalation():
    metrics = run_baseline_comparison._escalation_metrics(
        "Urgent crisis intervention is required.",
        "shallow",
    )

    assert metrics["over_escalation_flag"] is True


def test_deep_cases_still_expect_some_review_or_escalation_language():
    no_review = run_baseline_comparison._escalation_metrics(
        "Offer low-pressure classroom support.",
        "deep",
    )
    with_review = run_baseline_comparison._escalation_metrics(
        "Escalate to the assigned reviewer if risk increases.",
        "deep",
    )

    assert no_review["under_escalation_flag"] is True
    assert with_review["under_escalation_flag"] is False
