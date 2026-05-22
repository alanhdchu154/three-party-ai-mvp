"""CLI helper for adding a reviewer note without hand-writing JSON."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import reviewer_workflow


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-type", required=True, choices=sorted(reviewer_workflow.ARTIFACT_TYPES))
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--verdict", required=True, choices=sorted(reviewer_workflow.VERDICTS))
    parser.add_argument("--confidence", default="medium", choices=sorted(reviewer_workflow.CONFIDENCE_LEVELS))
    parser.add_argument("--source-path", default="")
    parser.add_argument("--comment", default="")
    parser.add_argument("--evidence-ref", action="append", default=[])
    parser.add_argument("--privacy-concern", action="append", default=[])
    parser.add_argument("--action-item", action="append", default=[])
    args = parser.parse_args()

    note = reviewer_workflow.build_review_note(
        artifact_type=args.artifact_type,
        artifact_id=args.artifact_id,
        reviewer=args.reviewer,
        verdict=args.verdict,
        confidence=args.confidence,
        source_path=args.source_path,
        comments=args.comment,
        evidence_ref_ids=args.evidence_ref,
        privacy_concerns=args.privacy_concern,
        action_items=args.action_item,
    )
    path = reviewer_workflow.save_review_note(note)
    print(f"Saved reviewer note: {path}")


if __name__ == "__main__":
    main()

