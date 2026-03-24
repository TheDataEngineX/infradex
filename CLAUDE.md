# CLAUDE.md — InfraDEX

> Repo-specific context. Workspace-level rules, coding standards, and git conventions are in `../CLAUDE.md`.

## Project Overview

**InfraDEX** — Infrastructure-as-Code for the full DataEngineX platform. Terraform, Helm, Ansible, ArgoCD, monitoring.

**Stack:** Python 3.13+ (CLI) · Terraform · Helm · Ansible · K3s · ArgoCD · Prometheus/Grafana

**Version:** `uv run poe version` | **Target:** Single Hetzner CX41 VPS (K3s) or AWS EKS

## Build & Run Commands

```bash
# Python CLI
uv run ruff check src/ tests/
uv run mypy src/infradex/ --strict
uv run pytest tests/ -x --tb=short -q

# Terraform
cd terraform/k3s-vps
terraform init && terraform plan && terraform apply

# Helm
helm lint helm/<chart>/
helm upgrade --install <release> helm/<chart>/ -f helm/<chart>/values.yaml

# Monitoring stack (local dev)
docker compose -f docker-compose.monitoring.yml up -d

# CLI
infradex deploy vps       # Full K3s stack on VPS
infradex deploy aws       # AWS EKS deployment
infradex status           # Cluster + service health
infradex rotate-secrets   # Rotate all secrets
```

## Key Files

| File | Purpose |
| --- | --- |
| `terraform/` | Hetzner VPS, DNS, Postgres, Redis, MinIO, Qdrant modules |
| `helm/` | Charts for each service |
| `ansible/` | VPS bootstrap, K3s install, monitoring setup |
| `argocd/` | GitOps app definitions + overlays (dev/prod) |
| `monitoring/` | Prometheus, Alertmanager, Grafana dashboards |
| `docker-compose.monitoring.yml` | Local observability stack |
| `scripts/promote.sh` | Promote image tag to prod overlay |
| `pyproject.toml` | CLI package config |
