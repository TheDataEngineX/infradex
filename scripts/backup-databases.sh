#!/usr/bin/env bash
# backup-databases.sh — PostgreSQL backup with S3 upload and retention
#
# Usage:
#   ./scripts/backup-databases.sh
#
# Environment variables:
#   PGHOST          — PostgreSQL host (default: localhost)
#   PGPORT          — PostgreSQL port (default: 5432)
#   PGUSER          — PostgreSQL user (default: postgres)
#   PGDATABASE      — Database name (default: dex)
#   BACKUP_DIR      — Local backup directory (default: /tmp/dex-backups)
#   S3_BUCKET       — S3/MinIO bucket for remote storage
#   RETENTION_DAYS  — Days to keep local backups (default: 7)

set -euo pipefail

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-dex}"
BACKUP_DIR="${BACKUP_DIR:-/tmp/dex-backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
BACKUP_FILE="${BACKUP_DIR}/${PGDATABASE}_${TIMESTAMP}.sql.gz"

echo "=== DEX Database Backup ==="
echo "Database: ${PGDATABASE}@${PGHOST}:${PGPORT}"
echo "Timestamp: ${TIMESTAMP}"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Run pg_dump and compress
echo "Creating backup..."
pg_dump -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" \
  --format=plain --no-owner --no-acl | gzip > "${BACKUP_FILE}"

BACKUP_SIZE="$(du -h "${BACKUP_FILE}" | cut -f1)"
echo "Backup created: ${BACKUP_FILE} (${BACKUP_SIZE})"

# Upload to S3/MinIO (if configured)
if [[ -n "${S3_BUCKET:-}" ]]; then
  echo "Uploading to s3://${S3_BUCKET}/backups/..."
  # TODO: Replace with aws s3 cp or mc (MinIO client)
  # aws s3 cp "${BACKUP_FILE}" "s3://${S3_BUCKET}/backups/$(basename "${BACKUP_FILE}")"
  echo "WARNING: S3 upload not configured. Set S3_BUCKET and install aws-cli or mc."
else
  echo "S3_BUCKET not set — skipping remote upload."
fi

# Retention cleanup — remove local backups older than RETENTION_DAYS
echo "Cleaning up backups older than ${RETENTION_DAYS} days..."
DELETED_COUNT="$(find "${BACKUP_DIR}" -name "${PGDATABASE}_*.sql.gz" -mtime "+${RETENTION_DAYS}" -print -delete | wc -l)"
echo "Removed ${DELETED_COUNT} old backup(s)."

echo "=== Backup complete ==="
