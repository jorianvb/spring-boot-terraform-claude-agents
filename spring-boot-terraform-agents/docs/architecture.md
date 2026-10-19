# Architecture

## Backend : DDD en couches

Chaque module metier (bounded context) est organise ainsi :

```
com.monprojet.<module>/
├── domain/           # entites, value objects, ports (interfaces), sans dependance Spring
├── application/      # use cases (services applicatifs), sans dependance Spring
└── infrastructure/   # adapters JPA, controllers REST, clients HTTP sortants
```

Regles :
- `domain` ne depend de rien d'autre que du JDK (et eventuellement d'une petite librairie de validation).
- `application` orchestre le domaine via les ports, sans savoir comment ils sont implementes.
- `infrastructure` implemente les ports (JPA, HTTP) et expose les controllers REST.

## Infra : Terraform

```
terraform/
├── modules/     # modules reutilisables (reseau, base de donnees, service applicatif...)
└── envs/
    └── dev/     # composition des modules pour l'environnement de dev
```

Le state est stocke dans un backend distant (S3 avec `use_lockfile = true`, verrouillage natif depuis
Terraform 1.10 ; l'ancienne table DynamoDB est depreciee), jamais en local.
Toute application (`terraform apply`) est precedee d'un `terraform plan` relu par un humain
(ou par le subagent `terraform-reviewer`, voir `.claude/agents/terraform-reviewer.md`).
