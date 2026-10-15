# CLAUDE.md

## Projet
API Spring Boot (DDD) + infrastructure Terraform (AWS).
Backend Java 21 / Spring Boot 3.x. Infra : Terraform, environnements sous `terraform/envs/`.

## Architecture
Voir @docs/architecture.md pour le détail. En résumé : chaque module métier est organisé en
`domain/`, `application/`, `infrastructure/` (voir la Skill `ddd-module`).

## Commandes
- Build + tests Java : `mvn verify` (depuis `spring-boot-app/`)
- Lancer l'appli en local : `mvn spring-boot:run`
- Terraform (depuis `terraform/envs/dev`) : `terraform fmt -check`, `terraform validate`, `terraform plan`

## Règles
- Toujours lancer les tests avant de proposer un commit.
- Ne jamais committer de secret (clé API, mot de passe, token). Utiliser des variables d'environnement.
- `terraform apply` est **toujours** validé par un humain après lecture du `plan` — jamais automatique.
- Suivre l'architecture DDD décrite dans @docs/architecture.md.
- Pour une revue de code avant commit, utiliser le subagent `code-reviewer`.
- Pour une revue d'infra avant apply, utiliser le subagent `terraform-reviewer`.

## Documentation
Voir `docs/tutoriel-agents-claude-spring-terraform.md` pour le guide complet d'utilisation
des agents Claude, des Skills, des subagents et de Ollama sur ce projet.
