---
name: terraform-module
description: A utiliser quand on cree un nouveau module Terraform. Ne pas utiliser pour une simple modification de variable existante.
---

# Creer un module Terraform

1. Structure : `variables.tf`, `main.tf`, `outputs.tf`, `versions.tf` (avec `required_providers` et version epinglee).
2. Toutes les ressources doivent avoir les tags obligatoires du projet (`Project`, `Environment`, `ManagedBy=terraform`).
3. Pas de valeur sensible en dur : passer par des variables marquees `sensitive = true` ou un secret manager.
4. Documenter chaque variable et output avec une `description`.
5. Lancer `terraform fmt`, `terraform validate` avant de proposer le module.
6. Ne jamais lancer `terraform apply` toi-meme : produire le `plan` et laisser la decision a un humain.
