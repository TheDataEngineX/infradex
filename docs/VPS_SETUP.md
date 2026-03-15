# VPS Setup Guide

Deploy the full DataEngineX platform on a single VPS using K3s.

## Prerequisites

- **VPS Provider:** Hetzner Cloud (recommended), DigitalOcean, or any Linux VPS
- **Specs:** Minimum 4 vCPU, 8 GB RAM, 80 GB SSD
- **OS:** Ubuntu 22.04 or Debian 12
- **Domain:** Registered domain with Cloudflare DNS (optional)
- **SSH Key:** Ed25519 key pair (`ssh-keygen -t ed25519`)

## Quick Start

```bash
# 1. Clone the infradex repo
git clone https://github.com/TheDataEngineX/infradex.git
cd infradex

# 2. Copy and edit configuration
cp ansible/inventory/hosts.example.yml ansible/inventory/hosts.yml
# Edit hosts.yml with your VPS IP and SSH key path

# 3. Run the one-click deploy
./scripts/one-click-deploy.sh
```

## Manual Setup

### 1. Provision VPS (Hetzner)

```bash
# Install hcloud CLI
brew install hcloud  # macOS
# or: snap install hcloud

# Create server
hcloud server create \
  --name dex-server \
  --type cx31 \
  --image ubuntu-22.04 \
  --ssh-key your-key-name \
  --location nbg1
```

### 2. Install K3s

```bash
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/install-k3s.yml
```

### 3. Deploy Platform

```bash
# Set kubeconfig
export KUBECONFIG=./kubeconfig

# Install core services
helm install datadex helm/charts/datadex -f helm/values/values-vps.yaml
helm install careerdex helm/charts/careerdex -f helm/values/values-vps.yaml
helm install agentdex helm/charts/agentdex -f helm/values/values-vps.yaml
helm install dex-studio helm/charts/dex-studio -f helm/values/values-vps.yaml
```

### 4. Setup Monitoring

```bash
ansible-playbook ansible/playbooks/setup-monitoring.yml
```

### 5. Configure DNS (Optional)

```bash
cd terraform/modules/dns-cloudflare
terraform init
terraform apply \
  -var="zone_id=YOUR_ZONE_ID" \
  -var="domain=dataenginex.dev" \
  -var="subdomain=api" \
  -var="ip_address=YOUR_VPS_IP" \
  -var="api_token=YOUR_CF_TOKEN"
```

## Verification

```bash
# Check all pods are running
kubectl get pods -A

# Check service health
curl http://YOUR_VPS_IP:8001/health   # datadex
curl http://YOUR_VPS_IP:8003/health   # careerdex
curl http://YOUR_VPS_IP:8002/health   # agentdex
```

## Resource Budget (8 GB VPS)

| Component | CPU | Memory |
|-------------|--------|--------|
| K3s system | 250m | 512Mi |
| datadex | 250m | 256Mi |
| careerdex | 250m | 256Mi |
| agentdex | 250m | 256Mi |
| dex-studio | 100m | 128Mi |
| PostgreSQL | 250m | 256Mi |
| Redis | 100m | 128Mi |
| Prometheus | 100m | 256Mi |
| Grafana | 50m | 64Mi |
| **Total** | **1.6**| **~2Gi**|

Leaves ~6 GB headroom for spikes and OS.
