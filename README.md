# InfraDEX

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Infrastructure-as-Code for the TheDataEngineX platform** — Terraform modules, Helm charts, Ansible playbooks, and monitoring configs to deploy the entire stack on VPS or cloud.

---

## Quick Start

```bash
pip install infradex
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

## What's Inside

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
- `bootstrap-vps.yml` — Initial server setup + hardening
- `install-k3s.yml` — K3s installation
- `setup-monitoring.yml` — Observability stack

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

---

**Part of [TheDataEngineX](https://github.com/TheDataEngineX) ecosystem** | **License**: MIT
