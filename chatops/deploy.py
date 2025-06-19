import typer

app = typer.Typer(help="Deployment related commands")

@app.command()
def status():
    """Show deployment status."""
    typer.echo("Deployment is healthy")
