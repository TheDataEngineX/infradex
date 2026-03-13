# MinIO Object Storage Module
# Deploys MinIO S3-compatible storage via Kubernetes or Helm
#
# Usage:
#   module "minio" {
#     source       = "../../modules/minio"
#     storage_size = "50Gi"
#     access_key   = var.minio_access_key
#     secret_key   = var.minio_secret_key
#   }

terraform {
  required_version = ">= 1.5"
}

variable "storage_size" {
  type = string
}

variable "access_key" {
  type      = string
  sensitive = true
}

variable "secret_key" {
  type      = string
  sensitive = true
}

variable "namespace" {
  description = "Kubernetes namespace for MinIO"
  type        = string
  default     = "dex"
}

# TODO: Replace with actual resource — options:
# - helm_release (MinIO Operator or standalone chart)
# - kubernetes_stateful_set_v1 (direct K8s)
#
# resource "helm_release" "minio" {
#   name       = "minio"
#   namespace  = var.namespace
#   repository = "https://charts.min.io/"
#   chart      = "minio"
#
#   set {
#     name  = "persistence.size"
#     value = var.storage_size
#   }
#
#   set_sensitive {
#     name  = "rootUser"
#     value = var.access_key
#   }
#
#   set_sensitive {
#     name  = "rootPassword"
#     value = var.secret_key
#   }
# }
