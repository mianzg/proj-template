"""Example entry point. Run from the project root:

    python src/run_example.py --config example_experiment

Since src/ isn't packaged, this puts the project root (not src/ itself) on
sys.path and imports as `src.config` — the same convention used in notebooks
(see notebooks/_bootstrap.py). Keeping one convention everywhere means code
moves between scripts and notebooks without changing its imports.
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import load_config  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Name of config in config/, no .yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    print(f"Running experiment: {cfg['experiment_name']}")
    # ... call into other functions in src/ here ...


if __name__ == "__main__":
    main()
