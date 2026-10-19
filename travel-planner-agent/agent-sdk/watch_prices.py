"""Lance le subagent price-watcher sur chaque recherche de watchlist.json.

Usage (depuis le dossier travel-planner-agent/) :
    python agent-sdk/watch_prices.py

Necessite ANTHROPIC_API_KEY dans l'environnement (jamais en dur dans ce fichier).
Prevu pour etre appele depuis une tache planifiee (voir .github/workflows/price-watch.yml
a la racine du depot).
"""

import asyncio
import json
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

WATCHLIST_PATH = Path(__file__).parent / "watchlist.json"
PROJECT_ROOT = Path(__file__).parent.parent


def build_options() -> ClaudeAgentOptions:
    """Options communes : execution sans humain, donc surface d'outils fixe et plafonnee."""
    return ClaudeAgentOptions(
        cwd=str(PROJECT_ROOT),
        # Charge CLAUDE.md, .claude/agents/ et .claude/skills/ du projet.
        setting_sources=["project"],
        # "dontAsk" : tout outil non autorise ci-dessous est refuse (personne pour valider).
        permission_mode="dontAsk",
        allowed_tools=[
            "Read",
            "WebSearch",
            "WebFetch",
            "Skill",
            # L'agent ne peut ecrire que dans reports/ (Edit(...) couvre aussi Write).
            "Edit(/reports/**)",
        ],
        max_turns=30,  # disjoncteur : pas de boucle infinie
        max_budget_usd=1.0,  # plafond de depense par recherche
    )


async def watch_one(recherche: dict) -> bool:
    prompt = (
        f"Utilise le subagent price-watcher pour la recherche suivante : "
        f"{recherche['description']}. Budget cible : {recherche['budget_cible_eur']} EUR. "
        f"Identifiant de recherche pour le fichier d'historique : {recherche['id']} "
        f"(fichier reports/price-history/{recherche['id']}.md, format de la Skill price-watch-report)."
    )
    ok = False
    async for message in query(prompt=prompt, options=build_options()):
        if isinstance(message, ResultMessage):
            ok = not message.is_error
            print(f"[{recherche['id']}] {message.subtype} - cout estime : {message.total_cost_usd} USD")
            if message.result:
                print(message.result)
    return ok


async def main() -> int:
    watchlist = json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))
    echecs = 0
    for recherche in watchlist:
        try:
            if not await watch_one(recherche):
                echecs += 1
        except Exception as erreur:  # une recherche en echec ne bloque pas les suivantes
            echecs += 1
            print(f"[{recherche['id']}] erreur : {erreur}", file=sys.stderr)
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
