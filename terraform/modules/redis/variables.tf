variable "redis_version" {
  description = "Redis / Valkey version to deploy"
  type        = string
  default     = "7"
}

variable "maxmemory" {
  description = "Maximum memory allocation for Redis"
  type        = string
  default     = "256mb"
}

variable "namespace" {
  description = "Kubernetes namespace for Redis deployment"
  type        = string
  default     = "dex"
}
