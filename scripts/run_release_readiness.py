"""Run the deterministic Evidence v1 release-readiness gate.

This script does not call LLMs and does not generate new synthetic data. It
reruns the current benchmark checks, validates the expected v1 metrics, scans
public docs for positive overclaims, and writes a markdown/json release report.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REPORT_JSON = ROOT / "umi" / "reports" / "release-readiness-latest.json"
REPORT_MD = ROOT / "umi" / "reports" / "release-readiness-latest.md"
BASELINE_JSON = ROOT / "umi" / "reports" / "baseline-comparison-latest.json"
LEAK_JSON = ROOT / "umi" / "reports" / "audience-report-leak-audit-latest.json"
SEMANTIC_TRACE_JSON = ROOT / "umi" / "reports" / "semantic-trace-audit-latest.json"
RELATIONSHIP_LEAK_JSON = ROOT / "umi" / "reports" / "relationship-leak-audit-latest.json"
RUNTIME_TRACE_JSON = ROOT / "umi" / "reports" / "runtime-trace-privacy-latest.json"

EXPECTED_CORPUS = {
    "n_conversations": 348,
    "depth_counts": {"deep": 85, "shallow": 142, "medium": 121},
}
EXPECTED_BASELINE_SAMPLE_SIZE = 11
MIN_REVIEWER_NOTES = 22
MIN_REVIEWED_ARTIFACTS = 22
MIN_BASELINE_ARTIFACTS = 12
MIN_AUDIENCE_REPORT_ARTIFACTS = 3
MIN_SECOND_REVIEWER_ARTIFACTS = 15
EXPECTED_SEMANTIC_TRACE_SURFACES = 22
EXPECTED_RELATIONSHIP_LEAK_REPORTS = 18
EXPECTED_RUNTIME_TRACE_SURFACES = 51

PUBLIC_CLAIM_FILES = [
    ROOT / "README.md",
    ROOT / "WORKLOG.md",
    ROOT / "docs" / "startup_thesis.md",
    ROOT / "docs" / "external_reviewer_packet.md",
    ROOT / "docs" / "external_testing_instructions.md",
    ROOT / "docs" / "external_reviewer_outreach.md",
    ROOT / "docs" / "external_review_agent_dry_run_2026-06-19.md",
    ROOT / "docs" / "simulated_external_panel_review_2026-06-19.md",
    ROOT / "docs" / "paper_draft.md",
    ROOT / "docs" / "benchmark_datasheet.md",
    ROOT / "docs" / "github_publication_checklist.md",
    ROOT / "docs" / "reviewer_gate_checklist.md",
    ROOT / "docs" / "roadmap.md",
    ROOT / "umi" / "workload.md",
]

OVERCLAIM_PATTERNS = [
    re.compile(r"\bvalidated\b.{0,50}\b(real[- ]?students?|minors?|schools?)\b", re.IGNORECASE),
    re.compile(r"\b(real[- ]?student|minor|school)\b.{0,50}\bvalidated\b", re.IGNORECASE),
    re.compile(r"\bproven\b.{0,50}\b(real[- ]?students?|minors?|schools?)\b", re.IGNORECASE),
    re.compile(r"\bsafe for minors\b", re.IGNORECASE),
    re.compile(r"\bdeployment[- ]ready\b", re.IGNORECASE),
    re.compile(r"\bdeployment readiness\b", re.IGNORECASE),
    re.compile(r"\bclinical validity\b", re.IGNORECASE),
    re.compile(r"\boutcome improvement\b", re.IGNORECASE),
]

SECRET_PATTERNS = [
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"\bsk-(?:ant-|proj-)?[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[0-9A-Za-z_]{20,}\b"),
    re.compile(r"\bGROQ_API_KEY\s*=\s*[^#\s<][^\s]+"),
    re.compile(r"\bGEMINI_API_KEY\s*=\s*[^#\s<][^\s]+"),
    re.compile(r"\bANTHROPIC_API_KEY\s*=\s*[^#\s<][^\s]+"),
    re.compile(r"\bOPENAI_API_KEY\s*=\s*[^#\s<][^\s]+"),
    re.compile(r"\bDEEPSEEK_API_KEY\s*=\s*[^#\s<][^\s]+"),
]

SECRET_ALLOWLIST_RE = re.compile(
    r"(\.example|example|placeholder|your-|<|\.\.\.|sk-ant-\.\.\.|sk-\.\.\.)",
    re.IGNORECASE,
)

ALLOWING_CONTEXT_RE = re.compile(
    r"(\b(no|not|cannot|can't|do not|does not|without|not yet|not a|unsafe wording|"
    r"non-use|non-uses|do not use|to claim|limitations?|known gaps|claim boundary|"
    r"what is not proven)\b|不要|不能|不可|不應|不是|不會|不宣稱|誤認|未)",
    re.IGNORECASE,
)


@dataclass
class CommandResult:
    name: str
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "command": self.command,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


def _venv_python() -> str:
    candidate = ROOT / ".venv" / "bin" / "python"
    return str(candidate) if candidate.exists() else sys.executable


def run_command(name: str, command: list[str]) -> CommandResult:
    proc = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return CommandResult(
        name=name,
        command=command,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def command_plan() -> list[tuple[str, list[str]]]:
    py = _venv_python()
    return [
        ("corpus_audit", ["python3", "scripts/audit_conversation_quality.py", "--json"]),
        ("baseline_comparison", [py, "scripts/run_baseline_comparison.py"]),
        ("reviewer_summary", [py, "scripts/generate_reviewer_summary.py"]),
        (
            "audience_report_leak_audit",
            [
                py,
                "scripts/audit_audience_report_leaks.py",
                "--json",
                "umi/reports/audience-report-leak-audit-latest.json",
            ],
        ),
        ("semantic_trace_audit", [py, "scripts/run_semantic_trace_audit.py"]),
        ("relationship_leak_audit", [py, "scripts/run_relationship_leak_audit.py"]),
        ("runtime_trace_privacy_audit", [py, "scripts/run_runtime_trace_privacy_audit.py"]),
        ("pytest", [py, "-m", "pytest", "-q"]),
    ]


def scan_claim_boundaries(paths: list[Path] | None = None) -> list[dict[str, Any]]:
    """Return positive claim-boundary overclaim hits in public docs."""
    hits: list[dict[str, Any]] = []
    for path in paths or PUBLIC_CLAIM_FILES:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if not any(pattern.search(line) for pattern in OVERCLAIM_PATTERNS):
                continue
            context_lines = lines[max(0, index - 5) : index + 1]
            context = " ".join(context_lines)
            if ALLOWING_CONTEXT_RE.search(context):
                continue
            hits.append(
                {
                    "path": _display_path(path),
                    "line": index + 1,
                    "text": line.strip(),
                }
            )
    return hits


def scan_secret_like_values(paths: list[Path] | None = None) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for path in paths or _git_public_files():
        if not path.exists() or path.is_dir() or path.stat().st_size > 1_000_000:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines):
            if SECRET_ALLOWLIST_RE.search(line):
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    hits.append(
                        {
                            "path": _display_path(path),
                            "line": index + 1,
                            "pattern": pattern.pattern,
                        }
                    )
                    break
    return hits


def _git_public_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [ROOT / line for line in proc.stdout.splitlines() if line]


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_corpus_metrics(command: CommandResult) -> dict[str, Any]:
    if not command.ok:
        return {}
    try:
        payload = json.loads(command.stdout)
    except json.JSONDecodeError:
        return {}
    return {
        "n_conversations": payload.get("n_conversations"),
        "depth_counts": payload.get("depth_counts", {}),
        "turns": payload.get("turns", {}),
        "warnings": payload.get("warnings", []),
    }


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _reviewer_summary_metrics() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    from src import reviewer_workflow

    summary = reviewer_workflow.summarize_reviews()
    artifacts = summary.get("artifacts", {})
    baseline_artifacts = [
        artifact for artifact in artifacts.values() if artifact.get("artifact_type") == "baseline_comparison"
    ]
    audience_artifacts = [
        artifact for artifact in artifacts.values() if artifact.get("artifact_type") == "audience_report"
    ]
    second_reviewer_artifacts = [
        artifact
        for artifact in artifacts.values()
        if "ReviewerB" in artifact.get("reviewers", [])
        and artifact.get("artifact_type") in {"baseline_comparison", "audience_report"}
    ]
    verdict_counts: dict[str, int] = {}
    for artifact in artifacts.values():
        for verdict, count in artifact.get("verdict_counts", {}).items():
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + count

    return {
        "n_notes": summary.get("n_notes", 0),
        "n_artifacts_reviewed": summary.get("n_artifacts_reviewed", 0),
        "baseline_artifacts": len(baseline_artifacts),
        "audience_report_artifacts": len(audience_artifacts),
        "second_reviewer_artifacts": len(second_reviewer_artifacts),
        "verdict_counts": verdict_counts,
    }


def collect_metrics(results: list[CommandResult]) -> dict[str, Any]:
    by_name = {result.name: result for result in results}
    baseline = _load_json(BASELINE_JSON, {})
    leak_results = _load_json(LEAK_JSON, [])
    semantic_trace = _load_json(SEMANTIC_TRACE_JSON, {})
    relationship_leak = _load_json(RELATIONSHIP_LEAK_JSON, {})
    runtime_trace = _load_json(RUNTIME_TRACE_JSON, {})
    leak_failures = [item for item in leak_results if item.get("status") != "PASS"]
    return {
        "corpus": _load_corpus_metrics(by_name["corpus_audit"]),
        "baseline": {
            "sample_size": baseline.get("sample_size"),
            "totals": baseline.get("totals", {}),
        },
        "leak_audit": {
            "reports_checked": len(leak_results) if isinstance(leak_results, list) else 0,
            "failures": len(leak_failures) if isinstance(leak_results, list) else None,
        },
        "semantic_trace_audit": {
            "surfaces_checked": semantic_trace.get("surfaces_checked", 0),
            "failures": semantic_trace.get("failures", 0),
        },
        "relationship_leak_audit": {
            "reports_checked": relationship_leak.get("reports_checked", 0),
            "failures": relationship_leak.get("failures", 0),
        },
        "runtime_trace_privacy_audit": {
            "surfaces_checked": runtime_trace.get("surfaces_checked", 0),
            "failures": runtime_trace.get("failures", 0),
            "surface_counts": runtime_trace.get("surface_counts", {}),
        },
        "reviewer_summary": _reviewer_summary_metrics(),
    }


def evaluate_readiness(
    *,
    command_results: list[CommandResult],
    metrics: dict[str, Any],
    claim_hits: list[dict[str, Any]],
    secret_hits: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    failures: list[str] = []
    for result in command_results:
        if not result.ok:
            failures.append(f"command_failed:{result.name}")

    corpus = metrics.get("corpus", {})
    if corpus.get("n_conversations") != EXPECTED_CORPUS["n_conversations"]:
        failures.append("corpus_count_changed")
    if corpus.get("depth_counts") != EXPECTED_CORPUS["depth_counts"]:
        failures.append("corpus_depth_distribution_changed")

    baseline = metrics.get("baseline", {})
    privacy_wall = baseline.get("totals", {}).get("privacy_wall_pipeline", {})
    if baseline.get("sample_size") != EXPECTED_BASELINE_SAMPLE_SIZE:
        failures.append("baseline_sample_size_changed")
    for key in (
        "raw_quote_leaks",
        "private_chunk_leaks",
        "private_key_or_path_hits",
        "reconstructability_risk_cases",
        "over_escalation_flags",
        "under_escalation_flags",
        "recommendation_without_evidence_flags",
        "missing_audience_report_cases",
    ):
        if privacy_wall.get(key) != 0:
            failures.append(f"privacy_wall_{key}_nonzero")

    leak_audit = metrics.get("leak_audit", {})
    if leak_audit.get("failures") != 0:
        failures.append("audience_report_leak_failures")

    semantic_trace = metrics.get("semantic_trace_audit", {})
    if semantic_trace.get("surfaces_checked") != EXPECTED_SEMANTIC_TRACE_SURFACES:
        failures.append("semantic_trace_surface_count_changed")
    if semantic_trace.get("failures") != 0:
        failures.append("semantic_trace_failures")

    relationship_leak = metrics.get("relationship_leak_audit", {})
    if relationship_leak.get("reports_checked") != EXPECTED_RELATIONSHIP_LEAK_REPORTS:
        failures.append("relationship_leak_report_count_changed")
    if relationship_leak.get("failures") != 0:
        failures.append("relationship_context_leak_failures")

    runtime_trace = metrics.get("runtime_trace_privacy_audit", {})
    if runtime_trace.get("surfaces_checked") != EXPECTED_RUNTIME_TRACE_SURFACES:
        failures.append("runtime_trace_surface_count_changed")
    if runtime_trace.get("failures") != 0:
        failures.append("runtime_trace_privacy_failures")

    reviewer = metrics.get("reviewer_summary", {})
    if reviewer.get("n_notes", 0) < MIN_REVIEWER_NOTES:
        failures.append("reviewer_note_coverage_low")
    if reviewer.get("n_artifacts_reviewed", 0) < MIN_REVIEWED_ARTIFACTS:
        failures.append("reviewer_artifact_coverage_low")
    if reviewer.get("baseline_artifacts", 0) < MIN_BASELINE_ARTIFACTS:
        failures.append("reviewer_baseline_artifact_coverage_low")
    if reviewer.get("audience_report_artifacts", 0) < MIN_AUDIENCE_REPORT_ARTIFACTS:
        failures.append("reviewer_audience_artifact_coverage_low")
    if reviewer.get("second_reviewer_artifacts", 0) < MIN_SECOND_REVIEWER_ARTIFACTS:
        failures.append("second_reviewer_coverage_low")

    if claim_hits:
        failures.append("positive_public_overclaim_detected")
    if secret_hits:
        failures.append("secret_like_value_detected")

    return {
        "status": "pass" if not failures else "fail",
        "failures": failures,
    }


def render_markdown(report: dict[str, Any]) -> str:
    status = report["readiness"]["status"].upper()
    metrics = report["metrics"]
    corpus = metrics["corpus"]
    baseline = metrics["baseline"]
    privacy_wall = baseline.get("totals", {}).get("privacy_wall_pipeline", {})
    raw_baseline = baseline.get("totals", {}).get("raw_coordinator_baseline", {})
    leak_audit = metrics["leak_audit"]
    semantic_trace = metrics["semantic_trace_audit"]
    relationship_leak = metrics["relationship_leak_audit"]
    runtime_trace = metrics["runtime_trace_privacy_audit"]
    reviewer = metrics["reviewer_summary"]
    command_rows = [
        f"| `{result['name']}` | `{result['returncode']}` | `{' '.join(result['command'])}` |"
        for result in report["commands"]
    ]
    failure_lines = report["readiness"]["failures"] or ["None."]
    claim_hits = report["claim_boundary"]["positive_overclaim_hits"]
    secret_hits = report["secret_scan"]["secret_like_hits"]

    lines = [
        "# Release Readiness Report",
        "",
        f"Status: `{status}`",
        f"Generated at: `{report['generated_at']}`",
        "",
        "> Evidence v1 is a synthetic-benchmark gate. Passing this report does not prove real-student validation, clinical validity, deployment readiness, or outcome improvement.",
        "",
        "## Commands",
        "",
        "| Check | Return code | Command |",
        "|---|---:|---|",
        *command_rows,
        "",
        "## Evidence Summary",
        "",
        f"- Corpus: `{corpus.get('n_conversations')}` conversations; depth counts `{corpus.get('depth_counts')}`.",
        f"- Baseline sample size: `{baseline.get('sample_size')}`.",
        f"- Raw coordinator reconstructability-risk cases: `{raw_baseline.get('reconstructability_risk_cases')}`.",
        f"- Privacy-wall reconstructability-risk cases: `{privacy_wall.get('reconstructability_risk_cases')}`.",
        f"- Privacy-wall over/under escalation flags: `{privacy_wall.get('over_escalation_flags')}` / `{privacy_wall.get('under_escalation_flags')}`.",
        f"- Privacy-wall unsupported recommendation flags: `{privacy_wall.get('recommendation_without_evidence_flags')}`.",
        f"- Audience report leak audit: `{leak_audit.get('reports_checked')}` checked / `{leak_audit.get('failures')}` failures.",
        f"- Semantic trace audit: `{semantic_trace.get('surfaces_checked')}` checked / `{semantic_trace.get('failures')}` failures.",
        f"- Relationship leak audit: `{relationship_leak.get('reports_checked')}` checked / `{relationship_leak.get('failures')}` failures.",
        f"- Runtime trace privacy audit: `{runtime_trace.get('surfaces_checked')}` checked / `{runtime_trace.get('failures')}` failures.",
        f"- Reviewer coverage: `{reviewer.get('n_notes')}` notes / `{reviewer.get('n_artifacts_reviewed')}` artifacts.",
        f"- Reviewer artifact mix: `{reviewer.get('baseline_artifacts')}` baseline / `{reviewer.get('audience_report_artifacts')}` audience-report artifacts.",
        f"- Second reviewer coverage: `{reviewer.get('second_reviewer_artifacts')}` baseline/audience artifacts.",
        f"- Reviewer verdict counts: `{reviewer.get('verdict_counts')}`.",
        "",
        "## Gate Failures",
        "",
        *[f"- {failure}" for failure in failure_lines],
        "",
        "## Claim Boundary Scan",
        "",
    ]
    if claim_hits:
        for hit in claim_hits:
            lines.append(f"- `{hit['path']}:{hit['line']}`: {hit['text']}")
    else:
        lines.append("- No positive public overclaim hits found.")
    lines.extend(["", "## Secret Scan", ""])
    if secret_hits:
        for hit in secret_hits:
            lines.append(f"- `{hit['path']}:{hit['line']}` matched `{hit['pattern']}`")
    else:
        lines.append("- No secret-like values found in git-visible files.")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This gate supports public synthetic-benchmark packaging only. It does not authorize real minor-data use, school deployment, clinical claims, or autonomous support workflows.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    results = [run_command(name, command) for name, command in command_plan()]
    metrics = collect_metrics(results)
    claim_hits = scan_claim_boundaries()
    secret_hits = scan_secret_like_values()
    readiness = evaluate_readiness(
        command_results=results,
        metrics=metrics,
        claim_hits=claim_hits,
        secret_hits=secret_hits,
    )
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "claim_boundary_statement": "Synthetic benchmark gate only. Not real-student validation, clinical validity, deployment readiness, or outcome proof.",
        "readiness": readiness,
        "metrics": metrics,
        "claim_boundary_scan_files": [str(path.relative_to(ROOT)) for path in PUBLIC_CLAIM_FILES if path.exists()],
        "claim_boundary": {
            "positive_overclaim_hits": claim_hits,
        },
        "secret_scan": {
            "secret_like_hits": secret_hits,
        },
        "commands": [result.as_dict() for result in results],
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    REPORT_MD.write_text(render_markdown(report), encoding="utf-8")

    print(f"Release readiness: {readiness['status'].upper()}")
    print(f"Report: {REPORT_MD}")
    if readiness["failures"]:
        print("Failures:")
        for failure in readiness["failures"]:
            print(f"- {failure}")
    return 0 if readiness["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
