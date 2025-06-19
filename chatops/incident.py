import os
import requests
import typer

app = typer.Typer(help="Incident management commands")

@app.command()
def list():
    """List current incidents."""
    typer.echo("No active incidents")


@app.command()
def create():
    """Create a new incident using a dummy ITSM API."""
    title = typer.prompt("Title")
    severity = typer.prompt("Severity")
    service = typer.prompt("Affected service")

    api_url = os.environ.get("ITSM_API_URL", "https://httpbin.org/post")
    body = {"title": title, "severity": severity, "service": service}

    try:
        resp = requests.post(api_url, json=body, timeout=5)
    except requests.RequestException as exc:
        typer.echo(f"Request failed: {exc}")
        raise typer.Exit(code=1)

    if resp.status_code in {200, 201, 202}:
        typer.echo("Incident created")
    else:
        typer.echo(f"Failed to create incident: {resp.status_code} {resp.text}")
        raise typer.Exit(code=1)
