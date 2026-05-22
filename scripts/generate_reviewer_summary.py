"""Generate reviewer calibration summary from JSON reviewer notes."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import reviewer_workflow


def main() -> None:
    path = reviewer_workflow.generate_reviewer_summary()
    print(f"Generated reviewer summary: {path}")


if __name__ == "__main__":
    main()

