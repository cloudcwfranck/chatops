from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None  # type: ignore

CONFIG_FILE = Path.home() / ".chatops" / "config.yaml"


def load() -> Dict:
    """Load configuration data."""
    if CONFIG_FILE.exists() and yaml is not None:
        try:
            return yaml.safe_load(CONFIG_FILE.read_text()) or {}
        except Exception:
            return {}
    return {}


def environments() -> Dict[str, Dict]:
    data = load()
    return data.get("environments", {})


def get_env(name: str) -> Optional[Dict]:
    return environments().get(name)


def validate_env(name: str) -> None:
    env = get_env(name)
    if env is None:
        raise ValueError(f"Environment {name} not found in config")
    provider = env.get("provider")
    if provider not in {"azure", "aws", "docker", "local"}:
        raise ValueError(f"Invalid provider for {name}")

