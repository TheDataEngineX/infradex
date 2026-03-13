variable "storage_size" {
  description = "Persistent volume size for MinIO data"
  type        = string
  default     = "50Gi"
}

variable "access_key" {
  description = "MinIO root access key"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "MinIO root secret key"
  type        = string
  sensitive   = true
}

variable "namespace" {
  description = "Kubernetes namespace for MinIO deployment"
  type        = string
  default     = "dex"
}
