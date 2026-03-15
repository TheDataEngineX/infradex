# Cloud Migration Guide

Migrate from a single-VPS K3s deployment to managed Kubernetes on AWS EKS or GCP GKE.

## When to Migrate

- Traffic exceeds what a single VPS can handle
- Need multi-AZ high availability
- Compliance requires managed infrastructure
- Team size grows beyond solo operation

## Migration Paths

### Path A: VPS → AWS EKS

1. **Provision EKS cluster**

   ```bash
   cd terraform/environments/aws
   terraform init
   terraform plan
   terraform apply
   ```

1. **Update kubeconfig**

   ```bash
   aws eks update-kubeconfig --name dex-cluster --region us-east-1
   ```

1. **Deploy with cloud values**

   ```bash
   helm install datadex helm/charts/datadex -f helm/values/values-cloud.yaml
   helm install careerdex helm/charts/careerdex -f helm/values/values-cloud.yaml
   helm install agentdex helm/charts/agentdex -f helm/values/values-cloud.yaml
   helm install dex-studio helm/charts/dex-studio -f helm/values/values-cloud.yaml
   ```

### Path B: VPS → GCP GKE

1. **Provision GKE cluster**

   ```bash
   cd terraform/environments/gcp
   terraform init
   terraform plan -var="gcp_project=your-project-id"
   terraform apply -var="gcp_project=your-project-id"
   ```

1. **Update kubeconfig**

   ```bash
   gcloud container clusters get-credentials dex-cluster --region us-central1
   ```

1. **Deploy with cloud values** (same Helm commands as Path A)

## Data Migration Checklist

### PostgreSQL

- [ ] Create backup on VPS: `./scripts/backup-databases.sh`
- [ ] Provision managed database (RDS / Cloud SQL)
- [ ] Restore backup to managed database
- [ ] Update `DATABASE_URL` in Kubernetes secrets
- [ ] Verify data integrity with row counts and checksums

### Redis

- [ ] Redis is ephemeral cache — no data migration needed
- [ ] Provision managed Redis (ElastiCache / Memorystore)
- [ ] Update `REDIS_URL` in Kubernetes secrets

### MinIO → S3 / GCS

- [ ] Sync objects: `mc mirror vps-minio/dex s3/dex-bucket`
- [ ] Update storage endpoints in application config
- [ ] Verify object accessibility

### Qdrant

- [ ] Create snapshot on VPS: `curl -X POST http://qdrant:6333/collections/*/snapshots`
- [ ] Restore snapshot on cloud Qdrant instance
- [ ] Update `QDRANT_URL` in application config

## DNS Cutover

1. Lower TTL to 60s (24 hours before migration)
1. Deploy and verify cloud environment
1. Update DNS A record to cloud load balancer IP
1. Monitor for errors during propagation
1. Restore TTL to 300s after verification

## Rollback Plan

Keep the VPS running for 72 hours after cutover:

- DNS can be reverted in < 5 minutes
- VPS data remains intact as fallback
- Only decommission after full verification period
