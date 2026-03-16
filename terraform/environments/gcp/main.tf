# GCP GKE Environment
# Production-grade Kubernetes on Google Cloud

terraform {
  required_version = ">= 1.9.0"

  backend "gcs" {
    bucket = "infradex-terraform-state"
    prefix = "gcp/terraform.tfstate"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

variable "gcp_project" {
  description = "GCP project ID"
  type        = string
}

variable "gcp_region" {
  description = "GCP region for GKE cluster"
  type        = string
  default     = "us-central1"
}

variable "cluster_name" {
  description = "GKE cluster name"
  type        = string
  default     = "dex-cluster"
}

# TODO: Add GKE module call
# module "gke" {
#   source  = "terraform-google-modules/kubernetes-engine/google"
#   version = "~> 33.0"
#
#   project_id = var.gcp_project
#   name       = var.cluster_name
#   region     = var.gcp_region
#
#   network    = google_compute_network.vpc.name
#   subnetwork = google_compute_subnetwork.subnet.name
#
#   node_pools = [
#     {
#       name         = "dex-pool"
#       machine_type = "e2-medium"
#       min_count    = 2
#       max_count    = 5
#       disk_size_gb = 50
#     }
#   ]
# }

# TODO: Add VPC
# resource "google_compute_network" "vpc" {
#   name                    = "${var.cluster_name}-vpc"
#   auto_create_subnetworks = false
# }
#
# resource "google_compute_subnetwork" "subnet" {
#   name          = "${var.cluster_name}-subnet"
#   ip_cidr_range = "10.0.0.0/16"
#   region        = var.gcp_region
#   network       = google_compute_network.vpc.id
# }
