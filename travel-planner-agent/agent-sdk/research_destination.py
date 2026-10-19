"""Lance le subagent destination-researcher sur une destination donnee.

Usage (depuis le dossier travel-planner-agent/) :
    python agent-sdk/research_destination.py "Lisbonne, Portugal"

Necessite ANTHROPIC_API_KEY dans l'environnement.
"""

import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

PROJECT_ROOT = Path(__file__).parent.parent


async def main(destination: str) -> int:
    prompt = (
        f"Utilise le subagent destination-researcher pour produire le dossier destination : "
        f"{destination}. Ecris-le dans docs/destinations/ au format de la Skill destination-dossier."
    )
    options = ClaudeAgentOptions(
        cwd=str(PROJECT_ROOT),
        setting_sources=["project"],  # charge CLAUDE.md, .claude/agents/ et .claude/skills/
        permission_mode="dontAsk",  # tout outil non liste ci-dessous est refuse
        allowed_tools=["Read", "WebSearch", "WebFetch", "Skill", "Edit(/docs/destinations/**)"],
        max_turns=40,
        max_budget_usd=2.0,
    )
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, ResultMessage):
            print(f"{message.subtype} - cout estime : {message.total_cost_usd} USD")
            if message.result:
                print(message.result)
            return 1 if message.is_error else 0
    return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python agent-sdk/research_destination.py "<destination>"')
        raise SystemExit(1)
    sys.exit(asyncio.run(main(sys.argv[1])))
