# VPS Environment — Priority deployment target
# Uses K3s module to deploy lightweight Kubernetes on a VPS

terraform {
  required_version = ">= 1.9.0"

  backend "s3" {
    bucket         = "thedataenginex-terraform-state"
    key            = "vps/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

variable "hetzner_token" {
  description = "Hetzner Cloud API token"
  type        = string
  sensitive   = true
}

variable "ssh_key_name" {
  description = "SSH key name in Hetzner Cloud"
  type        = string
}

module "k3s" {
  source       = "../../modules/k3s-vps"
  server_type  = "cx41"
  location     = "fsn1"
  ssh_key_name = var.ssh_key_name
  domain       = "thedataenginex.org"
}
