# Tutoriel : comprendre, créer et gérer des agents Claude (subagents)

Ce tutoriel est **général** : il complète les deux tutoriels de ce dépôt
([Spring Boot/Terraform](../spring-boot-terraform-agents/docs/tutoriel-agents-claude-spring-terraform.md) et
[Travel Planner](../travel-planner-agent/docs/tutoriel-travel-planner-agent.md)) en expliquant **la mécanique
de base** : qu'est-ce qu'un agent Claude Code, comment en créer un, comment en ajouter, modifier ou supprimer
un dans un projet existant. Les deux projets de ce dépôt sont pleins d'exemples concrets — reviens vers eux
une fois les bases comprises ici.

---

## Sommaire

1. [Agent, subagent, Skill : de quoi on parle](#1-vocabulaire)
2. [Créer un premier subagent](#2-creer-un-subagent)
3. [Anatomie complète d'un fichier de subagent](#3-anatomie)
4. [Où ranger les fichiers, et pourquoi ça change tout](#4-emplacements)
5. [Comment invoquer un subagent](#5-invoquer)
6. [Ajouter un subagent à un projet existant (pas à pas)](#6-ajouter)
7. [Modifier ou supprimer un subagent](#7-modifier-supprimer)
8. [Checklist avant de committer un nouveau subagent](#8-checklist)
9. [Erreurs fréquentes](#9-erreurs)
10. [Liens utiles](#10-liens)
11. [3 podcasts pour aller plus loin](#11-podcasts)

---

## 1. Agent, subagent, Skill : de quoi on parle <a name="1-vocabulaire"></a>

Ces trois mots se ressemblent, et c'est volontairement qu'on les a laissés se recouper dans les deux
projets de ce dépôt. Voici la différence concrète :

| Terme | C'est quoi | Exemple dans ce dépôt |
|---|---|---|
| **Claude Code** | L'agent principal, celui avec qui tu discutes dans le terminal | La session que tu ouvres avec `claude` |
| **Subagent** | Un agent *secondaire*, avec son propre prompt, ses propres outils, parfois son propre modèle, invoqué par l'agent principal pour une tâche précise, dans un contexte isolé | `terraform-reviewer`, `destination-researcher` |
| **Skill** | Pas un agent : un mode d'emploi (`SKILL.md`) que Claude charge quand c'est pertinent, pour savoir *comment* faire une tâche ou *sous quel format* rendre un résultat | `ddd-module`, `destination-dossier` |
| **Agent SDK** | Une bibliothèque (Python/TypeScript) pour lancer un agent *par programme*, hors session interactive — utile pour une tâche planifiée | `agent-sdk/watch_prices.py` dans travel-planner-agent |

**Ce tutoriel ne parle que des subagents** (le deuxième de la liste) : comment les créer et les gérer dans
`.claude/agents/`. Pour les Skills, un tutoriel séparé pourrait être ajouté si besoin — la mécanique de
création est proche (un dossier avec un `SKILL.md`), mais leur rôle est différent.

---

## 2. Créer un premier subagent <a name="2-creer-un-subagent"></a>

Il y a deux façons de faire, et les deux sont légitimes :

### Méthode A — demander à Claude de l'écrire (la plus simple)

Dans une session Claude Code, décris simplement ce que tu veux :

```text
Crée un subagent personnel "code-improver" dans ~/.claude/agents/ qui relit un fichier
et propose des améliorations de lisibilité et de performance. Il doit être en lecture
seule (pas d'écriture) et utiliser le modèle Sonnet.
```

Claude écrit le fichier à ta place. **Relis-le ensuite** — comme pour tout code généré, tu restes
responsable de ce qu'il contient.

### Méthode B — l'écrire toi-même

Crée le dossier et le fichier à la main :

```bash
mkdir -p .claude/agents
cat > .claude/agents/code-improver.md << 'EOF'
---
name: code-improver
description: Relit un fichier et propose des ameliorations de lisibilite et de performance.
tools: Read, Grep, Glob
model: sonnet
---

Tu es un specialiste de l'amelioration de code. Pour chaque probleme trouve,
explique-le, montre le code actuel et propose une version amelioree.
EOF
```

Claude Code détecte les nouveaux fichiers dans un dossier `agents/` déjà existant en quelques secondes,
sans redémarrage. Si c'est le **premier** fichier dans un dossier `.claude/agents/` qui n'existait pas
encore, un redémarrage de la session peut être nécessaire pour que Claude Code le repère.

> La commande `/agents` existe toujours en session interactive, mais selon la version de Claude Code elle
> se contente d'un rappel ("modifie `.claude/agents/`") ou ouvre un gestionnaire interactif complet
> (onglets *Running* / *Library*). Ne te fie pas à une capture d'écran ancienne — regarde ce que `/agents`
> affiche réellement dans ta version.

---

## 3. Anatomie complète d'un fichier de subagent <a name="3-anatomie"></a>

Un subagent est un fichier Markdown avec un en-tête YAML (le "frontmatter") entre deux lignes `---`,
suivi du corps qui est le prompt système du subagent.

```markdown
---
name: terraform-reviewer
description: Relit un plan ou un diff Terraform avant un apply. Utiliser PROACTIVEMENT apres toute modification de fichiers .tf.
tools: Read, Grep, Bash
model: sonnet
---

Tu es un ingenieur infrastructure senior specialise Terraform/AWS.
Quand on t'invoque : ...
```

**Seuls deux champs sont obligatoires** : `name` et `description`. Tout le reste est optionnel, mais
voici les champs les plus utiles à connaître (la liste complète est dans la doc officielle, qui évolue) :

| Champ | À quoi ça sert |
|---|---|
| `name` | Identifiant du subagent (c'est lui qui compte, pas le nom du fichier) |
| `description` | **Le champ le plus important** : c'est ce qui décide quand Claude déclenche ce subagent automatiquement |
| `tools` | La liste des outils autorisés (ex: `Read, Grep, Bash`). Par défaut, un subagent hérite de tous les outils disponibles — restreins-la si le rôle doit être limité (ex: lecture seule) |
| `disallowedTools` | Pour retirer des outils précis d'une liste héritée, plutôt que de tout réénumérer |
| `model` | `sonnet`, `opus`, `haiku`, ou `inherit` pour garder le modèle de la session principale |
| `maxTurns` | Un plafond du nombre d'allers-retours, utile pour éviter qu'un subagent ne tourne en boucle |
| `skills` | Des Skills à charger automatiquement au démarrage de ce subagent |

### La `description` : le champ qui fait tout

C'est la `description` qui décide si Claude invoque ton subagent automatiquement, en comparant la
demande de l'utilisateur au texte de la description. Deux règles d'or :

1. **Sois précis sur le "quand".** "Relit le code" est trop vague. "Relit un diff Terraform avant un
   apply, à utiliser PROACTIVEMENT après toute modification de fichiers .tf" déclenche au bon moment.
2. **Dis aussi ce qu'il ne faut PAS déclencher.** Ex: "Ne pas utiliser pour une simple modification de
   variable existante" — ça évite les faux déclenchements qui gaspillent du contexte pour rien.

---

## 4. Où ranger les fichiers, et pourquoi ça change tout <a name="4-emplacements"></a>

| Emplacement | Portée | Versionné avec le projet ? |
|---|---|---|
| `.claude/agents/` | Le projet courant seulement | Oui — c'est ce que font les deux projets de ce dépôt |
| `~/.claude/agents/` | Tous tes projets, sur ta machine | Non, c'est personnel |

**Priorité en cas de nom identique** : un réglage d'organisation (si ton entreprise en définit) prime sur
tout, puis le projet (`.claude/agents/`) prime sur l'utilisateur (`~/.claude/agents/`). Autrement dit, si
tu as un `code-reviewer` personnel dans `~/.claude/agents/` et qu'un projet en définit un autre du même
nom dans `.claude/agents/`, c'est **celui du projet** qui s'applique quand tu travailles dans ce projet.

**Pourquoi versionner `.claude/agents/` avec Git ?** Parce que c'est ce qui permet à toute une équipe de
bénéficier des mêmes subagents — exactement comme pour le code. C'est ce que font
`spring-boot-terraform-agents/.claude/agents/` et `travel-planner-agent/.claude/agents/` dans ce dépôt :
chacun a ses propres subagents, adaptés à son domaine, et les deux sont commités.

---

## 5. Comment invoquer un subagent <a name="5-invoquer"></a>

Il y a trois façons, du plus automatique au plus explicite :

1. **Automatiquement**, quand ta demande correspond à la `description` du subagent. C'est le mode
   normal : tu ne nommes même pas le subagent, Claude décide de l'invoquer.
2. **En le nommant dans le prompt** : `"Utilise le subagent terraform-reviewer sur le dossier terraform/envs/dev"`.
   C'est la méthode la plus fiable quand tu veux être sûr que c'est bien *ce* subagent-là qui s'exécute.
3. **Via `/agents`** en session interactive (si ta version propose un gestionnaire interactif) : tu peux
   lancer, modifier ou consulter les subagents depuis cette interface.

---

## 6. Ajouter un subagent à un projet existant (pas à pas) <a name="6-ajouter"></a>

Reprenons un exemple concret : ajouter un subagent **`flight-alternative-finder`** au projet
`travel-planner-agent/`, qui cherche des alternatives d'aéroport ou de date si le prix cible n'est
jamais atteint par `price-watcher`.

**Étape 1 — identifier le rôle précis et ses limites.**
Avant d'écrire une ligne, réponds à : *quand* ce subagent doit-il se déclencher ? *quels outils*
lui faut-il vraiment (recherche web seulement, ou aussi écriture de fichier) ? *que ne doit-il
jamais faire* (ici : ne jamais réserver, comme tous les autres agents de ce projet) ?

**Étape 2 — créer le fichier.**

```bash
cd travel-planner-agent
mkdir -p .claude/agents   # déjà présent dans ce projet
cat > .claude/agents/flight-alternative-finder.md << 'EOF'
---
name: flight-alternative-finder
description: A utiliser quand price-watcher ne trouve jamais de prix sous le budget cible apres plusieurs releves. Cherche des alternatives (aeroports proches, dates decalees de quelques jours) pour la meme recherche. Ne pas utiliser pour une premiere recherche de prix.
tools: WebSearch, WebFetch, Read, Write
model: sonnet
---

Tu cherches des alternatives pour faire baisser un budget de transport, tu ne reserves jamais rien.

Quand on t'invoque avec une recherche qui depasse systematiquement son budget cible :
1. Relis l'historique dans reports/price-history/<recherche>.md pour comprendre l'ecart au budget.
2. Propose 2-3 alternatives concretes : aeroport de depart/arrivee proche, dates decalees de 2-3 jours,
   escale au lieu de direct.
3. Pour chaque alternative, donne une estimation de prix et la source.
4. Ajoute ces alternatives a la fin du fichier d'historique correspondant, sous un titre clair
   "Alternatives explorees le <date>".
EOF
```

**Étape 3 — tester le déclenchement.**
Essaie plusieurs formulations qui *devraient* le déclencher ("le prix ne descend jamais sous mon
budget, as-tu une idée ?") et une qui ne devrait *pas* le déclencher ("quel est le prix aujourd'hui
pour ce vol ?" — qui doit rester sur `price-watcher`). Si Claude se trompe de subagent, c'est souvent
la `description` qu'il faut préciser.

**Étape 4 — documenter le nouveau subagent là où les autres sont listés.**
Dans ce dépôt, chaque projet liste ses subagents dans son `README.md` et parfois son `CLAUDE.md` —
mets ce nouveau subagent à jour dans ces deux fichiers pour que l'équipe le découvre sans avoir à
fouiller `.claude/agents/`.

**Étape 5 — committer.**

```bash
git add .claude/agents/flight-alternative-finder.md README.md
git commit -m "Ajoute le subagent flight-alternative-finder"
```

---

## 7. Modifier ou supprimer un subagent <a name="7-modifier-supprimer"></a>

- **Modifier** : édite directement le fichier `.md` (toi-même, ou en demandant à Claude de le faire).
  Les changements sont pris en compte à la prochaine invocation.
- **Supprimer** : supprime simplement le fichier `.md`. Il n'y a rien d'autre à nettoyer — un subagent
  n'a pas d'état caché ailleurs.
- Si ta version de Claude Code propose l'onglet **Library** dans `/agents`, tu peux aussi modifier ou
  supprimer depuis cette interface — c'est strictement équivalent à éditer le fichier.

---

## 8. Checklist avant de committer un nouveau subagent <a name="8-checklist"></a>

- [ ] `description` précise sur le "quand" **et** sur le "quand pas" (une phrase "ne pas utiliser pour...").
- [ ] `tools` restreint au strict nécessaire pour le rôle (pas de `Bash`/`Write` par réflexe).
- [ ] Testé avec au moins 2 formulations qui doivent déclencher, et 1 qui ne doit pas.
- [ ] Si le subagent produit un document, il suit le format d'une Skill existante plutôt que d'inventer
      un format à chaque fois (voir les Skills des deux projets de ce dépôt).
- [ ] Le subagent est documenté (README/CLAUDE.md du projet) pour que l'équipe le découvre.
- [ ] Aucune action irréversible (achat, suppression, envoi d'email...) n'est confiée au subagent sans
      validation humaine explicite — règle suivie partout dans ce dépôt.

---

## 9. Erreurs fréquentes <a name="9-erreurs"></a>

- **Un subagent qui ne se déclenche jamais** → la `description` est trop vague ou trop éloignée du
  vocabulaire que tu emploies réellement dans tes demandes. Reformule-la avec les mots que tu utilises
  vraiment.
- **Un subagent qui se déclenche trop souvent** → ajoute la phrase "ne pas utiliser pour..." dans la
  `description`, et vérifie qu'il n'y a pas de recoupement avec un autre subagent du projet.
- **Deux subagents portant le même `name`** → celui du dossier le plus prioritaire (projet avant
  utilisateur) gagne, silencieusement. Garde des noms uniques dans tout l'arbre `.claude/agents/`.
- **Un champ du frontmatter mal orthographié** → il est simplement ignoré, sans message d'erreur. Si un
  réglage semble ne pas s'appliquer, vérifie l'orthographe exacte du champ dans la doc officielle.
- **Un subagent avec trop d'outils "juste au cas où"** → ça augmente le risque (un subagent qui ne
  devrait que lire peut, par erreur de prompt, écrire ou exécuter une commande). Restreins `tools` au
  strict nécessaire pour son rôle.

---

## 10. Liens utiles <a name="10-liens"></a>

- [Créer des subagents personnalisés — documentation officielle](https://code.claude.com/docs/en/sub-agents)
- [Subagents dans le Claude Code SDK](https://docs.claude.com/en/docs/claude-code/sdk/subagents)
- [Guide FR pas-à-pas des sous-agents (12 étapes)](https://tech-insider.org/fr/?p=2893)

---

## 11. Trois podcasts pour aller plus loin <a name="11-podcasts"></a>

1. **"How to Use Claude Code Like the People Who Built It"** (*AI & I*, avec les créateurs de Claude Code
   chez Anthropic) — ils expliquent directement comment ils utilisent les subagents en interne.
   👉 https://www.youtube.com/watch?v=IDSAMqip6ms

2. **"The future of agentic coding with Claude Code"** (Anthropic, YouTube) — pour comprendre le
   fonctionnement général d'un agent Claude Code avant de se lancer dans la création de subagents.
   👉 https://www.youtube.com/watch?v=iF9iV4xponk

3. **"How agentic AI could transform travel"** (*The McKinsey Podcast*, Spotify) — pour voir comment une
   logique de subagents spécialisés (recherche, veille, planification) s'applique à un domaine entier,
   en écho direct au projet `travel-planner-agent/` de ce dépôt.
   👉 https://open.spotify.com/show/4dyjRTP9xzEUPgleo6XjXI

---

*Comme toujours : les commandes et le frontmatter exacts évoluent vite d'une version de Claude Code à
l'autre. Vérifie `claude --help`, `/agents`, ou la doc officielle avant de copier un exemple tel quel.*
