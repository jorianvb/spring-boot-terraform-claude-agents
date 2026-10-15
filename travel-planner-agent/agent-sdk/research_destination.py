"""Lance le subagent destination-researcher sur une destination donnee.

Usage:
    python agent-sdk/research_destination.py "Lisbonne, Portugal"

Necessite ANTHROPIC_API_KEY dans l'environnement.
"""

import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, query

PROJECT_ROOT = Path(__file__).parent.parent


async def main(destination: str) -> None:
    prompt = f"Utilise le subagent destination-researcher pour produire le dossier destination : {destination}."
    options = ClaudeAgentOptions(cwd=str(PROJECT_ROOT))
    async for message in query(prompt=prompt, options=options):
        print(message)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python research_destination.py \"<destination>\"")
        raise SystemExit(1)
    asyncio.run(main(sys.argv[1]))
