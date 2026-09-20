import json
from pathlib import Path
from typing import Any

from .errors import ConfigurationError


def load_json_subset_yaml(path: Path) -> dict[str, Any]:
    """Load the engine's JSON-subset YAML documents without third-party dependencies."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigurationError(f"Unable to load configuration: {path}") from exc
    if not isinstance(value, dict):
        raise ConfigurationError(f"Configuration root must be an object: {path}")
    return value
