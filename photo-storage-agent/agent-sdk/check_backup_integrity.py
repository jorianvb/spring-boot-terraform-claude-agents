"""
check_backup_integrity.py - execute le subagent `backup-integrity-checker` par programme,
via l'Agent SDK, hors d'une session interactive. Pense pour une execution reguliere
planifiee (cron local, tache planifiee du systeme), car une bibliotheque de photos est en
general sur un disque local ou un NAS, pas accessible depuis un runner cloud comme GitHub
Actions - contrairement au cas du travel-planner-agent (qui n'interroge que des API web).

Usage (depuis n'importe quel dossier) :
    python agent-sdk/check_backup_integrity.py --source /chemin/photos --backup /chemin/sauvegarde

Variables d'environnement attendues : ANTHROPIC_API_KEY (ou ANTHROPIC_BASE_URL /
ANTHROPIC_AUTH_TOKEN pour un usage via Ollama, voir le tutoriel Spring Boot/Terraform).
"""

import argparse
import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

# Racine du projet photo-storage-agent/, quel que soit le dossier d'ou le script est lance
# (important en cron, ou le dossier courant n'est pas celui du projet).
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def build_options(*dossiers_photos: str) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        cwd=str(PROJECT_ROOT),
        setting_sources=["project"],  # charge CLAUDE.md, .claude/agents/ et .claude/skills/
        # Les dossiers de photos sont hors du projet : on les ajoute pour autoriser leur lecture.
        add_dirs=list(dossiers_photos),
        # Tache sans humain : tout ce qui n'est pas explicitement autorise est refuse.
        permission_mode="dontAsk",
        allowed_tools=[
            "Read",
            "Skill",
            "Bash(./scripts/hash_scan.sh *)",  # seul script shell autorise (lecture + hash)
            "Edit(/reports/**)",  # ecriture limitee au dossier reports/ du projet
        ],
        # Ceinture et bretelles : aucune commande destructive, meme par erreur de prompt.
        disallowed_tools=["Bash(rm *)", "Bash(mv *)", "Bash(cp *)", "Bash(rsync *)"],
        max_turns=30,
        max_budget_usd=1.0,
    )


async def main(source: str, backup: str) -> int:
    prompt = (
        f"Utilise le subagent backup-integrity-checker pour verifier l'integrite de la "
        f"sauvegarde. Bibliotheque source : {source}. Sauvegarde : {backup}. "
        f"Lance ./scripts/hash_scan.sh sur chacun des deux dossiers pour obtenir les "
        f"inventaires (chemins relatifs + hash), compare-les, puis ecris le rapport dans "
        f"reports/backup-integrity/ en suivant la Skill backup-integrity-report."
    )
    async for message in query(prompt=prompt, options=build_options(source, backup)):
        if isinstance(message, ResultMessage):
            print(f"{message.subtype} - cout estime : {message.total_cost_usd} USD")
            if message.result:
                print(message.result)
            return 1 if message.is_error else 0
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verifie l'integrite d'une sauvegarde photo.")
    parser.add_argument("--source", required=True, help="Dossier de la bibliotheque principale")
    parser.add_argument("--backup", required=True, help="Dossier de la sauvegarde (monte localement)")
    args = parser.parse_args()

    sys.exit(asyncio.run(main(args.source, args.backup)))
