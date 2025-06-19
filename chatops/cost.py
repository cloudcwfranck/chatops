import typer

app = typer.Typer(help="Cost management commands")

@app.command()
def report():
    """Generate cost report."""
    typer.echo("Cost report for the month")
