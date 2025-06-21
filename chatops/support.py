from __future__ import annotations
import typer
from rich.console import Console
from rich.markdown import Markdown
from .utils import log_command, time_command
from .openai_utils import openai_client

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None

app = typer.Typer(help="Interactive support assistant")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Run interactive assistant when invoked directly."""
    if ctx.invoked_subcommand is None:
        support()


def _client(console: Console | None = None) -> 'openai.OpenAI':
    """Return an OpenAI client after ensuring an API key is available."""
    return openai_client(console)


@time_command
@log_command
@app.command()
def support():
    """Launch an interactive DevOps assistant."""
    console = Console()
    try:
        client = _client(console)
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1)

    messages = [
        {"role": "system", "content": "You are a helpful DevOps and cloud assistant"}
    ]

    while True:
        try:
            user_input = console.input("[bold blue]support> [/bold blue]")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        messages.append({"role": "user", "content": user_input})
        try:
            resp = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.2,
                stream=True,
            )
            parts: list[str] = []
            if hasattr(resp, "__iter__"):
                for chunk in resp:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        console.print(delta, end="")
                        parts.append(delta)
                console.print()
                reply = "".join(parts)
            else:
                reply = resp.choices[0].message.content
                console.print(Markdown(reply))
            messages.append({"role": "assistant", "content": reply})
        except Exception as exc:
            console.print(f"[red]Error: {exc}[/red]")
    console.print("[green]Goodbye![/green]")
