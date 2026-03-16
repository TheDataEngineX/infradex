# Cloudflare DNS Module
# Manages DNS records via Cloudflare API
#
# Usage:
#   module "dns" {
#     source     = "../../modules/dns-cloudflare"
#     zone_id    = var.cloudflare_zone_id
#     domain     = "dataenginex.dev"
#     subdomain  = "api"
#     ip_address = module.k3s_vps.public_ip
#     api_token  = var.cloudflare_api_token
#   }

terraform {
  required_version = ">= 1.9.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.api_token
}

variable "zone_id" {
  type = string
}

variable "domain" {
  type = string
}

variable "subdomain" {
  type = string
}

variable "ip_address" {
  type = string
}

variable "api_token" {
  type      = string
  sensitive = true
}

# TODO: Uncomment and configure when Cloudflare account is ready
#
# resource "cloudflare_record" "a_record" {
#   zone_id = var.zone_id
#   name    = var.subdomain
#   content = var.ip_address
#   type    = "A"
#   ttl     = 300
#   proxied = true
# }
