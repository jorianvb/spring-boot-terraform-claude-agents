# Tutoriel : créer et utiliser des agents Claude pour un projet Spring Boot + Terraform (de la spec à la prod)

Ce tutoriel fait suite aux deux tutoriels précédents (Spring Boot dernières versions, et Terraform). Ici, on ajoute la couche "agents IA" : comment utiliser Claude Code, le Agent SDK (API), les Skills, et même Ollama en local, pour accompagner un projet Java/Spring Boot + infra Terraform **du cadrage jusqu'à la mise en production**.

Le but : que tu saches quel outil choisir à quel moment, comment le configurer, et quelles sont les bonnes pratiques pour ne pas te faire piéger (sécurité, coûts, qualité).

---

## Sommaire

1. [Panorama : les différentes façons d'utiliser Claude](#1-panorama)
2. [Installer et configurer Claude Code](#2-installer-claude-code)
3. [Le fichier CLAUDE.md : la mémoire du projet](#3-claudemd)
4. [Les Skills : donner des compétences précises à Claude](#4-skills)
5. [Les Subagents : des agents spécialisés dans ta session](#5-subagents)
6. [Le Agent SDK / l'API Claude : construire un agent dans ton appli](#6-agent-sdk)
7. [Ollama : faire tourner un modèle local à la place (ou en complément) de Claude](#7-ollama)
8. [Cycle de vie complet du projet : de la spec à la prod](#8-cycle-de-vie)
9. [Sécurité, coûts et bonnes pratiques générales](#9-bonnes-pratiques)
10. [Structure de dépôt proposée](#10-structure-depot)
11. [Liens utiles](#11-liens)
12. [3 podcasts pour aller plus loin](#12-podcasts)

---

## 1. Panorama : les différentes façons d'utiliser Claude <a name="1-panorama"></a>

Il y a plusieurs façons bien différentes d'utiliser "un agent Claude". Pour un projet Spring Boot + Terraform, tu vas en réalité combiner plusieurs d'entre elles :

| Outil | C'est quoi | Pour quoi faire ici |
|---|---|---|
| **Claude Code** (CLI) | Un agent en ligne de commande qui lit/écrit des fichiers, lance des commandes, explore ton code | Coder le projet Spring Boot, écrire/relire le Terraform, piloter les tests, faire des revues de PR |
| **Subagents** (dans Claude Code) | Des "mini-agents" spécialisés, avec leur propre prompt et leurs propres outils, qu'on invoque depuis Claude Code | Un agent "revue de code Java", un agent "revue Terraform/sécurité", un agent "rédaction de tests" |
| **Agent SDK** (Python / TypeScript) | Une bibliothèque qui te donne la même boucle d'agent que Claude Code, mais programmable dans ton propre code | Construire un service "agent" qui automatise une tâche métier (ex: un agent qui génère de la doc, triage des tickets) |
| **API Claude (Messages API)**, dont le **SDK Java officiel** | L'API brute pour envoyer des messages à Claude et gérer toi-même les appels d'outils | Intégrer Claude *dans* ton application Spring Boot elle-même (ex: un endpoint qui appelle Claude) |
| **Skills** | Des dossiers de instructions (`SKILL.md`) que Claude charge automatiquement quand c'est pertinent | Standardiser la façon de générer un module DDD, de relire du Terraform, de produire un rapport de sécurité |
| **Ollama** | Un serveur de modèles IA **en local**, compatible avec l'API Claude Code | Travailler hors ligne, sur du code sensible, sans dépendre du cloud |
| **Claude Security** | Un scanner de vulnérabilités basé sur Claude, intégré à Claude Code web | Scanner le code et le Terraform avant la mise en prod |
| **GitHub Actions + `claude-code-action`** | L'intégration officielle de Claude Code dans GitHub | Revue de PR automatique, triage d'issues, correctifs automatiques |

Dans ce tutoriel, on utilise **Claude Code comme chef d'orchestre** (c'est l'outil le plus riche), avec :
- des **subagents** pour les tâches spécialisées (revue, tests, sécurité) ;
- des **Skills** pour standardiser les méthodes ("comment on écrit un module DDD ici", "comment on relit du Terraform ici") ;
- le **Agent SDK / API Java** pour la partie où tu veux que *ton application elle-même* appelle Claude (par exemple un agent métier) ;
- **Ollama** comme option locale, pour les cas où tu ne veux/peux pas appeler le cloud.

---

## 2. Installer et configurer Claude Code <a name="2-installer-claude-code"></a>

Méthode recommandée (installateur natif, mises à jour automatiques) :

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Vérifier
claude --version
claude doctor      # diagnostic de l'installation
```

Alternatives : `brew install --cask claude-code` (macOS), `winget install Anthropic.ClaudeCode` (Windows), ou via npm (`npm install -g @anthropic-ai/claude-code`, nécessite **Node.js 22 ou plus**, et jamais avec `sudo`).

Lance `claude` dans le dossier de ton projet. Au premier lancement, exécute `/init` : Claude Code scanne le projet (Maven/Gradle, structure des packages, conventions) et te propose un premier `CLAUDE.md`.

Commandes à connaître :
- `claude` : démarre une session interactive dans le dossier courant.
- `claude -p "..."` : exécute un prompt en mode non-interactif (utile en script/CI).
- `/install-github-app` (en session) : installe l'app GitHub officielle sur ton repo.
- `/agents` (en session) : selon la version, affiche un rappel ou un gestionnaire des subagents. Dans les versions récentes, on crée/modifie un subagent en éditant directement `.claude/agents/` (ou en demandant à Claude de le faire).

> ⚠️ Vérifie toujours la syntaxe exacte des commandes/flags dans `claude --help` ou la doc officielle : elles évoluent vite d'une version à l'autre de Claude Code.

Référence officielle : [installation de Claude Code](https://code.claude.com/docs/en/setup) et [guide d'installation complet (13 étapes, FR)](https://tech-insider.org/fr/?p=2893).

---

## 3. Le fichier CLAUDE.md : la mémoire du projet <a name="3-claudemd"></a>

`CLAUDE.md`, à la racine du projet, est lu automatiquement par Claude Code à chaque démarrage de session. C'est l'endroit où tu mets :

- l'architecture du projet (ex : "DDD avec `domain/`, `application/`, `infrastructure/`") ;
- les commandes à connaître (`mvn test`, `terraform plan`) ;
- les conventions de code (nommage, format des commits) ;
- la séquence à suivre pour un changement (format → lint → test) ;
- ce qu'il **ne faut jamais faire** (ex : "ne jamais appliquer `terraform apply` sans un `plan` validé par un humain").

### Règle d'or : rester sous ~200 lignes

La documentation officielle recommande de garder `CLAUDE.md` sous les 200 lignes : au-delà, les instructions importantes se diluent et Claude commence à les ignorer. Si le fichier grossit, découpe-le avec des imports :

```markdown
# CLAUDE.md

Pour l'architecture : @docs/architecture.md
Pour les conventions de code Java : @docs/conventions-java.md
Pour les règles Terraform : @docs/conventions-terraform.md
```

Tu peux aussi avoir des `CLAUDE.md` par sous-dossier (ex: `spring-boot-app/CLAUDE.md`, `terraform/CLAUDE.md`) : ils se chargent automatiquement quand Claude travaille dans ce dossier, sans polluer le reste.

Et `CLAUDE.local.md` (à ajouter dans `.gitignore`) pour tes réglages personnels, non partagés avec l'équipe.

**Exemple minimal pour ce projet :**

```markdown
# CLAUDE.md

## Projet
API Spring Boot (DDD) + infra Terraform (AWS). Backend Java 21 / Spring Boot 4.x.

## Commandes
- Build + tests : `mvn verify`
- Lancer en local : `mvn spring-boot:run`
- Terraform (dans terraform/envs/dev) : `terraform fmt -check`, `terraform validate`, `terraform plan`

## Règles
- Toujours lancer les tests avant de proposer un commit.
- Ne jamais committer de secret (clé API, mot de passe). Utiliser les variables d'environnement.
- `terraform apply` est **toujours** validé par un humain après lecture du `plan`.
- Suivre l'architecture DDD : domain/application/infrastructure (voir @docs/architecture.md).
```

Sources : [CLAUDE.md best practices (en)](https://techsy.io/en/blog/claude-md-best-practices), [Claude Code project structure best practices](https://uxplanet.org/claude-code-project-structure-best-practices-5a9c3c97f121), [guide mémoire Claude Code (FR)](https://institute.sfeir.com/fr/claude-code/claude-code-le-systeme-de-memoire-claude-md/erreurs/).

---

## 4. Les Skills : donner des compétences précises à Claude <a name="4-skills"></a>

### C'est quoi

Une **Skill** est un dossier contenant au minimum un fichier `SKILL.md` :

```
.claude/skills/
└── ddd-module/
    ├── SKILL.md          # instructions principales
    └── reference.md      # détails supplémentaires (chargés seulement si besoin)
```

Le `SKILL.md` a un en-tête YAML qui dit **quand** se déclencher, et un corps qui dit **quoi faire** :

```markdown
---
name: ddd-module
description: À utiliser quand on crée un nouveau module métier (bounded context) dans l'application Spring Boot DDD. Ne pas utiliser pour une simple classe utilitaire.
---

# Créer un module DDD

Quand on te demande de créer un nouveau module métier :
1. Crée les packages `domain`, `application`, `infrastructure` sous `com.monprojet.<module>`.
2. Dans `domain`, mets les entités, value objects et le port du repository (interface).
3. Dans `application`, mets les use cases (services applicatifs), sans dépendance à Spring.
4. Dans `infrastructure`, mets l'implémentation JPA du repository et le controller REST.
5. Écris un test unitaire du domaine et un test du use case avec mock du port.
```

Claude charge le `SKILL.md` **seulement si la description correspond à la demande** — ça évite de surcharger le contexte en permanence. Pour des Skills plus riches, tu peux renvoyer vers des fichiers annexes (ex: `forms.md`) que Claude ne lit que s'il en a besoin.

### Où les ranger

- `.claude/skills/` à la racine du projet : partagées avec l'équipe via Git.
- `~/.claude/skills/` : personnelles, disponibles sur tous tes projets.
- Les Skills sont aussi disponibles sur claude.ai, dans l'Agent SDK et via l'API — pas seulement dans Claude Code.

### Skills utiles à créer pour ce projet

| Skill | Rôle |
|---|---|
| `ddd-module` | Générer un nouveau module métier DDD (domain/application/infrastructure) |
| `spring-rest-client` | Générer un client HTTP sortant avec `@HttpExchange` (interface déclarative Spring 6) + tests avec `MockWebServer` |
| `jpa-entity` | Générer une entité JPA + repository Spring Data + migration Flyway/Liquibase |
| `terraform-module` | Générer un module Terraform (variables, outputs, conventions de nommage, tags obligatoires) |
| `terraform-review` | Relire un plan Terraform : vérifier les ressources détruites, les changements de taille d'instance, les coûts, les tags manquants |
| `security-review` | Lancer une revue de sécurité ciblée (injections, secrets en dur, CORS, auth) avant une mise en prod |

Pas besoin d'écrire une Skill de revue de code générique : la revue d'un diff est confiée au subagent `code-reviewer` (section 5), et Claude Code embarque déjà une Skill `/code-review`.

Il existe aussi des Skills "communautaires" déjà prêtes à l'emploi, par exemple une Skill *Terraform Infrastructure as Code*, installable avec l'outil communautaire `skills` (pas un outil Anthropic — lis toujours le contenu d'une Skill tierce avant de l'installer) :

```bash
npx -y skills add manutej/luxor-claude-marketplace --skill terraform-infrastructure-as-code --agent claude-code
```

### Bonnes pratiques Skills

1. **Une tâche = une Skill.** Mieux vaut plusieurs petites Skills ciblées qu'une seule énorme.
2. **Soigne la `description`.** C'est elle qui décide quand la Skill se déclenche. Ajoute toujours une phrase "ne pas utiliser pour...".
3. **Teste le déclenchement** : essaie plusieurs formulations qui doivent l'activer, et plusieurs qui ne doivent pas.
4. **Sécurité** : si tu installes une Skill trouvée sur Internet, lis-la avant — une Skill peut contenir du code exécutable.

Sources : [Agent Skills — vue d'ensemble officielle](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Skills dans Claude Code](https://code.claude.com/docs/en/skills), [Agent Skills dans le SDK](https://code.claude.com/docs/en/agent-sdk/skills), [blog Anthropic — Equipping agents with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills).

---

## 5. Les Subagents : des agents spécialisés dans ta session <a name="5-subagents"></a>

### Différence avec les Skills

Une **Skill** dit "comment faire une tâche". Un **Subagent** est carrément un *agent séparé* : son propre prompt système, son propre jeu d'outils autorisés, et éventuellement son propre modèle — qui tourne dans un contexte isolé de ta conversation principale, pour ne pas la polluer avec tous les résultats intermédiaires.

Claude Code a des subagents intégrés (`Explore`, `Plan`, `general-purpose`), et tu peux en créer des personnalisés : ce sont des fichiers Markdown avec un en-tête YAML.

```
.claude/agents/
├── code-reviewer.md
├── terraform-reviewer.md
└── test-writer.md
```

Exemple `.claude/agents/terraform-reviewer.md` :

```markdown
---
name: terraform-reviewer
description: Relit un plan ou un diff Terraform avant un apply. Utiliser PROACTIVEMENT après toute modification de fichiers .tf.
tools: Read, Grep, Bash
model: sonnet
skills: terraform-review
---

Tu es un ingénieur infra senior spécialisé Terraform/AWS.
Quand on t'invoque :
1. Lance `terraform plan` et lis la sortie.
2. Vérifie : ressources détruites, changements de taille/type d'instance, absence de tags obligatoires, secrets en dur.
3. Donne un verdict clair : OK pour apply / à corriger, avec la liste des points bloquants.
```

- `model` accepte un alias (`sonnet`, `opus`, `haiku`, `fable`), un identifiant complet (ex : `claude-sonnet-5`) ou `inherit` (même modèle que la session principale).
- `skills` **précharge** le contenu d'une Skill dans le contexte du subagent dès son démarrage. Un subagent ne voit pas les Skills déjà utilisées dans ta conversation : sans ce champ, il peut encore les découvrir via l'outil Skill, mais le préchargement rend le format de sortie beaucoup plus fiable.
- `.claude/agents/` (projet) : disponible pour toute l'équipe, versionné.
- `~/.claude/agents/` (utilisateur) : disponible sur tous tes projets perso.
- Par défaut, un subagent peut lui-même lancer des subagents, jusqu'à 3 niveaux sous la conversation principale (réglable avec la variable `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` ; `1` désactive l'imbrication). Pour l'interdire à un subagent précis, retire l'outil `Agent` de sa liste `tools`.

### Comment on les invoque

- Automatiquement, quand ta demande correspond à la `description` du subagent.
- En le nommant dans le prompt : `claude -p "Utilise le subagent terraform-reviewer sur le dossier terraform/envs/dev"`.
- Par @-mention en session : tape `@` et choisis le subagent dans la liste (ex : `@agent-terraform-reviewer relis envs/dev`).
- Pour toute une session : `claude --agent terraform-reviewer`.

### Exemples utiles pour ce projet

| Subagent | Outils autorisés | Rôle |
|---|---|---|
| `code-reviewer` | Read, Grep, Bash (tests) | Relire un diff Java avant de committer |
| `terraform-reviewer` | Read, Grep, Bash (`terraform plan`) | Relire l'infra avant un apply |
| `test-writer` | Read, Write, Bash | Écrire les tests manquants sur un module |
| `security-auditor` | Read, Grep, Bash | Revue de sécurité ciblée avant mise en prod |
| `doc-reviewer` | Read, Grep (pas d'écriture) | Relire la doc sans jamais pouvoir la modifier par erreur |

**Piège classique à éviter** : donner trop d'autonomie trop tôt (`--dangerously-skip-permissions` / `bypassPermissions`) — réserve ça à des environnements de test, jamais à de la prod ou des credentials réels.

Sources : [Create custom subagents — doc officielle](https://code.claude.com/docs/en/sub-agents), [Subagents dans le SDK](https://code.claude.com/docs/en/agent-sdk/subagents), [guide FR pas-à-pas (12 étapes)](https://tech-insider.org/fr/?p=2893).

---

## 6. Le Agent SDK / l'API Claude : construire un agent dans ton appli <a name="6-agent-sdk"></a>

Ici on change de registre : ce n'est plus toi qui pilotes Claude Code dans un terminal, c'est **ton application (ou un script) qui appelle Claude par programme**.

### 6.1 Agent SDK (Python / TypeScript) — pour un agent autonome

Le **Agent SDK** (ex-"Claude Code SDK", renommé) te donne la même boucle d'agent que Claude Code (lire des fichiers, exécuter des commandes, chercher sur le web...) mais dans ton propre script Python ou TypeScript.

```bash
# Python 3.10+ (le paquet embarque Claude Code, rien d'autre à installer)
python -m venv .venv && source .venv/bin/activate
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

Exemple minimal (Python) — `query()` est asynchrone, il faut donc l'appeler depuis une fonction `async` lancée avec `asyncio.run()` (un `async for` écrit directement au niveau du script provoque une `SyntaxError`) :

```python
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query


async def main() -> None:
    options = ClaudeAgentOptions(
        cwd=".",                         # dossier du projet
        setting_sources=["project"],     # charge CLAUDE.md, .claude/agents/ et .claude/skills/
        permission_mode="dontAsk",       # sans humain pour valider : tout ce qui n'est pas autorisé est refusé
        allowed_tools=["Read", "Grep", "Glob"],  # lecture seule
        max_turns=20,                    # disjoncteur
    )
    async for message in query(
        prompt="Relis le module de paiement et liste les risques de sécurité",
        options=options,
    ):
        if isinstance(message, ResultMessage):   # le message final, avec le résultat et le coût
            print(message.result)


asyncio.run(main())
```

Sans `permission_mode`/`allowed_tools`, un script lancé sans humain (cron, CI) ne peut pas valider les demandes de permission : les outils qui écrivent ou exécutent des commandes sont alors bloqués. Les scripts de `travel-planner-agent/agent-sdk/` et `photo-storage-agent/agent-sdk/` de ce dépôt montrent un réglage complet (écriture limitée à un dossier avec `Edit(/reports/**)`, plafond de coût `max_budget_usd`).

Cas d'usage typiques pour ce projet :
- un agent planifié (cron) qui scanne le dépôt chaque nuit et ouvre un rapport ;
- un agent qui génère la documentation d'API à partir du code à chaque release ;
- un agent qui triage les tickets d'un board Jira/GitHub.

Attention : pour un agent construit avec ce SDK, authentifie-toi avec une **clé API** (`ANTHROPIC_API_KEY`) créée dans le Claude Console. Sauf accord préalable d'Anthropic, un produit tiers ne doit pas proposer la connexion claude.ai (ni réutiliser ses quotas d'abonnement).

Sources : [Agent SDK — vue d'ensemble](https://code.claude.com/docs/en/agent-sdk/overview), [référence Python](https://code.claude.com/docs/en/agent-sdk/python), [permissions dans le SDK](https://code.claude.com/docs/en/agent-sdk/permissions).

### 6.2 L'API Claude "brute" (Messages API) — pour intégrer Claude *dans* Spring Boot

Si tu veux que **ton application Spring Boot elle-même** appelle Claude (par exemple un endpoint `/support/analyser-ticket` qui invoque Claude avec tool-use), tu utilises directement l'API Messages, via le **SDK Java officiel**.

```xml
<dependency>
  <groupId>com.anthropic</groupId>
  <artifactId>anthropic-java</artifactId>
  <version>2.73.0</version>
</dependency>
```

Exemple autonome (Java 17+, comme Spring Boot 4) :

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlock;
import java.util.stream.Collectors;

public class ExempleClaude {
    public static void main(String[] args) {
        String texteDuTicket = "Le client ne reçoit plus les emails de confirmation depuis lundi.";

        AnthropicClient client = AnthropicOkHttpClient.fromEnv(); // lit ANTHROPIC_API_KEY

        MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_SONNET_5)
                .maxTokens(1024L)
                .addUserMessage("Résume ce ticket client en 3 points : " + texteDuTicket)
                .build();

        Message message = client.messages().create(params);

        // La réponse est une liste de blocs (texte, appel d'outil...) : on garde le texte.
        String resume = message.content().stream()
                .flatMap(bloc -> bloc.text().stream())
                .map(TextBlock::text)
                .collect(Collectors.joining("\n"));
        System.out.println(resume);

        client.close();
    }
}
```

Côté Spring Boot, le plus propre est d'encapsuler ça dans un `@Service`, avec un seul client déclaré comme `@Bean` (il est fait pour être réutilisé) et la clé API lue depuis l'environnement, jamais en dur dans le code. C'est exactement ce que fait le squelette de ce dépôt (compilé et testé en CI) :

- [`ClaudeProperties.java`](../spring-boot-app/src/main/java/com/monprojet/shared/infrastructure/claude/ClaudeProperties.java) — un `record` `@ConfigurationProperties(prefix = "anthropic")` ;
- [`ClaudeConfig.java`](../spring-boot-app/src/main/java/com/monprojet/shared/infrastructure/claude/ClaudeConfig.java) — le `@Bean AnthropicClient` ;
- [`ClaudeAssistantService.java`](../spring-boot-app/src/main/java/com/monprojet/shared/infrastructure/claude/ClaudeAssistantService.java) — le service qui appelle Claude.

```yaml
anthropic:
  api-key: ${ANTHROPIC_API_KEY:}   # ":" = valeur vide par défaut, l'appli démarre même sans clé
  model: claude-sonnet-5
  max-tokens: 1024
```

Avec le **tool use** (appel d'outils), l'API *bêta* du SDK Java (`com.anthropic.models.beta.messages.MessageCreateParams`) peut dériver automatiquement un outil à partir d'une classe Java (`addTool(MaClasse.class)` : la classe décrit les paramètres de l'outil), et le `BetaToolRunner` peut même gérer la boucle d'appels pour toi. Comme c'est une API bêta, vérifie la doc du SDK avant de t'appuyer dessus en production.

**Différence clé à retenir** :
- **Agent SDK** = un agent complet (Claude Code) avec ses outils intégrés (fichiers, shell, web) → pour un agent autonome, type script/service dédié.
- **API Messages (SDK Java)** = un appel de modèle, avec tes propres outils métier → pour intégrer Claude *dans* ta logique métier Spring Boot existante.

Sources : [Java SDK — doc officielle](https://platform.claude.com/docs/en/api/sdks/java), [dépôt GitHub anthropic-sdk-java](https://github.com/anthropics/anthropic-sdk-java), [tool use avec l'API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

---

## 7. Ollama : faire tourner un modèle local <a name="7-ollama"></a>

Depuis janvier 2026, **Ollama expose une API compatible avec l'API Anthropic Messages** (`/v1/messages`). Concrètement, ça veut dire que **Claude Code peut pointer vers un modèle local** tournant sur ta machine, au lieu du cloud Anthropic.

### Pourquoi faire ça

- travailler **hors ligne** ;
- garder du code sensible **entièrement local** (pas d'appel réseau) ;
- réduire les coûts sur des tâches simples et répétitives ;
- offrir un service LLM self-hosted à toute une équipe sans que chacun gère sa propre installation.

### Installation rapide

```bash
# installer Ollama (voir ollama.com). L'application de bureau démarre le serveur toute seule ;
# sinon, lance-le dans un terminal à part AVANT le pull :
ollama serve                      # serveur local sur le port 11434 (laisse ce terminal ouvert)

# dans un autre terminal :
ollama pull qwen3-coder          # un modèle orienté code
```

Pointer Claude Code vers Ollama :

```bash
export ANTHROPIC_BASE_URL="http://localhost:11434"
export ANTHROPIC_AUTH_TOKEN="ollama"   # valeur bidon, Ollama ne vérifie pas en local

claude --model qwen3-coder
```

Ollama propose aussi une commande `ollama launch` qui configure l'environnement et lance directement un outil agentique (Claude Code ou un autre) pointé sur un modèle local. La syntaxe exacte (nom de la sous-commande, du modèle) évolue vite selon la version d'Ollama — vérifie `ollama launch --help` ou la [doc officielle de compatibilité Anthropic](https://docs.ollama.com/api/anthropic-compatibility) avant de copier une commande trouvée sur un blog.

### Limites à connaître (important)

Les retours d'expérience (début 2026) sont clairs : **Claude Code + modèle local n'est pas encore au niveau de Claude Code + Claude cloud** pour les tâches agentiques complexes (gestion fine des todos, outils avancés, grands contextes). Ça fonctionne bien pour :
- de la génération de code simple et ciblée ;
- du travail hors ligne ponctuel ;
- des tâches répétitives à faible enjeu.

Mais pour du refactoring complexe, de la revue d'architecture ou du pilotage multi-fichiers, le modèle cloud reste nettement plus fiable en 2026. Une bonne pratique vue dans la communauté : avoir deux alias, et basculer selon le besoin.

```bash
alias claude-local='ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama claude --model qwen3-coder'
alias claude-cloud='claude'   # usage normal, cloud Anthropic
```

Sources : [Ollama supporte maintenant Claude Code (FR)](https://angelo-lima.fr/fr/claude-code-ollama-local-llm/), [Ollama en 2026 : état des lieux (FR)](https://angelo-lima.fr/fr/ollama-2026-etat-des-lieux/), [Run LLMs Locally with Ollama in 2026](https://dev.to/cursuri-ai/run-llms-locally-with-ollama-in-2026-the-practical-developer-guide-48n), [retour d'expérience critique — dev.classmethod.jp](https://dev.classmethod.jp/en/articles/claude-code-ollama-local/), [Ollama + Claude Code : guide pas à pas](https://betterstack.com/community/guides/ai/ollama-local-llm/).

---

## 8. Cycle de vie complet du projet : de la spec à la prod <a name="8-cycle-de-vie"></a>

Maintenant qu'on a vu les outils, voici comment les enchaîner sur un vrai projet Spring Boot (API métier DDD) + Terraform (infra AWS).

### 8.1 Cadrage et spécification

- Ouvre une session Claude (app ou Claude Code) en lui donnant le contexte métier et demande-lui de produire : user stories, critères d'acceptation, modèle de domaine (entités, agrégats) sous forme de diagramme textuel.
- Utilise un **Project** (claude.ai) avec des instructions personnalisées si plusieurs personnes collaborent sur le cadrage — le contexte métier est conservé entre les sessions.
- Garde une trace de ces specs dans `docs/specs/` du dépôt : Claude Code pourra ensuite s'en servir comme référence pendant le développement (ajoute-les en lien dans `CLAUDE.md`).

### 8.2 Développement Spring Boot avec Claude Code

1. `claude` dans le dossier du projet, avec le `CLAUDE.md` déjà en place (section 3).
2. Pour un nouveau module métier : "Utilise la Skill ddd-module pour créer le module Commandes" → Claude lit la Skill, génère domain/application/infrastructure.
3. Pour la revue avant commit : invoque le subagent `code-reviewer`.
4. Pour les tests manquants : invoque le subagent `test-writer`.
5. Pour les appels API sortants/entrants : utilise la Skill `spring-rest-client` (client déclaratif `@HttpExchange`) côté sortant, et demande à Claude de générer les contrôleurs + la doc OpenAPI côté entrant.
6. Reste **dans une boucle courte** : décrire l'objectif → laisser Claude proposer un plan → relire le diff → tester → committer. Évite de laisser tourner un agent "en autonomie totale" sur un gros refactor sans checkpoint.

### 8.3 Infrastructure Terraform avec Claude

1. Demande à Claude de générer un module Terraform à partir d'une description ("un cluster ECS Fargate + RDS Postgres + un ALB"), avec la Skill `terraform-module` pour forcer les conventions (nommage, tags, variables).
2. **Jamais d'`apply` automatique** : le flux recommandé est Claude génère → `terraform plan` → relecture humaine (ou subagent `terraform-reviewer`) → `apply` manuel ou via pipeline avec approbation.
3. Pour une revue poussée, le subagent `terraform-reviewer` (section 5) vérifie les destructions de ressources, les tags manquants, les risques de coût.
4. Garde le state Terraform dans un backend distant (S3, avec `use_lockfile = true` pour le verrouillage natif depuis Terraform 1.10 — l'ancienne table DynamoDB n'est plus nécessaire) — ça n'a rien à voir avec Claude, mais c'est indispensable avant de laisser un agent toucher à l'infra. Exemple commenté dans `terraform/envs/dev/main.tf`.

### 8.4 Intégration continue (CI) et revue automatique de PR

Le plus simple : dans une session Claude Code ouverte dans ton dépôt, tape la commande `/install-github-app` (il faut la [CLI GitHub](https://cli.github.com) installée et connectée avec `gh auth login`). Elle installe l'app GitHub Claude, crée le secret et prépare la PR avec les workflows.

Ou manuellement, avec un workflow `.github/workflows/claude-review.yml` (version utilisée dans ce dépôt) :

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize, ready_for_review, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: read
      issues: read
      id-token: write   # requis par l'authentification par défaut de l'action
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 1
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          plugin_marketplaces: "https://github.com/anthropics/claude-code.git"
          plugins: "code-review@claude-code-plugins"
          prompt: "/code-review:code-review --comment ${{ github.repository }}/pull/${{ github.event.pull_request.number }}"
          claude_args: '--allowedTools "mcp__github_inline_comment__create_inline_comment"'
```

> ⚠️ **Monorepo** : GitHub n'exécute que les workflows placés dans `.github/workflows/` **à la racine du dépôt**. Un workflow rangé dans `spring-boot-terraform-agents/.github/workflows/` n'est jamais lancé. Dans ce dépôt, les workflows sont donc à la racine, avec un filtre `paths:` pour ne réagir qu'aux changements du bon projet.

Ce que ça apporte :
- une revue automatique sur chaque PR (bugs, failles de sécurité), postée en commentaires sur la PR grâce à `--comment` ;
- avec un second workflow (`examples/claude.yml` de l'action), la possibilité de mentionner `@claude` dans un commentaire d'issue/PR pour lui demander une action ;
- ce workflow de revue n'a que des droits de **lecture** sur le code (`contents: read`) — c'est volontaire, pour garder un humain dans la boucle.

Tu peux avoir un second workflow, plus permissif, qui laisse Claude ouvrir une PR de correctif quand on le lui demande explicitement (`@claude corrige ce bug`), toujours avec une revue humaine avant merge.

### 8.5 Sécurité avant la mise en prod

- **`/security-review`** dans Claude Code : commande intégrée qui lance une revue de sécurité ciblée (injections SQL, secrets en dur, CORS, etc.) sur le code modifié.
- **Claude Security** (bêta) : un outil séparé, accessible depuis Claude.ai, qui scanne un dépôt entier, trace les flux de données, propose des correctifs, avec un score de confiance — à réserver aux dépôts que tu es autorisé à scanner (jamais du code tiers sans droit).
- Pour le Terraform : vérifie en plus que les règles de sécurité réseau (security groups, IAM) sont bien revues — un agent IA génère du Terraform syntaxiquement correct, mais la relecture humaine des permissions reste indispensable.

### 8.6 Mise en production et exploitation

- Le déploiement lui-même (pipeline `terraform apply` + déploiement de l'artefact Spring Boot) reste piloté par ton pipeline CI/CD habituel (GitHub Actions, GitLab CI...) — Claude t'aide à l'écrire et à le relire, pas à appuyer sur le bouton de prod à ta place.
- Une fois en prod, un agent planifié (cron + Agent SDK, ou scheduled task) peut :
  - relire les logs d'erreurs et ouvrir un ticket résumant les incidents récurrents ;
  - vérifier chaque nuit que le Terraform appliqué correspond au code versionné (`terraform plan` ne doit rien montrer) ;
  - générer un changelog à partir des commits/PR fusionnées.

---

## 9. Sécurité, coûts et bonnes pratiques générales <a name="9-bonnes-pratiques"></a>

- **Jamais d'autonomie totale par défaut.** Réserve les modes "sans confirmation" à des environnements jetables/test.
- **Permissions du moins au plus.** Un subagent de revue ne doit avoir que `Read`/`Grep`, pas `Write`/`Bash` avec accès large.
- **Jamais de secret en dur**, ni dans le code, ni dans un prompt, ni commité dans `CLAUDE.md`.
- **Terraform : toujours `plan` avant `apply`**, et jamais d'`apply` automatique sans validation humaine en production.
- **Coût des subagents.** Chaque subagent consomme son propre contexte/tokens — à utiliser quand ça apporte une vraie isolation, pas par réflexe.
- **CLAUDE.md compact** (sous les 200 lignes), découpé en imports si besoin, pour que Claude continue de suivre tes règles.
- **Teste tes Skills et subagents** avec plusieurs formulations, pour vérifier qu'ils se déclenchent (et ne se déclenchent pas) au bon moment.
- **Versionne tout.** `.claude/agents/`, `.claude/skills/`, `CLAUDE.md` vont dans Git, au même titre que le code — c'est ce qui permet à toute l'équipe de bénéficier des mêmes agents.
- **Pin les versions.** `required_providers` en Terraform, versions explicites en Maven, image Docker avec tag précis plutôt que `latest` — pour que le projet reste reproductible, agent IA ou pas.

---

## 10. Structure de dépôt proposée <a name="10-structure-depot"></a>

```
(racine du dépôt)
├── .github/workflows/
│   ├── claude-review.yml          # revue de PR par Claude (doit être à la racine)
│   └── ci.yml                     # compile/valide le code des tutoriels
└── spring-boot-terraform-agents/
    ├── CLAUDE.md
    ├── .claude/
    │   ├── agents/
    │   │   ├── code-reviewer.md
    │   │   ├── terraform-reviewer.md
    │   │   ├── test-writer.md
    │   │   ├── security-auditor.md
    │   │   └── doc-reviewer.md
    │   └── skills/
    │       ├── ddd-module/SKILL.md
    │       ├── spring-rest-client/SKILL.md
    │       ├── jpa-entity/SKILL.md
    │       ├── terraform-module/SKILL.md
    │       ├── terraform-review/SKILL.md
    │       └── security-review/SKILL.md
    ├── docs/
    │   ├── specs/                 # à créer pour tes specs
    │   └── architecture.md
    ├── spring-boot-app/
    │   ├── pom.xml                # Spring Boot 4.1, Java 21, SDK Java Anthropic
    │   ├── compose.yaml           # PostgreSQL local
    │   └── src/main/java/com/monprojet/...
    └── terraform/
        ├── modules/network/       # VPC + sous-réseaux, tags obligatoires
        └── envs/dev/
```

---

## 11. Liens utiles <a name="11-liens"></a>

**Claude Code & subagents**
- [Create custom subagents (doc officielle)](https://code.claude.com/docs/en/sub-agents)
- [Subagents dans l'Agent SDK](https://code.claude.com/docs/en/agent-sdk/subagents)
- [Installation de Claude Code](https://code.claude.com/docs/en/setup)
- [Guide FR pas-à-pas des sous-agents (12 étapes)](https://tech-insider.org/fr/?p=2893)

**Agent SDK & API**
- [Agent SDK — vue d'ensemble officielle](https://code.claude.com/docs/en/agent-sdk/overview)
- [Agent SDK — référence Python](https://code.claude.com/docs/en/agent-sdk/python)
- [Agent SDK — permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- [SDK Java officiel — documentation](https://platform.claude.com/docs/en/api/sdks/java)
- [Dépôt GitHub du SDK Java](https://github.com/anthropics/anthropic-sdk-java)
- [Dépôt GitHub du SDK Python (Agent SDK)](https://github.com/anthropics/claude-agent-sdk-python)

**Skills**
- [Agent Skills — vue d'ensemble officielle](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Agent Skills dans le SDK](https://code.claude.com/docs/en/agent-sdk/skills)
- [Blog Anthropic — Equipping agents with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [Skill communautaire Terraform (marketplace)](https://claudemarketplaces.com/skills/manutej/luxor-claude-marketplace/terraform-infrastructure-as-code)

**CLAUDE.md**
- [CLAUDE.md best practices (en)](https://techsy.io/en/blog/claude-md-best-practices)
- [Claude Code project structure best practices](https://uxplanet.org/claude-code-project-structure-best-practices-5a9c3c97f121)
- [Le système de mémoire CLAUDE.md, erreurs à éviter (FR)](https://institute.sfeir.com/fr/claude-code/claude-code-le-systeme-de-memoire-claude-md/erreurs/)

**Ollama**
- [Ollama supporte maintenant Claude Code (FR)](https://angelo-lima.fr/fr/claude-code-ollama-local-llm/)
- [Ollama en 2026 : état des lieux (FR)](https://angelo-lima.fr/fr/ollama-2026-etat-des-lieux/)
- [Run LLMs Locally with Ollama in 2026](https://dev.to/cursuri-ai/run-llms-locally-with-ollama-in-2026-the-practical-developer-guide-48n)
- [Retour d'expérience critique sur Claude Code + Ollama](https://dev.classmethod.jp/en/articles/claude-code-ollama-local/)

**GitHub Actions / CI-CD**
- [Claude Code GitHub Actions — doc officielle](https://code.claude.com/docs/en/github-actions)
- [Claude Code GitHub Action — présentation](https://www.promptlayer.com/glossary/claude-code-github-action)
- [Intégrer Claude Code dans un workflow GitHub](https://chamith.medium.com/how-we-integrated-claude-code-into-our-github-workflow-97a5db8bcb8e)

**Sécurité**
- [Claude Security — bêta publique (FR)](https://www.blogdumoderateur.com/claude-security-detecte-vulnerabilites-code-disponible-beta-publique/)
- [Guide Claude Code Security (FR)](https://agence-scroll.com/blog/claude-code-security-securisez-le-code-de-votre-entreprise)

**Terraform avec IA (contexte général)**
- [Using Claude to Write Terraform Infrastructure as Code](https://www.guvi.in/blog/?p=128845)

---

## 12. Trois podcasts pour aller plus loin <a name="12-podcasts"></a>

1. **"The future of agentic coding with Claude Code"** (Anthropic, YouTube) — une bonne introduction à ce qu'est Claude Code et pourquoi ce type d'outil change le développement logiciel.
   👉 https://www.youtube.com/watch?v=iF9iV4xponk

2. **"How to Use Claude Code Like the People Who Built It"** (podcast *AI & I*, avec Boris Cherny et Cat Wu, les créateurs de Claude Code chez Anthropic — YouTube/Spotify/Apple Podcasts) — ils racontent comment Claude Code est né en interne, et donnent leurs astuces sur les subagents et les commandes favorites.
   👉 https://www.youtube.com/watch?v=IDSAMqip6ms

3. **"OpenTofu, with Ohad Maislish"** (Kubernetes Podcast from Google — Spotify/Apple Podcasts) — pour comprendre les enjeux actuels de l'écosystème Infrastructure as Code (Terraform/OpenTofu), utile en complément de la partie Terraform de ce tutoriel.
   👉 Page de l'épisode : https://kubernetespodcast.com/episode/232-opentofu/
   👉 Spotify (chaîne du podcast) : https://open.spotify.com/show/0AsnxlMtXRUEeZkIO0ScpJ

---

*Rappel : les fonctionnalités de Claude évoluent vite. Si un nom de menu, une commande ou une URL a changé depuis la rédaction de ce tutoriel, cherche un terme proche dans la documentation officielle (docs.claude.com / code.claude.com).*

---

## Note de vérification

Ce tutoriel a été relu et confronté à la documentation officielle (docs.claude.com, code.claude.com, platform.claude.com, docs.ollama.com, spring.io) après une première rédaction. Les points suivants ont été corrigés à la suite de cette vérification :

- la gestion des subagents en session passe par `/agents`, pas par une commande `claude agents` ;
- l'imbrication de subagents n'est **pas** interdite par défaut (elle est limitée en profondeur et configurable selon la version de Claude Code) ;
- la taille recommandée de `CLAUDE.md` est "sous ~200 lignes" (pas une fourchette 150-200) ;
- Ollama n'utilise pas `ANTHROPIC_API_KEY` pour la compatibilité Messages API, seulement `ANTHROPIC_BASE_URL` et `ANTHROPIC_AUTH_TOKEN` ;
- la syntaxe exacte de `ollama launch` et du prompt de revue de PR (`/review` vs un skill dédié) dépend de la version installée — à vérifier localement plutôt qu'à copier tel quel ;
- `@HttpExchange` est une façade déclarative au-dessus de `RestClient`/`WebClient`, pas un remplacement bas niveau de `RestTemplate`.

### Deuxième vérification (octobre 2026)

Le dépôt a été relu une seconde fois, en testant le code avec de vrais outils (compilation Java en CI, `terraform validate`, `py_compile` + import du SDK Python, `shellcheck`, `actionlint`, vérification des liens et ancres Markdown). Corrections apportées :

- **workflows GitHub inactifs** : ils étaient rangés dans les sous-dossiers des projets, où GitHub ne les lit jamais. Ils sont maintenant dans `.github/workflows/` à la racine, avec un filtre `paths:` ;
- **revue de PR** : `prompt: "/review"` remplacé par le plugin officiel `code-review` (`/code-review:code-review --comment ...`), avec la permission `id-token: write` et `actions/checkout@v6`, comme dans la doc officielle ;
- **installation** : l'installateur natif (`curl -fsSL https://claude.ai/install.sh | bash`) est la méthode recommandée ; npm reste possible avec Node.js 22+ ;
- **exemple Python** : un `async for` au niveau du script est une erreur de syntaxe — l'exemple est maintenant enveloppé dans `async def main()` + `asyncio.run(main())` ;
- **scripts Agent SDK** : ajout de `permission_mode="dontAsk"` + `allowed_tools` (sinon les outils d'écriture sont bloqués en tâche planifiée), `setting_sources`, `max_turns`, `max_budget_usd`, et un code de sortie non nul en cas d'échec ;
- **SDK Java** : version 2.73.0, exemple complet qui compile (extraction du texte de la réponse), et précision que la dérivation d'outil depuis une classe est dans l'API **bêta** ;
- **squelette Spring Boot** : passage à Spring Boot 4.1 (`spring-boot-starter-webmvc`, starter Flyway), ajout de la classe `Application`, du plugin Maven (sans lui `mvn spring-boot:run` ne fonctionne pas), du service Claude et d'un test unitaire ;
- **Terraform** : le module `network` était vide (`main.tf`/`outputs.tf` à 0 ligne) et n'était pas appelé ; il contient maintenant un VPC avec tags obligatoires, et le provider AWS passe en `~> 6.0` ; le verrouillage du state S3 utilise `use_lockfile` (DynamoDB est déprécié) ;
- **Skills** : la ligne `code-review` du tableau renvoyait vers une Skill inexistante ; les subagents préchargent maintenant leur Skill de sortie via le champ `skills:`.

Comme toujours avec les outils IA (qui évoluent vite), vérifie les commandes exactes avec `--help` ou la doc officielle avant de les exécuter en prod.
