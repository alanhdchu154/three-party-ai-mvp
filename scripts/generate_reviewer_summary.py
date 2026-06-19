"""Generate reviewer calibration and annotation summaries from JSON notes."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import reviewer_workflow


def main() -> None:
    calibration = reviewer_workflow.generate_reviewer_summary()
    annotation = reviewer_workflow.generate_reviewer_summary(
        filename="reviewer_annotation_summary.md",
        title="Reviewer Annotation Summary",
    )
    print(f"Generated reviewer calibration summary: {calibration}")
    print(f"Generated reviewer annotation summary: {annotation}")


if __name__ == "__main__":
    main()
