# K3s on VPS — Terraform module
# Provisions a lightweight Kubernetes cluster on Hetzner/DigitalOcean/Contabo

terraform {
  required_version = ">= 1.9.0"
}

variable "server_type" {
  description = "VPS server type (e.g. cx41 for Hetzner)"
  type        = string
  default     = "cx41"
}

variable "location" {
  description = "Server location"
  type        = string
  default     = "fsn1"
}

variable "ssh_key_name" {
  description = "Name of the SSH key to use"
  type        = string
}

variable "domain" {
  description = "Base domain for the platform"
  type        = string
  default     = "thedataenginex.org"
}

# Outputs
output "server_ip" {
  description = "Public IP of the VPS"
  value       = "TODO: implement"
}

output "kubeconfig" {
  description = "K3s kubeconfig content"
  value       = "TODO: implement"
  sensitive   = true
}
