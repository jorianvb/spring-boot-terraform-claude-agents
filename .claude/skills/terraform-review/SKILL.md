---
name: terraform-review
description: A utiliser pour relire un plan ou un diff Terraform avant un apply. Utiliser PROACTIVEMENT apres toute modification de fichiers .tf.
---

# Relire un plan Terraform

1. Lancer `terraform plan` et lire integralement la sortie.
2. Verifier particulierement :
   - des ressources marquees pour destruction (`-`) non voulues ;
   - un changement de taille/type d'instance ou de base de donnees ;
   - l'absence de tags obligatoires ;
   - des security groups trop permissifs (0.0.0.0/0 en entree) ;
   - des secrets ou identifiants en dur.
3. Donner un verdict clair : "OK pour apply" ou "a corriger", avec la liste precise des points bloquants.
4. Ne jamais executer `terraform apply` : ce n'est pas le role de cette revue.
