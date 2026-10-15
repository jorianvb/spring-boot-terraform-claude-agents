"""
check_backup_integrity.py — execute le subagent `backup-integrity-checker` par programme,
via l'Agent SDK, hors d'une session interactive. Pense pour une execution reguliere
planifiee (cron local, tache planifiee du systeme), car une bibliotheque de photos est en
general sur un disque local ou un NAS, pas accessible depuis un runner cloud comme GitHub
Actions — contrairement au cas du travel-planner-agent (qui n'interroge que des API web).

Usage :
    python check_backup_integrity.py --source /chemin/photos --backup /chemin/sauvegarde

Variables d'environnement attendues : ANTHROPIC_API_KEY (ou ANTHROPIC_BASE_URL /
ANTHROPIC_AUTH_TOKEN pour un usage via Ollama, voir le tutoriel).
"""

import argparse
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, query


async def main(source: str, backup: str) -> None:
    prompt = (
        f"Utilise le subagent backup-integrity-checker pour verifier l'integrite de la "
        f"sauvegarde. Bibliotheque source : {source}. Sauvegarde : {backup}. "
        f"Utilise le script scripts/hash_scan.sh sur les deux dossiers pour obtenir les "
        f"inventaires, compare-les, puis ecris le rapport dans reports/backup-integrity/ "
        f"en suivant la Skill backup-integrity-report."
    )

    options = ClaudeAgentOptions(cwd=".")

    async for message in query(prompt=prompt, options=options):
        print(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verifie l'integrite d'une sauvegarde photo.")
    parser.add_argument("--source", required=True, help="Dossier de la bibliotheque principale")
    parser.add_argument("--backup", required=True, help="Dossier ou identifiant de la sauvegarde")
    args = parser.parse_args()

    asyncio.run(main(args.source, args.backup))
