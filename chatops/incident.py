import typer

app = typer.Typer(help="Incident management commands")

@app.command()
def list():
    """List current incidents."""
    typer.echo("No active incidents")
