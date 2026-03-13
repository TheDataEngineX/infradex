#!/usr/bin/env bash
# rotate-secrets.sh — Generate new secrets, update K8s, restart pods
#
# Usage:
#   ./scripts/rotate-secrets.sh [namespace]
#
# Environment variables:
#   NAMESPACE   — Kubernetes namespace (default: dex)
#   SECRET_NAME — Name of the Kubernetes secret (default: dex-secrets)

set -euo pipefail

NAMESPACE="${1:-${NAMESPACE:-dex}}"
SECRET_NAME="${SECRET_NAME:-dex-secrets}"

echo "=== DEX Secret Rotation ==="
echo "Namespace: ${NAMESPACE}"
echo "Secret: ${SECRET_NAME}"

# Generate new secrets
echo "Generating new secrets..."
NEW_DB_PASSWORD="$(openssl rand -base64 32)"
NEW_REDIS_PASSWORD="$(openssl rand -base64 32)"
NEW_MINIO_SECRET="$(openssl rand -base64 32)"
NEW_JWT_SECRET="$(openssl rand -base64 48)"

# Update Kubernetes secret
echo "Updating Kubernetes secret ${SECRET_NAME}..."
kubectl create secret generic "${SECRET_NAME}" \
  --namespace="${NAMESPACE}" \
  --from-literal=database-password="${NEW_DB_PASSWORD}" \
  --from-literal=redis-password="${NEW_REDIS_PASSWORD}" \
  --from-literal=minio-secret-key="${NEW_MINIO_SECRET}" \
  --from-literal=jwt-secret="${NEW_JWT_SECRET}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Secret updated."

# Restart deployments to pick up new secrets
echo "Restarting deployments..."
DEPLOYMENTS="$(kubectl get deployments -n "${NAMESPACE}" -o name 2>/dev/null || true)"

if [[ -z "${DEPLOYMENTS}" ]]; then
  echo "No deployments found in namespace ${NAMESPACE}."
else
  for deploy in ${DEPLOYMENTS}; do
    echo "  Restarting ${deploy}..."
    kubectl rollout restart "${deploy}" -n "${NAMESPACE}"
  done

  # Wait for rollouts to complete
  for deploy in ${DEPLOYMENTS}; do
    echo "  Waiting for ${deploy}..."
    kubectl rollout status "${deploy}" -n "${NAMESPACE}" --timeout=120s
  done
fi

echo "=== Secret rotation complete ==="
echo "WARNING: Update any external services that use these credentials."
