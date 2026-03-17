# AWS EKS Environment
# Production-grade Kubernetes on AWS

terraform {
  required_version = ">= 1.9.0"

  backend "s3" {
    bucket         = "infradex-terraform-state"
    key            = "aws/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "infradex-terraform-locks"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for EKS cluster"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "dex-cluster"
}

# TODO: Add EKS module call
# module "eks" {
#   source  = "terraform-aws-modules/eks/aws"
#   version = "~> 20.0"
#
#   cluster_name    = var.cluster_name
#   cluster_version = "1.30"
#
#   vpc_id     = module.vpc.vpc_id
#   subnet_ids = module.vpc.private_subnets
#
#   eks_managed_node_groups = {
#     dex_workers = {
#       instance_types = ["t3.medium"]
#       min_size       = 2
#       max_size       = 5
#       desired_size   = 3
#     }
#   }
# }

# TODO: Add VPC module
# module "vpc" {
#   source  = "terraform-aws-modules/vpc/aws"
#   version = "~> 5.0"
#
#   name = "${var.cluster_name}-vpc"
#   cidr = "10.0.0.0/16"
#
#   azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
#   private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
#   public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
#
#   enable_nat_gateway = true
#   single_nat_gateway = true
# }
