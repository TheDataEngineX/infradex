variable "version" {
  description = "Qdrant version to deploy"
  type        = string
  default     = "1.12"
}

variable "storage_size" {
  description = "Persistent volume size for Qdrant data"
  type        = string
  default     = "10Gi"
}

variable "grpc_port" {
  description = "gRPC port for Qdrant service"
  type        = number
  default     = 6334
}

variable "namespace" {
  description = "Kubernetes namespace for Qdrant deployment"
  type        = string
  default     = "dex"
}
