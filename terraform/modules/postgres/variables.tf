variable "postgres_version" {
  description = "PostgreSQL version to deploy"
  type        = string
  default     = "16"
}

variable "storage_size" {
  description = "Persistent volume size for PostgreSQL data"
  type        = string
  default     = "10Gi"
}

variable "database_name" {
  description = "Name of the default database to create"
  type        = string
  default     = "dex"
}

variable "namespace" {
  description = "Kubernetes namespace for PostgreSQL deployment"
  type        = string
  default     = "dex"
}
