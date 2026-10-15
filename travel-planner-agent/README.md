# Travel Planner Agent

Un système d'agents Claude pour **planifier un voyage soi-même** : recherche de destination,
construction d'itinéraire, veille tarifaire automatisée, repérage d'événements locaux.
**Ce n'est pas une agence de voyage** : aucun agent ne réserve, n'achète ni ne crée de compte —
ils cherchent et rapportent, tu décides et agis toi-même.

👉 Le tutoriel complet est dans [`docs/tutoriel-travel-planner-agent.md`](docs/tutoriel-travel-planner-agent.md).

## Contenu

- `CLAUDE.md` : mémoire de projet lue par Claude Code.
- `.claude/agents/` : subagents (destination-researcher, itinerary-builder, price-watcher, local-events-scout, trip-journal-writer).
- `.claude/skills/` : Skills qui standardisent le format des documents produits.
- `agent-sdk/` : scripts Python (Agent SDK) pour lancer les agents hors session interactive.
- `.github/workflows/price-watch.yml` : veille tarifaire quotidienne automatisée.
- `docs/` : dossiers destinations, itinéraires, suivis de voyage (générés par les agents).
- `reports/price-history/` : historique de veille tarifaire (généré par les agents).

## Démarrer

```bash
cd travel-planner-agent
claude
# "Utilise le subagent destination-researcher pour Lisbonne, Portugal"
```
