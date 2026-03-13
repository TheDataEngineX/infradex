# Qdrant Vector Database Module
# Deploys Qdrant for vector similarity search
#
# Usage:
#   module "qdrant" {
#     source       = "../../modules/qdrant"
#     version      = "1.12"
#     storage_size = "10Gi"
#     grpc_port    = 6334
#   }

terraform {
  required_version = ">= 1.5"
}

variable "version" {
  type = string
}

variable "storage_size" {
  type = string
}

variable "grpc_port" {
  type = number
}

variable "namespace" {
  description = "Kubernetes namespace for Qdrant"
  type        = string
  default     = "dex"
}

# TODO: Replace with actual resource — options:
# - helm_release (official Qdrant Helm chart)
# - kubernetes_stateful_set_v1 (direct K8s)
#
# resource "helm_release" "qdrant" {
#   name       = "qdrant"
#   namespace  = var.namespace
#   repository = "https://qdrant.github.io/qdrant-helm"
#   chart      = "qdrant"
#   version    = var.version
#
#   set {
#     name  = "persistence.size"
#     value = var.storage_size
#   }
#
#   set {
#     name  = "service.grpcPort"
#     value = var.grpc_port
#   }
# }
