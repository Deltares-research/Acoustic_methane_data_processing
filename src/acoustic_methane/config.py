from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load YAML configuration from disk."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
