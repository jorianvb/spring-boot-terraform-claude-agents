variable "region" {
  description = "Region AWS de deploiement"
  type        = string
  default     = "eu-west-3"
}

variable "project" {
  description = "Nom du projet, utilise dans les noms et les tags"
  type        = string
  default     = "spring-boot-app"
}
