"""Generate trajectory reports from existing analysis artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import trajectory_model


def main() -> None:
    models = trajectory_model.build_trajectory_models()
    paths = trajectory_model.generate_trajectory_reports(models)
    print(f"Generated {len(paths)} trajectory reports:")
    for path in paths:
        print(f"- {path}")


if __name__ == "__main__":
    main()

