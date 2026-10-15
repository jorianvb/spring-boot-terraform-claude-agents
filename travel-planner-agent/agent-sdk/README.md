# Scripts Agent SDK (automatisation)

Ces scripts utilisent le **Agent SDK Python** (`claude-agent-sdk`) pour lancer des agents Claude
par programme, en dehors d'une session interactive Claude Code. C'est ce qui permet de les
brancher sur une tache planifiee (cron, GitHub Actions) plutot que de les lancer a la main.

## Installation

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="..."   # cle API du Claude Console, jamais en dur dans le code
```

## Scripts

- `watch_prices.py` : relance le subagent `price-watcher` sur une liste de recherches definie
  dans `agent-sdk/watchlist.json`, et ecrit/mets a jour l'historique dans `reports/price-history/`.
- `research_destination.py` : lance le subagent `destination-researcher` sur une destination donnee
  en argument de ligne de commande.

Ces scripts chargent automatiquement les Skills et subagents de `.claude/` de ce projet
(l'Agent SDK lit `.claude/` comme le ferait Claude Code).

## Lancer une veille ponctuelle

```bash
python agent-sdk/watch_prices.py
python agent-sdk/research_destination.py "Lisbonne, Portugal"
```

## Lancer en automatique

Voir `.github/workflows/price-watch.yml` pour un exemple de tache planifiee (cron GitHub Actions)
qui execute `watch_prices.py` chaque jour et commite le rapport mis a jour dans le depot.
