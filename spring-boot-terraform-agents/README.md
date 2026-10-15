# Spring Boot + Terraform avec agents Claude

Ce depot accompagne le tutoriel **"Créer et utiliser des agents Claude pour un projet Spring Boot + Terraform"**
(du cadrage a la mise en production).

👉 Le tutoriel complet est dans [`docs/tutoriel-agents-claude-spring-terraform.md`](docs/tutoriel-agents-claude-spring-terraform.md).

## Contenu du depot

- `CLAUDE.md` : la memoire de projet lue automatiquement par Claude Code.
- `.claude/skills/` : les Skills du projet (DDD, client REST, JPA, Terraform, revue, securite).
- `.claude/agents/` : les subagents du projet (revue de code, revue Terraform, redaction de tests, audit securite, revue de doc).
- `.github/workflows/claude-review.yml` : revue automatique des pull requests par Claude Code.
- `docs/architecture.md` : l'architecture DDD + Terraform du projet.
- `spring-boot-app/` : squelette de l'application Spring Boot.
- `terraform/` : squelette de l'infrastructure Terraform.

## Demarrer

```bash
npm install -g @anthropic-ai/claude-code
claude
```

Claude Code charge automatiquement `CLAUDE.md`, les Skills et les subagents de ce depot.
