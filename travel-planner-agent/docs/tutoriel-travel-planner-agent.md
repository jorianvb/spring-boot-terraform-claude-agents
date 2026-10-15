# Tutoriel : un système d'agents Claude pour planifier un voyage soi-même

Ce dossier (`travel-planner-agent/`) est un second projet, distinct du projet Spring Boot/Terraform. Ici, les agents Claude ne codent pas : ils **cherchent, surveillent, et proposent**, pour t'aider à préparer un voyage **toi-même** — ce n'est pas une agence de voyage, aucun agent ne réserve ni ne paie quoi que ce soit à ta place.

---

## Sommaire

1. [Principe général](#1-principe)
2. [Les agents du projet](#2-agents)
3. [Les Skills : le format des documents produits](#3-skills)
4. [Automatiser la veille (tâches planifiées)](#4-automatisation)
5. [Comment bien construire un système multi-agents de recherche](#5-multi-agent-recherche)
6. [Scénario complet d'utilisation](#6-scenario)
7. [Limites et bonnes pratiques](#7-limites)
8. [Liens utiles](#8-liens)
9. [3 podcasts pour aller plus loin](#9-podcasts)

---

## 1. Principe général <a name="1-principe"></a>

Un voyage se prépare en plusieurs étapes, et chaque étape est confiée à un agent spécialisé :

```
Destination choisie
     │
     ▼
destination-researcher   →  docs/destinations/<ville>.md
     │
     ▼
itinerary-builder        →  docs/itineraries/<voyage>.md
     │
     ▼
local-events-scout       →  vérifie les dates retenues
     │
     ▼
price-watcher (répété)   →  reports/price-history/<recherche>.md
     │
     ▼
trip-journal-writer      →  docs/trips/<voyage>.md (document de suivi unique)
```

Comme pour le projet Spring Boot/Terraform, tout repose sur les mêmes briques Claude Code : un `CLAUDE.md`, des **Skills** (format de sortie standardisé), des **subagents** (rôles spécialisés), et en plus ici, des **scripts Agent SDK** pour automatiser la veille tarifaire sans avoir besoin d'ouvrir une session interactive.

---

## 2. Les agents du projet <a name="2-agents"></a>

| Subagent | Rôle | Jamais fait |
|---|---|---|
| `destination-researcher` | Recherche une destination : sécurité, visa, climat, budget, culture | Ne réserve rien, ne crée pas de compte |
| `itinerary-builder` | Construit un itinéraire jour par jour à partir du dossier destination | Ne vend pas d'excursion, propose juste un plan |
| `price-watcher` | Compare un prix relevé à l'historique et au budget cible, signale les baisses | N'achète jamais un billet, ne saisit aucune donnée de paiement |
| `local-events-scout` | Repère les événements/jours fériés qui tombent dans la fenêtre de voyage | Ne fait pas une liste exhaustive de tout ce qui existe |
| `trip-journal-writer` | Consolide tous les documents en un seul suivi à jour | Ne refait pas les recherches lui-même |

Chaque subagent est un fichier dans `.claude/agents/`, avec un en-tête qui dit **quand** l'utiliser et quels outils il a le droit d'utiliser (`WebSearch`, `WebFetch`, `Read`, `Write`...). Par exemple, `trip-journal-writer` n'a accès qu'à `Read`/`Write` — pas de `WebSearch` — car son rôle est de consolider, pas de chercher.

---

## 3. Les Skills : le format des documents produits <a name="3-skills"></a>

Chaque recherche produit un document structuré, toujours au même format, grâce à une Skill dédiée :

| Skill | Document produit |
|---|---|
| `destination-dossier` | `docs/destinations/<ville>.md` |
| `itinerary-builder` | `docs/itineraries/<voyage>.md` |
| `price-watch-report` | `reports/price-history/<recherche>.md` |
| `packing-list` | `docs/trips/<voyage>-bagages.md` |
| `trip-budget` | `docs/trips/<voyage>-budget.md` |

Pourquoi standardiser le format ? Parce que les autres agents (et toi) relisent ces documents plus tard : si chaque recherche a une forme différente, impossible de les comparer ou de les faire relire par `trip-journal-writer`.

**Règle commune à toutes les Skills de ce projet : toute information sensible (visa, sécurité, taux de change, prix) doit être datée et sourcée.** Une info sur un visa vieille de six mois n'a aucune valeur — mieux vaut que l'agent le dise clairement que de laisser croire que c'est à jour.

---

## 4. Automatiser la veille (tâches planifiées) <a name="4-automatisation"></a>

### 4.1 En session interactive (pour tester)

```bash
cd travel-planner-agent
claude
# puis dans la session :
# "Utilise le subagent price-watcher sur la recherche paris-lisbonne-decembre"
```

### 4.2 En automatique, avec le Agent SDK (Python)

Le dossier `agent-sdk/` contient deux scripts qui utilisent le **Agent SDK Python** (`claude-agent-sdk`) pour lancer un agent par programme, sans session interactive :

```bash
pip install -r agent-sdk/requirements.txt
export ANTHROPIC_API_KEY="..."

python agent-sdk/research_destination.py "Lisbonne, Portugal"
python agent-sdk/watch_prices.py   # relance price-watcher sur toute la watchlist.json
```

Ces scripts pointent l'Agent SDK sur le dossier du projet (`cwd`), ce qui lui permet de charger automatiquement les Skills et subagents de `.claude/` — exactement comme le ferait Claude Code en session interactive.

### 4.3 En tâche planifiée (cron GitHub Actions)

Le fichier `.github/workflows/price-watch.yml` lance `watch_prices.py` **chaque jour à 6h UTC**, et committe automatiquement le rapport mis à jour dans `reports/price-history/`. Il suffit d'ajouter la clé `ANTHROPIC_API_KEY` dans les secrets du dépôt GitHub.

C'est l'équivalent, pour ce projet, du workflow de revue de PR du projet Spring Boot : **une tâche qui tourne seule, et qui écrit un résultat que tu relis ensuite** — jamais une tâche qui agit de façon irréversible (acheter, réserver) sans toi.

### Bonnes pratiques pour un agent planifié

D'après les retours d'expérience sur ce sujet (voir liens en section 8) :
- **Définis les tâches dans un fichier de données** (comme `watchlist.json` ici), pas en dur dans le code : modifier une recherche ne doit pas demander de changer de script.
- **Limite chaque exécution** (nombre de tours, budget de tokens) pour éviter qu'un agent ne tourne en boucle sans fin.
- **Prévois un "disjoncteur"** : si plusieurs exécutions échouent de suite, arrête la tâche plutôt que de laisser le cron la relancer indéfiniment en consommant des crédits API.
- **Garde une mémoire courte et à jour** (ici, les fichiers `reports/price-history/*.md`) plutôt que de tout refaire depuis zéro à chaque exécution.
- **Mets un plafond de dépense** côté Claude Console, pour ne jamais être surpris par la facture d'une tâche automatisée qui tourne tous les jours.

---

## 5. Comment bien construire un système multi-agents de recherche <a name="5-multi-agent-recherche"></a>

Anthropic a documenté comment son propre système de "recherche approfondie" multi-agent fonctionne — c'est une bonne base pour étendre ce projet (par exemple : lancer `destination-researcher` sur 3 destinations candidates en parallèle, puis comparer). Les principes clés :

1. **Un agent orchestrateur, plusieurs agents travailleurs.** L'orchestrateur découpe la question en sous-tâches indépendantes et lance un subagent par sous-tâche ; les subagents ne communiquent pas entre eux.
2. **Ça ne marche que si les sous-tâches sont vraiment indépendantes.** "Comparer 3 destinations sur le budget" se découpe bien en 3 recherches parallèles. "Construire un itinéraire cohérent" ne se découpe pas (il faut tout l'itinéraire en tête) — ça reste un seul agent.
3. **La vague de recherche dure aussi longtemps que le sous-agent le plus lent.** Chaque sous-agent a son propre contexte, donc le contexte principal reste léger.
4. **Vérifier séparément.** Pour une info sensible (sécurité, visa), un agent de vérification dédié doit pouvoir rattacher l'affirmation à sa source brute plutôt que de se fier à un résumé de résumé.
5. **Attention au coût.** Un système multi-agent consomme largement plus de tokens qu'une conversation simple — à réserver aux recherches qui le justifient (comparer plusieurs destinations), pas à une simple question factuelle.

Dans ce projet, le "multi-agent parallèle" n'est pas encore implémenté comme tel (`destination-researcher` tourne une destination à la fois) — c'est une extension naturelle si tu veux comparer plusieurs destinations d'un coup : lancer trois instances du subagent en parallèle (avec l'Agent SDK, plusieurs appels `query()` concurrents) et faire la synthèse dans `trip-journal-writer`.

---

## 6. Scénario complet d'utilisation <a name="6-scenario"></a>

**Objectif : partir 10 jours entre le 10 et le 20 décembre, budget 1200€/personne, depuis Paris, destination à déterminer entre Lisbonne et Marrakech.**

1. `destination-researcher` sur "Lisbonne" puis sur "Marrakech" → deux dossiers dans `docs/destinations/`.
2. Lecture des deux dossiers → décision : Lisbonne (climat plus adapté en décembre).
3. `itinerary-builder` sur "Lisbonne, 10 jours, budget 1200€, rythme tranquille" → `docs/itineraries/lisbonne-decembre.md`.
4. `local-events-scout` sur "Lisbonne, 10-20 décembre" → vérifie qu'aucun jour férié ne ferme les sites prévus.
5. Ajout de la recherche dans `agent-sdk/watchlist.json`, activation du cron → veille tarifaire quotidienne automatique.
6. Quand une alerte prix tombe → décision humaine de réserver (hors de ce projet, sur le site du transporteur).
7. `trip-journal-writer` → `docs/trips/lisbonne-decembre.md` tenu à jour à chaque étape.
8. `packing-list` et `trip-budget` en dernière étape, une fois l'itinéraire figé.

---

## 7. Limites et bonnes pratiques <a name="7-limites"></a>

- **Jamais d'action irréversible automatisée.** Aucun agent ici n'a accès à un moyen de paiement, ne remplit un formulaire de réservation, ni ne crée de compte — ce sont des actions "Explicit permission required" dans toute bonne pratique d'agent IA, et ce projet choisit de ne jamais les automatiser du tout.
- **Les prix et disponibilités changent vite.** Un prix relevé par `price-watcher` est une estimation à l'instant T, jamais une garantie — toujours vérifier sur le site final avant de payer.
- **Les règles de visa/sécurité évoluent.** Revérifie toujours la source officielle avant le départ, même si le dossier destination a été fait il y a quelques semaines.
- **Coût des tâches planifiées.** Une veille quotidienne sur plusieurs recherches a un coût API réel — mets un plafond de dépense et limite le nombre de recherches actives en même temps.
- **Vérifie l'avant-dernière étape humainement.** Avant de considérer un voyage "prêt", relis toi-même le document `docs/trips/<voyage>.md` produit par `trip-journal-writer` plutôt que de faire confiance aveuglément à l'agent.

---

## 8. Liens utiles <a name="8-liens"></a>

- [Claude Agent SDK — vue d'ensemble officielle](https://code.claude.com/docs/en/agent-sdk/overview)
- [Comment Anthropic a construit son système de recherche multi-agent](https://theaiengineer.substack.com/p/how-anthropic-built-multi-agent-deep)
- [Faire tourner un agent Claude sur un cron : mémoire persistante et gestion des erreurs](https://kjetilfuras.com/run-claude-agent-on-schedule/)
- [Building Agents with Claude: From Skills to Scheduled Tasks and Routines](https://hatchworks.com/?p=35376)
- [Panorama des meilleurs outils IA pour planifier un voyage en 2026](https://fast.io/resources/best-ai-for-travel-planning-2026/)
- [Comment l'IA agentique pourrait transformer le voyage (McKinsey)](https://www.mckinsey.com/industries/travel/our-insights/how-agentic-ai-could-transform-travel)

---

## 9. Trois podcasts pour aller plus loin <a name="9-podcasts"></a>

1. **"How agentic AI could transform travel"** (*The McKinsey Podcast*, Spotify) — comment l'IA agentique change la façon de préparer et vendre un voyage, vu côté industrie du voyage (utile pour comprendre le contexte, même si ce projet n'est pas une agence).
   👉 https://open.spotify.com/show/4dyjRTP9xzEUPgleo6XjXI

2. **"Egor Karpovich built 12 AI agents in 5 weeks… and now they're running parts of his travel company while he is sleeping"** (*Everything AI & Travel Podcast*, Spotify) — un retour concret sur la mise en place d'une flotte d'agents IA appliqués au voyage (veille, automatisation), à prendre comme retour d'expérience plutôt que comme modèle à copier tel quel.
   👉 https://open.spotify.com/episode/3L4Tn4JFS6GZyP74R95syx

3. **"How to Use Claude Code Like the People Who Built It"** (podcast *AI & I*, avec les créateurs de Claude Code chez Anthropic) — déjà cité dans le tutoriel Spring Boot/Terraform, il reste pertinent ici : les mêmes bonnes pratiques de subagents et de contexte s'appliquent à ce projet de recherche voyage.
   👉 https://www.youtube.com/watch?v=IDSAMqip6ms

---

*Comme pour l'autre tutoriel de ce dépôt : les commandes et APIs évoluent vite, vérifie toujours la syntaxe exacte avant de lancer quoi que ce soit en automatique.*
