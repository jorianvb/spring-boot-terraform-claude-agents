# Agent SDK — photo-storage-agent

Scripts Python qui executent les subagents de ce projet par programme (hors session Claude Code
interactive), via `claude-agent-sdk`.

## Installation
```bash
cd photo-storage-agent
python -m venv .venv && source .venv/bin/activate   # Python 3.10+
pip install -r agent-sdk/requirements.txt
export ANTHROPIC_API_KEY="..."   # cle API du Claude Console
```

Le paquet `claude-agent-sdk` embarque Claude Code : rien d'autre a installer. Pour `metadata-enricher`
(lecture EXIF), installe aussi `exiftool` (`brew install exiftool`, `sudo apt install libimage-exiftool-perl`).

## Pourquoi pas de workflow GitHub Actions (cloud) ici ?
Dans `travel-planner-agent/`, la veille tarifaire interroge uniquement des API web : un runner
GitHub Actions dans le cloud peut le faire sans probleme. Une bibliotheque de photos est en
general sur un disque local, un NAS domestique, ou un service cloud personnel (pas forcement
accessible depuis un runner externe) : ce projet est donc pense pour une execution **locale**
planifiee (cron sur ta machine ou ton NAS, tache planifiee Windows/macOS), pas un workflow GitHub
Actions cloud. Voir le tutoriel pour un exemple de ligne crontab.

Si ta bibliotheque est elle-meme sur un stockage cloud accessible par API (ex: un bucket S3, un
service avec API REST), le meme principe que `price-watch.yml` s'applique : un workflow planifie
peut alors tourner dans le cloud.

## Scripts
- `check_backup_integrity.py --source <dossier> --backup <dossier>` : lance
  `backup-integrity-checker`. A executer regulierement (ex: chaque semaine).
- `storage_cost_report.py --library <dossier>` : lance `storage-cost-optimizer`. A executer
  ponctuellement (ex: chaque mois, ou quand une alerte de quota de stockage apparait).

## Garde-fous des scripts
- `permission_mode="dontAsk"` : execution sans humain, donc tout outil non autorise est refuse.
- Seule commande shell autorisee : `./scripts/hash_scan.sh` (lecture + hash). `rm`, `mv`, `cp` et
  `rsync` sont explicitement interdits.
- Ecriture limitee au dossier `reports/` du projet (`Edit(/reports/**)`).
- Les dossiers de photos sont ajoutes en lecture via `add_dirs`.
- Plafonds : `max_turns=30`, `max_budget_usd=1.0` par execution.
- Les scripts trouvent la racine du projet tout seuls : on peut les lancer depuis n'importe quel
  dossier (pratique en cron).
