import typer
from . import deploy, logs, cost, iam, incident, security, cve, suggest, monitor, explain, support

app = typer.Typer(help="ChatOps CLI")

app.add_typer(deploy.app, name="deploy")
app.add_typer(logs.app, name="logs")
app.add_typer(cost.app, name="cost")
app.add_typer(iam.app, name="iam")
app.add_typer(incident.app, name="incident")
app.add_typer(security.app, name="security")
app.add_typer(cve.app, name="cve")
app.add_typer(explain.app, name="explain")
app.add_typer(monitor.app, name="monitor")


@app.command("suggest")
def suggest_cmd(prompt: str) -> None:
    """Suggest best ChatOps command."""
    suggest.suggest(prompt)


@app.command("support")
def support_cmd() -> None:
    """Launch the interactive support assistant."""
    support.support()
