variable "zone_id" {
  description = "Cloudflare zone ID for the domain"
  type        = string
}

variable "domain" {
  description = "Root domain name (e.g., dataenginex.dev)"
  type        = string
}

variable "subdomain" {
  description = "Subdomain for the A record (e.g., api, app)"
  type        = string
}

variable "ip_address" {
  description = "IPv4 address to point the DNS record to"
  type        = string
}

variable "api_token" {
  description = "Cloudflare API token with DNS edit permissions"
  type        = string
  sensitive   = true
}
