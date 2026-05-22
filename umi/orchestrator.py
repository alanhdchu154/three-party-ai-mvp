#!/usr/bin/env python3
"""Umi orchestrator for Codex + Claude Code course-pipeline work.

Umi is intentionally small in this MVP:
- read-only worker prompts by default
- no upload permission unless --upload is set
- no write permission unless --write is set
- markdown reports saved under umi/reports/
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "umi" / "reports"
DEFAULT_WORKLOAD = REPO_ROOT / "umi" / "workload.md"

UPLOAD_TERMS = (
    "youtube",
    "youtu.be",
    "upload",
    "publish",
    "post ",
    "上傳",
    "發布",
    "發佈",
)

@dataclass
class WorkerResult:
    name: str
    command: list[str]
    returncode: int | None
    stdout: str
    stderr: str
    skipped_reason: str | None = None


def now_slug() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def slugify(value: str, fallback: str = "umi-task") -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned[:80] or fallback


def extract_task_id(task_text: str, fallback: str) -> str:
    lines = task_text.splitlines()
    for index, line in enumerate(lines):
        if line.strip().lower() == "### task id":
            for candidate in lines[index + 1 :]:
                value = candidate.strip()
                if value:
                    return value
    return fallback


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_claude_env() -> dict[str, str]:
    env = os.environ.copy()
    if env.get("CLAUDE_CODE_OAUTH_TOKEN"):
        return env
    if sys.platform != "darwin" or shutil.which("security") is None:
        return env

    completed = subprocess.run(
        [
            "security",
            "find-generic-password",
            "-w",
            "-a",
            env.get("USER", ""),
            "-s",
            "claude-code-oauth-token",
        ],
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    token = completed.stdout.strip()
    if completed.returncode == 0 and token:
        env["CLAUDE_CODE_OAUTH_TOKEN"] = token
    return env


def run_command(
    command: list[str],
    timeout_seconds: int,
    display_command: list[str] | None = None,
    env: dict[str, str] | None = None,
) -> WorkerResult:
    name = command[0]
    safe_command = display_command or command
    if shutil.which(name) is None:
        return WorkerResult(
            name=name,
            command=safe_command,
            returncode=None,
            stdout="",
            stderr="",
            skipped_reason=f"`{name}` was not found on PATH.",
        )

    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        return WorkerResult(
            name=name,
            command=command,
            returncode=None,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            skipped_reason=f"`{name}` timed out after {timeout_seconds} seconds.",
        )

    return WorkerResult(
        name=name,
        command=safe_command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def safe_git_capture(args: list[str]) -> str:
    if shutil.which("git") is None:
        return "`git` was not found on PATH."
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    output = completed.stdout.strip()
    error = completed.stderr.strip()
    if completed.returncode != 0:
        return error or output or f"git {' '.join(args)} failed with code {completed.returncode}."
    return output or "(no output)"


def has_upload_intent(text: str) -> bool:
    for raw_line in text.splitlines():
        line = raw_line.lower()
        if any(guard in line for guard in ("do not", "don't", "no ", "不要", "不准", "禁止")):
            continue
        if any(term in line for term in UPLOAD_TERMS):
            return True
    return False


def build_claude_prompt(task_text: str, allow_write: bool, allow_upload: bool) -> str:
    write_policy = (
        "You may write only the output files explicitly listed in the workload. "
        "Do not modify pipeline scripts or final lesson files."
        if allow_write
        else "Read-only mode: do not modify files. Put draft content and notes in stdout."
    )
    upload_policy = (
        "Upload/publishing actions are allowed only if the workload explicitly asks for them."
        if allow_upload
        else "Do not upload, publish, post, or call YouTube/external delivery tools."
    )

    return f"""You are Claude Code working as Umi's focused worker for Alan's three-party AI education coordination repo.

