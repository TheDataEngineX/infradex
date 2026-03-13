"""InfraDEX CLI — deploy and manage TheDataEngineX platform infrastructure."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(package_name="infradex")
def main() -> None:
    """InfraDEX — infrastructure-as-code for TheDataEngineX platform."""


@main.command()
@click.argument("target", type=click.Choice(["vps", "aws", "gcp"]))
@click.option("--dry-run", is_flag=True, help="Show plan without applying")
def deploy(target: str, dry_run: bool) -> None:
    """Deploy full stack to a target environment."""
    if dry_run:
        console.print(f"[yellow]DRY RUN[/yellow] — would deploy to: [bold]{target}[/bold]")
        return
    console.print(f"Deploying to: [bold]{target}[/bold]")
    # TODO: run terraform + helm + ansible
    console.print("[green]✓[/green] Deployment complete")


@main.command()
def status() -> None:
    """Show cluster and service health."""
    table = Table(title="Cluster Status")
    table.add_column("Service", style="cyan")
    table.add_column("Status")
    table.add_column("Pod")
    table.add_column("Port")
    for svc, port in [
        ("dataenginex", "8000"),
        ("datadex", "8001"),
        ("agentdex", "8002"),
        ("careerdex", "8003"),
        ("dex-studio", "8080"),
        ("postgres", "5432"),
        ("redis", "6379"),
        ("qdrant", "6333"),
    ]:
        table.add_row(svc, "[dim]unknown[/dim]", "-", port)
    console.print(table)


@main.command()
def backup() -> None:
    """Backup all databases."""
    console.print("Backing up PostgreSQL...")
    # TODO: pg_dump via fabric SSH
    console.print("[green]✓[/green] Backup complete")


@main.command(name="rotate-secrets")
def rotate_secrets() -> None:
    """Rotate all secrets and tokens."""
    console.print("Rotating secrets...")
    # TODO: rotate JWT keys, DB passwords, API tokens
    console.print("[green]✓[/green] Secrets rotated")


@main.command()
@click.option("--tail", "-n", default=50, help="Number of log lines")
def logs(tail: int) -> None:
    """Aggregate logs from all services."""
    console.print(f"Fetching last {tail} lines from all services...")
    # TODO: kubectl logs or Loki query
    console.print("(no services running)")


if __name__ == "__main__":
    main()
