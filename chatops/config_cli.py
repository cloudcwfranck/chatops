from __future__ import annotations
import yaml
from pathlib import Path
import typer
from rich.console import Console
from .utils import log_command, time_command

CONFIG_FILE = Path.home() / ".chatops" / "config.yaml"

app = typer.Typer(help="Configuration")


def _load() -> dict:
    if CONFIG_FILE.exists():
        try:
            return yaml.safe_load(CONFIG_FILE.read_text()) or {}
        except Exception:
            return {}
    return {}


def _save(data: dict) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(yaml.safe_dump(data))


@time_command
@log_command
@app.command("set")
def set_value(
    key: str = typer.Argument(..., help="Config key"),
    value: str = typer.Argument(..., help="Config value"),
):
    """Set a configuration value."""
    data = _load()
    data[key] = value
    _save(data)
    Console().print(f"Set {key}={value}")


@time_command
@log_command
@app.command("get")
def get_value(key: str = typer.Argument(..., help="Config key")):
    """Get a configuration value."""
    data = _load()
    Console().print(data.get(key, ""))
