terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # State distant (a activer une fois le bucket S3 cree) : jamais de state en local en equipe.
  # Depuis Terraform 1.10, le verrouillage se fait directement dans S3 (use_lockfile),
  # la table DynamoDB n'est plus necessaire (elle est depreciee).
  # backend "s3" {
  #   bucket       = "mon-bucket-terraform-state"
  #   key          = "spring-boot-app/dev/terraform.tfstate"
  #   region       = "eu-west-3"
  #   use_lockfile = true
  # }
}

provider "aws" {
  region = var.region
}

module "network" {
  source = "../../modules/network"

  project            = var.project
  environment        = "dev"
  availability_zones = ["${var.region}a", "${var.region}b"]
}
