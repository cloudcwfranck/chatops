from datetime import datetime, timedelta, timezone

import boto3
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Cost management commands")

@app.command()
def report():
    """Generate AWS cost report for the last 7 days by service."""
    # Determine date range for the last 7 complete days. The Cost Explorer API
    # expects the end date to be exclusive, so we use today as the end and
    # subtract seven days for the start.
    end = datetime.now(tz=timezone.utc).date()
    start = end - timedelta(days=7)

    client = boto3.client("ce")

    response = client.get_cost_and_usage(
        TimePeriod={"Start": start.strftime("%Y-%m-%d"), "End": end.strftime("%Y-%m-%d")},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    # Aggregate costs by service across the returned days
    totals: dict[str, float] = {}
    for day in response.get("ResultsByTime", []):
        for group in day.get("Groups", []):
            service = group["Keys"][0]
            cost = float(group["Metrics"]["UnblendedCost"]["Amount"])
            totals[service] = totals.get(service, 0.0) + cost

    table = Table(title=f"AWS Cost by Service ({start} to {end - timedelta(days=1)})")
    table.add_column("Service", style="cyan")
    table.add_column("USD", justify="right", style="green")

    for service, cost in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        table.add_row(service, f"{cost:.2f}")

    Console().print(table)
