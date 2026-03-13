output "connection_string" {
  description = "Redis connection string"
  value       = "redis://redis.${var.namespace}.svc.cluster.local:6379"
  sensitive   = true
}

output "host" {
  description = "Redis service hostname"
  value       = "redis.${var.namespace}.svc.cluster.local"
}

output "port" {
  description = "Redis service port"
  value       = 6379
}
