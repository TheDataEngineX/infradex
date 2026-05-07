#!/usr/bin/env bash
# One-click deploy — bootstraps the entire TheDataEngineX platform on a VPS
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRADEX_ROOT="$(dirname "$SCRIPT_DIR")"

echo "╔══════════════════════════════════════════════╗"
echo "║  TheDataEngineX — One-Click Deploy           ║"
echo "╚══════════════════════════════════════════════╝"

# 1. Bootstrap VPS
echo "→ Step 1/4: Bootstrapping VPS..."
ansible-playbook "$INFRADEX_ROOT/ansible/playbooks/bootstrap-vps.yml" -i "$INFRADEX_ROOT/ansible/inventory/hosts.yml"

# 2. Install K3s
echo "→ Step 2/4: Installing K3s..."
ansible-playbook "$INFRADEX_ROOT/ansible/playbooks/install-k3s.yml" -i "$INFRADEX_ROOT/ansible/inventory/hosts.yml"

# 3. Deploy services via Helm
echo "→ Step 3/4: Deploying services..."
helm upgrade --install dataenginex "$INFRADEX_ROOT/helm/charts/dataenginex/" -f "$INFRADEX_ROOT/helm/values/values-vps.yaml"
helm upgrade --install dex-studio "$INFRADEX_ROOT/helm/charts/dex-studio/" -f "$INFRADEX_ROOT/helm/values/values-vps.yaml"

# 4. Set up monitoring
echo "→ Step 4/4: Setting up monitoring..."
ansible-playbook "$INFRADEX_ROOT/ansible/playbooks/setup-monitoring.yml" -i "$INFRADEX_ROOT/ansible/inventory/hosts.yml"

echo ""
echo "✓ Deployment complete!"
echo "  API:     https://api.thedataenginex.org"
echo "  Studio:  https://studio.thedataenginex.org"
echo "  Grafana: https://monitoring.thedataenginex.org"
