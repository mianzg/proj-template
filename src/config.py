"""Central place to load .env and config/*.yaml so paths and settings
aren't scattered/hardcoded across notebooks and scripts."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


def data_root() -> Path:
    """Resolve the data directory, preferring DATA_ROOT from .env if set."""
    return Path(os.environ.get("DATA_ROOT", PROJECT_ROOT / "data"))


def load_config(name: str) -> dict:
    """Load a YAML config file from config/ by name, e.g. load_config('experiment1')."""
    path = PROJECT_ROOT / "config" / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No config found at {path}")
    with open(path) as f:
        return yaml.safe_load(f)


def random_seed() -> int:
    return int(os.environ.get("RANDOM_SEED", 42))
