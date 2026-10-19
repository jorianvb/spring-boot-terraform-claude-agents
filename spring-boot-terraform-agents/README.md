# Spring Boot + Terraform avec agents Claude

Ce dossier accompagne le tutoriel **"Créer et utiliser des agents Claude pour un projet Spring Boot + Terraform"**
(du cadrage à la mise en production).

👉 Le tutoriel complet est dans [`docs/tutoriel-agents-claude-spring-terraform.md`](docs/tutoriel-agents-claude-spring-terraform.md).

## Contenu

- `CLAUDE.md` : la mémoire de projet lue automatiquement par Claude Code.
- `.claude/skills/` : les Skills du projet (DDD, client REST, JPA, Terraform, revue, sécurité).
- `.claude/agents/` : les subagents du projet (revue de code, revue Terraform, rédaction de tests, audit sécurité, revue de doc).
- `docs/architecture.md` : l'architecture DDD + Terraform du projet.
- `spring-boot-app/` : squelette Spring Boot 4.1 / Java 21 qui compile, avec un exemple d'appel à Claude
  via le SDK Java officiel (`shared/infrastructure/claude/`) et une base PostgreSQL locale (`compose.yaml`).
- `terraform/` : un module `network` (VPC, sous-réseaux, tags obligatoires) et l'environnement `envs/dev`.

Les workflows GitHub de ce projet (revue de PR par Claude, CI) sont dans `.github/workflows/`
**à la racine du dépôt** : GitHub ignore les workflows rangés dans un sous-dossier.

## Démarrer

```bash
# 1. Installer Claude Code (méthode recommandée ; voir le tutoriel pour Windows/Homebrew/npm)
curl -fsSL https://claude.ai/install.sh | bash

# 2. Ouvrir une session dans ce projet
cd spring-boot-terraform-agents
claude
```

Claude Code charge automatiquement `CLAUDE.md`, les Skills et les subagents de ce dossier.

Pour lancer l'application (Java 21, Maven et Docker requis) :

```bash
cd spring-boot-app
docker compose up -d          # PostgreSQL local
export ANTHROPIC_API_KEY=...  # seulement si tu appelles réellement Claude
mvn spring-boot:run
```