Role:
- Help with read-only repo review, safety auditing, synthetic benchmark inspection, pilot-readiness notes, or narrow artifact-generation tasks.
- Preserve the repo's core purpose: three-party AI education coordination, synthetic safety benchmark, and controlled pilot readiness.
- Keep the privacy wall central: do not expose raw student/private party disclosures across audiences.
- Surface assumptions and uncertain points.

Safety:
- {write_policy}
- {upload_policy}
- Do not call paid APIs.
- Do not delete files.
- Do not overwrite existing final files.
- Do not expose private student raw conversations.

Workload:
{task_text}

Return:
1. Content draft or inspection findings.
2. Notes, assumptions, and uncertain points.
3. Any blockers for Codex review.
"""


def build_codex_prompt(task_text: str, claude_stdout: str, allow_write: bool, allow_upload: bool) -> str:
    write_policy = (
        "You may propose file edits only if the workload explicitly asks for integration."
        if allow_write
        else "Read-only review mode: do not modify files. Provide review findings only."
    )
    upload_policy = (
        "Upload/publishing actions may be discussed only if explicitly requested."
        if allow_upload
        else "Do not upload, publish, post, or call YouTube/external delivery tools."
    )

    return f"""You are Codex working as Umi's engineering/review worker for Alan's three-party AI education coordination repo.

Role:
- Review Claude Code's output for repo alignment, safety, privacy-wall risks, implementation accuracy, and integration risk.
- Keep Codex as the engineering owner.
- Be concrete and practical.

Safety:
- {write_policy}
- {upload_policy}
- Do not call paid APIs.
- Do not delete files.
- Do not overwrite final lesson files without Alan approval.

Original workload:
{task_text}

Claude Code stdout:
{claude_stdout[:20000]}

Return:
1. Accuracy and alignment review.
2. Tone/pacing edits or concerns.
3. Integration checklist.
4. Recommended next action for Alan/Codex.
"""


def fenced(value: str, language: str = "text") -> str:
    if not value:
        value = "(empty)"
    return f"```{language}\n{value.rstrip()}\n```"


def format_worker_result(result: WorkerResult) -> str:
    command_text = " ".join(result.command)
    if result.skipped_reason:
        status = f"Skipped: {result.skipped_reason}"
    else:
        status = f"Exit code: {result.returncode}"
    return f"""### {result.name}

Command:
{fenced(command_text)}

Status:
{status}

Stdout:
{fenced(result.stdout)}

Stderr:
{fenced(result.stderr)}
"""


def write_report(
    task_label: str,
    task_text: str,
    allow_write: bool,
    allow_upload: bool,
    blocked_reason: str | None,
    claude_result: WorkerResult | None,
    codex_result: WorkerResult | None,
) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    task_id = extract_task_id(task_text, task_label)
    report_path = REPORT_DIR / f"{now_slug()}-{slugify(task_id)}.md"
    git_status = safe_git_capture(["status", "--short"])
    git_diff_summary = safe_git_capture(["diff", "--stat"])

    claude_section = (
        format_worker_result(claude_result)
        if claude_result
        else "Claude Code was not run."
    )
    codex_section = (
        format_worker_result(codex_result)
        if codex_result
        else "Codex worker was not run."
    )
    blocked_section = blocked_reason or "(none)"

    report = f"""# Umi Task Report

## Umi Summary Template

- Task: {task_id}
- Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}
- Repo: {REPO_ROOT}
- Worker write permission: {allow_write}
- Upload permission: {allow_upload}
- Safety block: {blocked_section}

### Next Action

- Alan/Codex should review Claude findings and Codex findings before changing final lesson files.
- If content should be integrated, rerun or continue with explicit `--write` and Alan approval.

## Workload

{task_text}

## Claude Findings

{claude_section}

## Codex Findings

{codex_section}

## Git Status

{fenced(git_status)}

## Git Diff Summary

