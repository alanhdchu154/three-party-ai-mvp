"""Run controlled internal pilot harness for one existing student case."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import pilot_harness


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--student", required=True, help="Student id, e.g. michael")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    path = pilot_harness.run_controlled_harness(args.student, run_id=args.run_id)
    print(f"Pilot harness run written to: {path}")


if __name__ == "__main__":
    main()

