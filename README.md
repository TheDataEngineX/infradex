# InfraDEX

[![CI](https://github.com/TheDataEngineX/infradex/actions/workflows/ci.yml/badge.svg)](https://github.com/TheDataEngineX/infradex/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/TheDataEngineX/infradex)](https://github.com/TheDataEngineX/infradex/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Infrastructure-as-Code for the TheDataEngineX platform** — Terraform modules, Helm charts, Ansible playbooks, and monitoring stack to deploy the entire platform on VPS or cloud.

______________________________________________________________________

## Quick Start

```bash
# Install CLI
uv add infradex

# Or run from source
git clone https://github.com/TheDataEngineX/infradex && cd infradex
uv sync

infradex deploy vps          # One-command VPS deployment
infradex status              # Show cluster + service health
```

## CLI

```bash
infradex deploy vps                  # Deploy full stack to VPS (K3s)
infradex deploy aws                  # Deploy to AWS EKS
infradex status                      # Show cluster + service health
infradex backup                      # Backup all databases
infradex rotate-secrets              # Rotate all secrets
infradex logs                        # Aggregate logs from all services
```

## Development

```bash
uv run ruff check src/ tests/          # lint
uv run ruff format --check src/ tests/ # format check
uv run mypy src/infradex/ --strict     # typecheck
uv run pytest tests/ -x --tb=short -q # test

terraform fmt -check -recursive terraform/   # Terraform format
helm lint helm/*/                            # Helm lint
```

______________________________________________________________________

## What's Inside

### Monitoring Stack (Local Development)

The full observability stack lives in this repo. Spin it up locally with:

```bash
docker compose -f docker-compose.monitoring.yml up -d
```

| Service | Port | Purpose |
|---|---|---|
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Dashboards (admin/admin) |
| Alertmanager | 9093 | Alert routing |
| Jaeger | 16686 | Distributed tracing |

Pre-built dashboards cover: API latency, pipeline throughput, ML model drift, agent token costs.

### Terraform Modules

| Module | Description |
|---|---|
| `k3s-vps` | K3s lightweight Kubernetes on any VPS provider |
| `dns-cloudflare` | DNS records + CDN |
| `postgres` | PostgreSQL (self-hosted or managed) |
| `redis` | Redis / Valkey cache |
| `minio` | MinIO S3-compatible object storage |
| `qdrant` | Qdrant vector database |

### Helm Charts

| Chart | Port | Description |
|---|---|---|
| `dataenginex` | 8000 | Core framework API |
| `datadex` | 8001 | Pipeline engine API |
| `agentdex` | 8002 | Agent platform API |
| `careerdex` | 8003 | Career intelligence API |
| `dex-studio` | 8080 | Desktop UI (server mode) |
| `dex-monitoring` | — | Prometheus + Grafana + Loki + Jaeger |

### Ansible Playbooks

| Playbook | Description |
|---|---|
| `bootstrap-vps.yml` | Initial server setup + hardening |
| `install-k3s.yml` | K3s installation |
| `setup-monitoring.yml` | Observability stack deployment |

## VPS Target

Single Hetzner CX41 (~$15-30/mo):

```
K3s → Traefik → Let's Encrypt TLS
├── dataenginex   :8000
├── datadex       :8001
├── agentdex      :8002
├── careerdex     :8003
├── dex-studio    :8080
├── PostgreSQL, Redis, MinIO, Qdrant
└── Prometheus, Grafana, Loki
```

## Cloud Migration

Same Helm charts work on AWS EKS / GCP GKE:

```bash
cd terraform/environments/aws/
terraform apply
```

______________________________________________________________________

**Part of [TheDataEngineX](https://github.com/TheDataEngineX) ecosystem** | **License**: MIT
