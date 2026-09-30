from typing import Any


def run_pipeline(config: dict[str, Any]) -> dict[str, Any]:
    """Pipeline placeholder that returns basic run metadata."""
    return {"status": "ok", "config_keys": sorted(config.keys())}
