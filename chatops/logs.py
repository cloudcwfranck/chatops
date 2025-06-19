import typer
from azure.identity import AzureCliCredential
from azure.monitor.query import LogsQueryClient
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Logging related commands")

@app.command()
def show(tail: int = 10):
    """Show recent logs."""
    typer.echo(f"Showing last {tail} log entries")


@app.command()
def azure(
    workspace_id: str = typer.Argument(..., help="Log Analytics workspace ID"),
    query: str = typer.Argument(..., help="Kusto query to run"),
):
    """Run a Kusto query against Azure Monitor Logs."""
    credential = AzureCliCredential()
    client = LogsQueryClient(credential)

    response = client.query_workspace(workspace_id, query)

    if not response.tables:
        typer.echo("No results")
        raise typer.Exit()

    table = Table(title="Query Results")
    first_table = response.tables[0]
    for column in first_table.columns:
        table.add_column(column.name)

    for row in first_table.rows:
        table.add_row(*[str(item) for item in row])

    Console().print(table)
