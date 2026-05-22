"""Generate internal, parent-safe, and teacher-safe case report variants."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import report_variants


def main() -> None:
    paths = report_variants.generate_case_variant_reports()
    print(f"Generated {len(paths)} audience reports:")
    for path in paths:
        print(f"- {path}")


if __name__ == "__main__":
    main()