{fenced(git_diff_summary)}
"""
    report_path.write_text(report, encoding="utf-8")
    return report_path


def load_task_from_args(args: argparse.Namespace) -> tuple[str, str]:
    if args.command == "run":
        workload_path = Path(args.workload)
        if not workload_path.is_absolute():
            workload_path = REPO_ROOT / workload_path
        task_text = read_text(workload_path)
        return workload_path.stem, task_text

    direct_task = " ".join(args.task).strip()
    if not direct_task:
        if DEFAULT_WORKLOAD.exists():
            return DEFAULT_WORKLOAD.stem, read_text(DEFAULT_WORKLOAD)
        raise SystemExit("No task provided and workload.md does not exist.")
    return direct_task, direct_task


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Umi orchestrator for Claude Code and Codex course-pipeline work."
    )
    parser.add_argument("command", nargs="?", help='Use "run" for workload files, or pass a direct task.')
    parser.add_argument("task", nargs="*", help="Direct task text when not using run.")
    parser.add_argument("--write", action="store_true", help="Allow worker prompts to request file modifications.")
    parser.add_argument("--upload", action="store_true", help="Allow worker prompts to request upload/publishing actions.")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout per worker command in seconds.")
    parser.add_argument("--skip-codex", action="store_true", help="Run Claude only.")
    parser.add_argument("--skip-claude", action="store_true", help="Run Codex only.")
    parser.add_argument("--dry-run", action="store_true", help="Build prompts and report without calling worker CLIs.")
    parser.add_argument(
        "--workload",
        default="workload.md",
        help="Workload markdown path when command is run.",
    )

    args = parser.parse_args(argv)
    if args.command == "run":
        if args.task:
            args.workload = args.task[0]
            args.task = args.task[1:]
        return args

    if args.command:
        args.task = [args.command, *args.task]
    args.command = "direct"
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    task_label, task_text = load_task_from_args(args)

    blocked_reason = None
    if has_upload_intent(task_text) and not args.upload:
        blocked_reason = "Workload appears to mention upload/publishing, but --upload was not provided."

    claude_result: WorkerResult | None = None
    codex_result: WorkerResult | None = None

    if blocked_reason:
        report_path = write_report(
            task_label,
            task_text,
            args.write,
            args.upload,
            blocked_reason,
            claude_result,
            codex_result,
        )
        print(f"Umi blocked the task for safety: {blocked_reason}")
        print(f"Report saved to {report_path}")
        return 2

    claude_prompt = build_claude_prompt(task_text, args.write, args.upload)
    if not args.skip_claude:
        if args.dry_run:
            claude_result = WorkerResult(
                name="claude",
                command=["claude", "-p", "<prompt>"],
                returncode=0,
                stdout=claude_prompt,
                stderr="",
                skipped_reason="Dry run: Claude Code was not invoked.",
            )
        else:
            claude_command = ["claude", "-p", claude_prompt]
            claude_display = ["claude", "-p", "<content-worker prompt>"]
            if args.write:
                claude_command = [
                    "claude",
                    "--permission-mode",
                    "acceptEdits",
                    "-p",
                    claude_prompt,
                ]
                claude_display = [
                    "claude",
                    "--permission-mode",
                    "acceptEdits",
                    "-p",
                    "<content-worker prompt>",
                ]
            claude_result = run_command(
                claude_command,
                args.timeout,
                display_command=claude_display,
                env=load_claude_env(),
            )

    claude_stdout = claude_result.stdout if claude_result else ""
    codex_prompt = build_codex_prompt(task_text, claude_stdout, args.write, args.upload)
    if not args.skip_codex:
        if args.dry_run:
            codex_result = WorkerResult(
                name="codex",
                command=["codex", "exec", "<prompt>"],
                returncode=0,
                stdout=codex_prompt,
                stderr="",
                skipped_reason="Dry run: Codex was not invoked.",
            )
        else:
            codex_result = run_command(
                ["codex", "exec", codex_prompt],
                args.timeout,
                display_command=["codex", "exec", "<engineering-worker prompt>"],
            )

    report_path = write_report(
        task_label,
        task_text,
        args.write,
        args.upload,
        None,
        claude_result,
        codex_result,
    )
    print(f"Umi report saved to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
