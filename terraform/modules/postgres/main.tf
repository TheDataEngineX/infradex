# PostgreSQL Module
# Deploys PostgreSQL via Kubernetes StatefulSet or Helm chart
#
# Usage:
#   module "postgres" {
#     source        = "../../modules/postgres"
#     postgres_version = "16"
#     storage_size     = "10Gi"
#     database_name    = "dex"
#   }

terraform {
  required_version = ">= 1.9.0"
}

variable "postgres_version" {
  type = string
}

variable "storage_size" {
  type = string
}

variable "database_name" {
  type = string
}

variable "namespace" {
  description = "Kubernetes namespace for PostgreSQL"
  type        = string
  default     = "dex"
}

# TODO: Replace with actual resource — options:
# - kubernetes_stateful_set_v1 (direct K8s)
# - helm_release (CloudNativePG or Bitnami chart)
# - aws_db_instance (RDS for cloud environments)
#
# resource "helm_release" "postgres" {
#   name       = "postgres"
#   namespace  = var.namespace
#   repository = "oci://registry-1.docker.io/bitnamicharts"
#   chart      = "postgresql"
#   version    = var.postgres_version
#
#   set {
#     name  = "primary.persistence.size"
#     value = var.storage_size
#   }
#
#   set {
#     name  = "auth.database"
#     value = var.database_name
#   }
# }
