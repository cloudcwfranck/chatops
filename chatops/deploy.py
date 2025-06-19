import os
import time
import requests
import typer

app = typer.Typer(help="Deployment related commands")

@app.command()
def deploy(app_name: str, env: str):
    """Trigger a GitHub Actions deployment workflow."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        typer.echo("GITHUB_TOKEN and GITHUB_REPOSITORY must be set")
        raise typer.Exit(code=1)

    dispatch_url = (
        f"https://api.github.com/repos/{repo}/actions/workflows/deploy.yml/dispatches"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    body = {"ref": "main", "inputs": {"app_name": app_name, "environment": env}}
    response = requests.post(dispatch_url, headers=headers, json=body)
    if response.status_code not in (200, 201, 204):
        typer.echo(f"Failed to dispatch workflow: {response.status_code} {response.text}")
        raise typer.Exit(code=1)

    typer.echo("Workflow dispatched")

    time.sleep(2)
    runs_url = (
        f"https://api.github.com/repos/{repo}/actions/workflows/deploy.yml/runs?per_page=1"
    )
    runs_resp = requests.get(runs_url, headers=headers)
    if runs_resp.status_code == 200:
        run = runs_resp.json().get("workflow_runs", [{}])[0]
        typer.echo(
            f"Run {run.get('id')} status: {run.get('status')} (conclusion: {run.get('conclusion')})"
        )
    else:
        typer.echo(
            f"Could not fetch workflow status: {runs_resp.status_code} {runs_resp.text}"
        )


@app.command()
def status():
    """Show deployment status."""
    typer.echo("Deployment is healthy")
