"""
storage_cost_report.py - execute le subagent `storage-cost-optimizer` par programme,
via l'Agent SDK. A lancer ponctuellement (mensuel par exemple), pas a chaque import de
photo : voir le tutoriel pour la justification de la cadence.

Usage (depuis n'importe quel dossier) :
    python agent-sdk/storage_cost_report.py --library /chemin/photos
"""

import argparse
import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

PROJECT_ROOT = Path(__file__).resolve().parent.parent


async def main(library: str) -> int:
    prompt = (
        f"Utilise le subagent storage-cost-optimizer pour analyser la bibliotheque "
        f"{library}. Lance ./scripts/hash_scan.sh sur ce dossier pour obtenir tailles et dates, "
        f"compare avec la derniere ligne de reports/storage-history/historique.csv si elle "
        f"existe, ajoute une nouvelle ligne a cet historique, puis ecris le rapport dans "
        f"reports/storage-cost/ en suivant la Skill storage-cost-report."
    )
    options = ClaudeAgentOptions(
        cwd=str(PROJECT_ROOT),
        setting_sources=["project"],
        add_dirs=[library],
        permission_mode="dontAsk",
        allowed_tools=["Read", "Skill", "Bash(./scripts/hash_scan.sh *)", "Edit(/reports/**)"],
        disallowed_tools=["Bash(rm *)", "Bash(mv *)", "Bash(cp *)", "Bash(rsync *)"],
        max_turns=30,
        max_budget_usd=1.0,
    )
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, ResultMessage):
            print(f"{message.subtype} - cout estime : {message.total_cost_usd} USD")
            if message.result:
                print(message.result)
            return 1 if message.is_error else 0
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse le cout de stockage d'une bibliotheque photo.")
    parser.add_argument("--library", required=True, help="Dossier de la bibliotheque a analyser")
    args = parser.parse_args()

    sys.exit(asyncio.run(main(args.library)))
