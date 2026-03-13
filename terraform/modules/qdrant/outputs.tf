output "grpc_endpoint" {
  description = "Qdrant gRPC endpoint"
  value       = "qdrant.${var.namespace}.svc.cluster.local:${var.grpc_port}"
}

output "http_endpoint" {
  description = "Qdrant HTTP REST endpoint"
  value       = "http://qdrant.${var.namespace}.svc.cluster.local:6333"
}
