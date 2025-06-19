import typer

app = typer.Typer(help="Logging related commands")

@app.command()
def show(tail: int = 10):
    """Show recent logs."""
    typer.echo(f"Showing last {tail} log entries")
