output "fqdn" {
  description = "Fully qualified domain name"
  value       = "${var.subdomain}.${var.domain}"
}

output "record_id" {
  description = "Cloudflare DNS record ID"
  value       = "" # TODO: Replace with cloudflare_record.a_record.id when resource is enabled
}
