"""InfraDEX CLI — deploy and manage TheDataEngineX platform infrastructure."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

_REPO_ROOT = Path(__file__).parent.parent.parent.parent  # infradex/
_HELM_CHARTS = _REPO_ROOT / "helm" / "charts"
_HELM_VALUES = _REPO_ROOT / "helm" / "values"
_TERRAFORM_DIR = _REPO_ROOT / "terraform" / "environments"
_NAMESPACE = os.getenv("DEX_K8S_NAMESPACE", "dex")
_REDIS_URL = os.getenv("DEX_REDIS_URL", "redis://localhost:6379")


def _run(
    cmd: list[str], check: bool = True, capture: bool = False
) -> subprocess.CompletedProcess[str]:
    """Run a shell command, streaming output to console."""
    console.print(f"[dim]$ {' '.join(cmd)}[/dim]")
    return subprocess.run(
        cmd,
        check=check,
        capture_output=capture,
        text=True,
    )


def _require_tool(name: str) -> None:
    """Exit with a clear message if a required CLI tool is missing."""
    if not shutil.which(name):
        console.print(f"[red]Error:[/red] '{name}' not found in PATH. Install it first.")
        sys.exit(1)


def _require_kubectl() -> None:
    _require_tool("kubectl")


def _require_helm() -> None:
    _require_tool("helm")


def _require_terraform() -> None:
    _require_tool("terraform")


@click.group()
@click.version_option(package_name="infradex")
def main() -> None:
    """InfraDEX — infrastructure-as-code for TheDataEngineX platform."""


# ---------------------------------------------------------------------------
# deploy
# ---------------------------------------------------------------------------


def _deploy_terraform(tf_dir: Path, dry_run: bool) -> None:
    console.print("\n[bold]Phase 1: Terraform[/bold]")
    _run(["terraform", "-chdir", str(tf_dir), "init", "-reconfigure"])
    plan_or_apply = ["plan"] if dry_run else ["apply", "-auto-approve"]
    _run(["terraform", "-chdir", str(tf_dir), *plan_or_apply])


def _deploy_helm(namespace: str, values_file: Path, dry_run: bool) -> None:
    console.print("\n[bold]Phase 2: Helm[/bold]")
    if not dry_run:
        _run(["kubectl", "create", "namespace", namespace], check=False)
    for chart_name in ["dataenginex", "dex-studio", "dex-monitoring"]:
        chart_path = _HELM_CHARTS / chart_name
        if not chart_path.exists():
            console.print(f"[yellow]Skipping missing chart:[/yellow] {chart_name}")
            continue
        cmd = [
            "helm",
            "upgrade",
            "--install",
            chart_name,
            str(chart_path),
            "--namespace",
            namespace,
            "--create-namespace",
        ]
        if values_file.exists():
            cmd += ["--values", str(values_file)]
        if dry_run:
            cmd += ["--dry-run"]
        _run(cmd)


@main.command()
@click.argument("target", type=click.Choice(["vps", "aws", "gcp"]))
@click.option("--dry-run", is_flag=True, help="Show plan without applying")
@click.option("--skip-terraform", is_flag=True, help="Skip Terraform, only run Helm")
@click.option("--skip-helm", is_flag=True, help="Skip Helm, only run Terraform")
@click.option("--namespace", default=_NAMESPACE, show_default=True, help="K8s namespace")
def deploy(
    target: str, dry_run: bool, skip_terraform: bool, skip_helm: bool, namespace: str
) -> None:
    """Deploy full stack to a target environment (vps | aws | gcp)."""
    _require_terraform()
    _require_helm()
    _require_kubectl()

    console.print(
        Panel(
            f"Deploying to [bold cyan]{target}[/bold cyan]" + (" [DRY RUN]" if dry_run else ""),
            title="InfraDEX Deploy",
        )
    )

    tf_dir = _TERRAFORM_DIR / target
    if not tf_dir.exists():
        console.print(f"[red]Terraform env not found:[/red] {tf_dir}")
        sys.exit(1)

    values_filename = "values-cloud.yaml" if target in ("aws", "gcp") else f"values-{target}.yaml"
    values_file = _HELM_VALUES / values_filename

    if not skip_terraform:
        _deploy_terraform(tf_dir, dry_run)
    if not skip_helm:
        _deploy_helm(namespace, values_file, dry_run)

    console.print(f"\n[green]{'DRY RUN complete' if dry_run else 'Deploy complete'}[/green]")


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------


@main.command()
@click.option("--namespace", default=_NAMESPACE, show_default=True)
@click.option("--watch", "-w", is_flag=True, help="Watch pod status (Ctrl+C to stop)")
def status(namespace: str, watch: bool) -> None:
    """Show cluster and service health."""
    _require_kubectl()

    if watch:
        _run(["kubectl", "get", "pods", "-n", namespace, "--watch"])
        return

    # Pods table
    result = _run(
        [
            "kubectl",
            "get",
            "pods",
            "-n",
            namespace,
            "-o",
            "custom-columns=NAME:.metadata.name,STATUS:.status.phase,READY:.status.containerStatuses[0].ready,RESTARTS:.status.containerStatuses[0].restartCount,AGE:.metadata.creationTimestamp",
        ],
        capture=True,
        check=False,
    )

    table = Table(title=f"Pods — namespace: {namespace}")
    table.add_column("Service", style="cyan")
    table.add_column("Status")
    table.add_column("Ready")
    table.add_column("Restarts")
    table.add_column("Port")

    _KNOWN_SERVICES = [
        ("dataenginex", "17000"),
        ("dex-studio", "7860"),
        ("careerdex", "7870"),
        ("postgres", "5432"),
        ("redis", "6379"),
        ("qdrant", "6333"),
        ("minio", "9000"),
        ("authentik", "9000"),
        ("prometheus", "9090"),
        ("grafana", "3000"),
    ]

    pod_output = result.stdout or ""
    for svc, port in _KNOWN_SERVICES:
        found = any(svc in line for line in pod_output.splitlines())
        status_str = "[green]Running[/green]" if found else "[dim]unknown[/dim]"
        table.add_row(svc, status_str, "-", "-", port)

    console.print(table)

    if result.returncode != 0:
        console.print(
            f"\n[yellow]Note:[/yellow] Could not reach cluster."
            f" Raw kubectl output:\n{result.stderr}"
        )

    # Services
    _run(["kubectl", "get", "svc", "-n", namespace], check=False)


# ---------------------------------------------------------------------------
# backup
# ---------------------------------------------------------------------------


@main.command()
@click.option("--namespace", default=_NAMESPACE, show_default=True)
@click.option(
    "--output-dir", "-o", default="./backups", show_default=True, help="Local backup directory"
)
@click.option("--postgres-pod", default="", help="PostgreSQL pod name (auto-detected if empty)")
def backup(namespace: str, output_dir: str, postgres_pod: str) -> None:
    """Backup PostgreSQL database to a local dump file."""
    _require_kubectl()

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    dump_file = out_dir / f"dex_postgres_{timestamp}.sql"

    # Auto-detect postgres pod
    pod = postgres_pod
    if not pod:
        result = _run(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                namespace,
                "-l",
                "app=postgres",
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ],
            capture=True,
            check=False,
        )
        pod = result.stdout.strip()

    if not pod:
        console.print(
            "[red]Error:[/red] Could not find PostgreSQL pod. Use --postgres-pod to specify."
        )
        sys.exit(1)

    console.print(f"Backing up from pod [cyan]{pod}[/cyan] → [cyan]{dump_file}[/cyan]")

    pg_user = os.getenv("POSTGRES_USER", "dex")
    pg_db = os.getenv("POSTGRES_DB", "dex")

    _run(
        [
            "kubectl",
            "exec",
            "-n",
            namespace,
            pod,
            "--",
            "pg_dump",
            "-U",
            pg_user,
            "-d",
            pg_db,
            "--no-password",
        ]
    )

    console.print(f"[green]Backup complete:[/green] {dump_file}")
    console.print(
        f"[dim]Restore with: kubectl exec -n {namespace} {pod} -- psql -U {pg_user} -d {pg_db}"
        f" < {dump_file}[/dim]"
    )


# ---------------------------------------------------------------------------
# rotate-secrets
# ---------------------------------------------------------------------------


@main.command(name="rotate-secrets")
@click.option("--namespace", default=_NAMESPACE, show_default=True)
@click.option("--dry-run", is_flag=True)
def rotate_secrets(namespace: str, dry_run: bool) -> None:
    """Rotate JWT secret, PostgreSQL password, and API tokens."""
    _require_kubectl()

    import secrets

    console.print(Panel("Secret Rotation" + (" [DRY RUN]" if dry_run else ""), title="InfraDEX"))

    new_jwt = secrets.token_urlsafe(64)
    new_db_pass = secrets.token_urlsafe(32)

    secrets_to_rotate: list[tuple[str, dict[str, str]]] = [
        ("dex-jwt-secret", {"DEX_JWT_SECRET": new_jwt}),
        ("dex-db-credentials", {"POSTGRES_PASSWORD": new_db_pass}),
    ]

    for secret_name, data in secrets_to_rotate:
        if dry_run:
            console.print(
                f"[yellow]DRY RUN:[/yellow] would patch secret/{secret_name} in {namespace}"
            )
            continue

        literal_args = [f"--from-literal={k}={v}" for k, v in data.items()]
        _run(
            [
                "kubectl",
                "create",
                "secret",
                "generic",
                secret_name,
                "-n",
                namespace,
                "--dry-run=client",
                "-o",
                "yaml",
                *literal_args,
            ],
            check=False,
        )
        _run(
            [
                "kubectl",
                "create",
                "secret",
                "generic",
                secret_name,
                "-n",
                namespace,
                *literal_args,
                "--save-config",
            ],
            check=False,
        )

        console.print(f"[green]Rotated:[/green] {secret_name}")

    if not dry_run:
        console.print("\nRestarting affected deployments...")
        for deployment in ("dataenginex", "dex-studio", "careerdex"):
            _run(
                ["kubectl", "rollout", "restart", f"deployment/{deployment}", "-n", namespace],
                check=False,
            )

    label = "DRY RUN complete" if dry_run else "Secret rotation complete"
    console.print(f"\n[green]{label}[/green]")
    if not dry_run:
        console.print(
            "[yellow]Action required:[/yellow] Update DEX_JWT_SECRET and"
            " POSTGRES_PASSWORD in Doppler/vault."
        )


# ---------------------------------------------------------------------------
# logs
# ---------------------------------------------------------------------------


@main.command()
@click.argument("service", default="dataenginex")
@click.option("--namespace", default=_NAMESPACE, show_default=True)
@click.option("--tail", "-n", default=100, show_default=True, help="Number of log lines")
@click.option("--follow", "-f", is_flag=True, help="Stream logs (Ctrl+C to stop)")
@click.option("--loki", is_flag=True, help="Query Loki instead of kubectl (requires LOKI_URL)")
def logs(service: str, namespace: str, tail: int, follow: bool, loki: bool) -> None:
    """Tail logs from a service pod (kubectl) or Loki."""
    if loki:
        _query_loki(service, tail)
        return

    _require_kubectl()

    cmd = [
        "kubectl",
        "logs",
        f"deployment/{service}",
        "-n",
        namespace,
        f"--tail={tail}",
    ]
    if follow:
        cmd.append("-f")

    console.print(f"Streaming logs from [cyan]{service}[/cyan] (namespace: {namespace})")
    _run(cmd, check=False)


def _query_loki(service: str, tail: int) -> None:
    loki_url = os.getenv("LOKI_URL", "http://localhost:3100")
    try:
        import httpx

        end = int(datetime.now(UTC).timestamp() * 1e9)
        start = end - 3_600_000_000_000  # last hour in nanoseconds
        resp = httpx.get(
            f"{loki_url}/loki/api/v1/query_range",
            params={
                "query": f'{{app="{service}"}}',
                "limit": tail,
                "start": start,
                "end": end,
            },
            timeout=10,
        )
        if resp.status_code == 200:
            data: Any = resp.json()
            for stream in data.get("data", {}).get("result", []):
                for _ts, line in stream.get("values", []):
                    console.print(line)
        else:
            console.print(f"[red]Loki error {resp.status_code}:[/red] {resp.text}")
    except Exception as exc:
        console.print(f"[red]Loki query failed:[/red] {exc}")
        console.print("[dim]Tip: set LOKI_URL env var or use --namespace with kubectl logs[/dim]")


if __name__ == "__main__":
    main()
