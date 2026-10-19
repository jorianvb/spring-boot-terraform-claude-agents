variable "project" {
  description = "Nom du projet, utilise dans les noms et les tags"
  type        = string
}

variable "environment" {
  description = "Nom de l'environnement (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment doit valoir dev, staging ou prod."
  }
}

variable "vpc_cidr" {
  description = "Plage d'adresses IP du VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Zones de disponibilite utilisees (un sous-reseau public et un prive par zone)"
  type        = list(string)
}
