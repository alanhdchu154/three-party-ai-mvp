"""Generate Analysis Layer v0.1 case summaries from existing artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import analysis_layer


def main() -> None:
    summaries = analysis_layer.build_case_summaries()
    paths = analysis_layer.generate_case_reports(summaries)
    print(f"Generated {len(paths)} case summaries:")
    for path in paths:
        print(f"- {path}")


if __name__ == "__main__":
    main()
