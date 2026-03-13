output "connection_string" {
  description = "PostgreSQL connection string"
  value       = "postgresql://postgres@${var.database_name}-postgres.${var.namespace}.svc.cluster.local:5432/${var.database_name}"
  sensitive   = true
}

output "host" {
  description = "PostgreSQL service hostname"
  value       = "${var.database_name}-postgres.${var.namespace}.svc.cluster.local"
}

output "port" {
  description = "PostgreSQL service port"
  value       = 5432
}
