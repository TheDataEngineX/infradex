# Redis / Valkey Module
# Deploys Redis-compatible cache via Kubernetes or Helm
#
# Usage:
#   module "redis" {
#     source        = "../../modules/redis"
#     redis_version = "7"
#     maxmemory     = "256mb"
#   }

terraform {
  required_version = ">= 1.5"
}

variable "redis_version" {
  type = string
}

variable "maxmemory" {
  type = string
}

variable "namespace" {
  description = "Kubernetes namespace for Redis"
  type        = string
  default     = "dex"
}

# TODO: Replace with actual resource — options:
# - helm_release (Bitnami Redis or Valkey chart)
# - kubernetes_stateful_set_v1 (direct K8s)
# - aws_elasticache_cluster (ElastiCache for cloud)
#
# resource "helm_release" "redis" {
#   name       = "redis"
#   namespace  = var.namespace
#   repository = "oci://registry-1.docker.io/bitnamicharts"
#   chart      = "redis"
#   version    = var.redis_version
#
#   set {
#     name  = "master.configuration"
#     value = "maxmemory ${var.maxmemory}"
#   }
#
#   set {
#     name  = "architecture"
#     value = "standalone"
#   }
# }
