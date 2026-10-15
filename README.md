# Agents Claude — monorepo de tutoriels et projets

Ce dépôt regroupe plusieurs projets qui montrent comment utiliser les agents Claude
(Claude Code, subagents, Skills, Agent SDK, tâches planifiées) sur des cas concrets.

## Commencer ici

👉 [**Tutoriel général : comprendre, créer et gérer des agents Claude (subagents)**](docs/tutoriel-creer-des-agents-claude.md)
— la mécanique de base (anatomie d'un subagent, où le ranger, comment l'invoquer, comment en ajouter un
à un projet existant) avant de plonger dans l'un des deux projets ci-dessous.

## Projets

### [`spring-boot-terraform-agents/`](spring-boot-terraform-agents/)
Développer un projet **Spring Boot (DDD) + infrastructure Terraform**, de la spec à la mise en
production, avec Claude Code, des subagents de revue (code, Terraform, sécurité), des Skills,
l'Agent SDK / le SDK Java, et une option Ollama en local.
👉 [Tutoriel complet](spring-boot-terraform-agents/docs/tutoriel-agents-claude-spring-terraform.md)

### [`travel-planner-agent/`](travel-planner-agent/)
Un système d'agents Claude pour **planifier un voyage soi-même** : recherche de destination,
construction d'itinéraire, veille tarifaire automatisée (tâche planifiée), repérage d'événements
locaux. Ce n'est pas une agence de voyage : aucun agent ne réserve ni ne paie à ta place.
👉 [Tutoriel complet](travel-planner-agent/docs/tutoriel-travel-planner-agent.md)

## Pourquoi un seul dépôt pour deux projets différents ?

Les deux projets utilisent la même "boîte à outils" Claude Code (`CLAUDE.md`, `.claude/agents/`,
`.claude/skills/`, workflows GitHub Actions), appliquée à deux domaines très différents — du code
d'un côté, de la recherche/veille de l'autre. C'est volontaire : voir comment les mêmes briques
s'adaptent à des besoins différents est la meilleure façon de comprendre ce qu'elles font vraiment.

Chaque projet a son propre `CLAUDE.md`, chargé automatiquement par Claude Code quand tu travailles
dans son dossier — les deux ne se mélangent pas.
