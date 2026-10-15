"""
storage_cost_report.py — execute le subagent `storage-cost-optimizer` par programme,
via l'Agent SDK. A lancer ponctuellement (mensuel par exemple), pas a chaque import de
photo : voir le tutoriel pour la justification de la cadence.

Usage :
    python storage_cost_report.py --library /chemin/photos
"""

import argparse
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, query


async def main(library: str) -> None:
    prompt = (
        f"Utilise le subagent storage-cost-optimizer pour analyser la bibliotheque "
        f"{library}. Utilise scripts/hash_scan.sh pour obtenir tailles et dates, compare "
        f"avec la derniere ligne de reports/storage-history/historique.csv si elle existe, "
        f"ajoute une nouvelle ligne a cet historique, puis ecris le rapport dans "
        f"reports/storage-cost/ en suivant la Skill storage-cost-report."
    )

    options = ClaudeAgentOptions(cwd=".")

    async for message in query(prompt=prompt, options=options):
        print(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse le cout de stockage d'une bibliotheque photo.")
    parser.add_argument("--library", required=True, help="Dossier de la bibliotheque a analyser")
    args = parser.parse_args()

    asyncio.run(main(args.library))
