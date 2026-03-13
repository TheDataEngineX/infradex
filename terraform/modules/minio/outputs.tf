output "endpoint" {
  description = "MinIO API endpoint"
  value       = "http://minio.${var.namespace}.svc.cluster.local:9000"
}

output "access_key" {
  description = "MinIO access key"
  value       = var.access_key
  sensitive   = true
}

output "secret_key" {
  description = "MinIO secret key"
  value       = var.secret_key
  sensitive   = true
}
