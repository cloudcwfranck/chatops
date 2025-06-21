from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None  # type: ignore

USER_CONFIG_FILE = Path.home() / ".chatops" / "config.yaml"
REPO_CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.yaml"

DEFAULT_CONFIG_FILE = USER_CONFIG_FILE if USER_CONFIG_FILE.exists() else REPO_CONFIG_FILE



def _parse_simple(text: str) -> Dict:
    """Very small YAML subset parser used when PyYAML is unavailable."""
    data: Dict[str, Dict] = {}
    current: Optional[str] = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if line == "environments:":
            continue
        if line.startswith("  ") and line.endswith(":"):
            current = line.strip()[:-1]
            data[current] = {}
        elif current and ":" in line:
            key, value = line.strip().split(":", 1)
            data[current][key.strip()] = value.strip()
    return {"environments": data}


def load() -> Dict:
    """Load configuration data."""
    if not CONFIG_FILE.exists():
        return {}
    text = CONFIG_FILE.read_text()
    if yaml is not None:
        try:
            return yaml.safe_load(text) or {}
        except Exception:
            return {}
    # Fallback to extremely small parser for test environments without PyYAML
    return _parse_simple(text)


def environments() -> Dict[str, Dict]:
    data = load()
    return data.get("environments", {})


def get_env(name: str) -> Optional[Dict]:
    return environments().get(name)


def validate_env(name: str) -> None:
    env = get_env(name)
    if env is None:
        raise ValueError(
            f"Environment '{name}' not found in {CONFIG_FILE}"
        )
    provider = env.get("provider")
    if provider not in {"azure", "aws", "gcp", "docker", "local"}:
        raise ValueError(f"Invalid provider for {name}")

