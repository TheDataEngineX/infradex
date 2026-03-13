# Disaster Recovery Plan

Backup strategy, recovery procedures, and RTO/RPO targets for the DataEngineX platform.

## RTO / RPO Targets

| Tier | Component | RPO | RTO | Strategy |
|------|-----------|-----|-----|----------|
| 1 | PostgreSQL | 1 hour | 30 min | Scheduled pg_dump + WAL archiving |
| 1 | Application state | 0 | 15 min | Stateless — redeploy from Git |
| 2 | Qdrant vectors | 24 hours | 2 hours | Daily snapshot + restore |
| 2 | MinIO objects | 24 hours | 1 hour | Daily sync to S3/backup bucket |
| 3 | Redis cache | N/A | 5 min | Ephemeral — auto-rebuilds on start |
| 3 | Prometheus metrics | 24 hours | 30 min | Thanos/remote-write (if configured) |

## Backup Strategy

### Automated Backups

```bash
# Daily PostgreSQL backup (add to cron)
0 2 * * * /opt/infradex/scripts/backup-databases.sh

# Weekly Qdrant snapshot
0 3 * * 0 curl -X POST http://qdrant:6333/collections/dex_vectors/snapshots

# Daily MinIO sync (if S3 backup target configured)
0 4 * * * mc mirror --overwrite minio/dex s3/dex-backup/minio/
```

### Backup Verification

Run monthly restore drills:
1. Restore PostgreSQL backup to a test database
2. Verify row counts match production
3. Run application health checks against test database
4. Document results and any issues

## Recovery Procedures

### Scenario 1: VPS Total Loss

**Time estimate: 30-60 minutes**

1. Provision new VPS
   ```bash
   hcloud server create --name dex-server-recovery --type cx31 --image ubuntu-22.04
   ```

2. Update inventory with new IP
   ```bash
   vim ansible/inventory/hosts.yml
   ```

3. Run full deployment
   ```bash
   ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/install-k3s.yml
   ./scripts/one-click-deploy.sh
   ```

4. Restore database
   ```bash
   gunzip -c /path/to/backup/dex_YYYYMMDD_HHMMSS.sql.gz | \
     psql -h localhost -U postgres -d dex
   ```

5. Update DNS to new IP

### Scenario 2: Database Corruption

**Time estimate: 15-30 minutes**

1. Stop application pods
   ```bash
   kubectl scale deployment --replicas=0 -l app=datadex -n dex
   kubectl scale deployment --replicas=0 -l app=careerdex -n dex
   ```

2. Restore from latest backup
   ```bash
   # Drop and recreate database
   psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS dex;"
   psql -h localhost -U postgres -c "CREATE DATABASE dex;"

   # Restore
   gunzip -c /path/to/latest/backup.sql.gz | psql -h localhost -U postgres -d dex
   ```

3. Restart application pods
   ```bash
   kubectl scale deployment --replicas=1 -l app=datadex -n dex
   kubectl scale deployment --replicas=1 -l app=careerdex -n dex
   ```

4. Verify data integrity

### Scenario 3: Kubernetes Cluster Failure

**Time estimate: 30 minutes**

1. Reinstall K3s
   ```bash
   ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/install-k3s.yml
   ```

2. Redeploy all Helm charts
   ```bash
   helm install datadex helm/charts/datadex -f helm/values/values-vps.yaml
   helm install careerdex helm/charts/careerdex -f helm/values/values-vps.yaml
   helm install agentdex helm/charts/agentdex -f helm/values/values-vps.yaml
   ```

3. Restore persistent data (PostgreSQL, Qdrant)

### Scenario 4: Secret Compromise

**Time estimate: 10 minutes**

1. Rotate all secrets immediately
   ```bash
   ./scripts/rotate-secrets.sh dex
   ```

2. Revoke any external API tokens (Cloudflare, container registry)

3. Audit access logs for unauthorized activity

4. Update monitoring alerts for anomalous patterns

## Communication Plan

| Severity | Notify | Channel |
|----------|--------|---------|
| P1 — Full outage | All stakeholders | Immediate |
| P2 — Degraded | Engineering team | Within 30 min |
| P3 — Minor issue | On-call engineer | Within 2 hours |

## Post-Incident

After every incident:
1. Conduct blameless post-mortem
2. Document root cause and timeline
3. Update runbooks if procedures were unclear
4. Implement preventive measures
5. Test the fix with a simulated failure
