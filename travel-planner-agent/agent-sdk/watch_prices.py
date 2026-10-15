"""Lance le subagent price-watcher sur chaque recherche de watchlist.json.

Usage:
    python agent-sdk/watch_prices.py

Necessite ANTHROPIC_API_KEY dans l'environnement (jamais en dur dans ce fichier).
Prevu pour etre appele depuis une tache planifiee (voir .github/workflows/price-watch.yml).
"""

import asyncio
import json
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, query

WATCHLIST_PATH = Path(__file__).parent / "watchlist.json"
PROJECT_ROOT = Path(__file__).parent.parent


async def watch_one(recherche: dict) -> None:
    prompt = (
        f"Utilise le subagent price-watcher pour la recherche suivante : "
        f"{recherche['description']}. Budget cible : {recherche['budget_cible_eur']} EUR. "
        f"Identifiant de recherche pour le fichier d'historique : {recherche['id']}."
    )
    options = ClaudeAgentOptions(cwd=str(PROJECT_ROOT))
    async for message in query(prompt=prompt, options=options):
        print(message)


async def main() -> None:
    watchlist = json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))
    for recherche in watchlist:
        await watch_one(recherche)


if __name__ == "__main__":
    asyncio.run(main())
