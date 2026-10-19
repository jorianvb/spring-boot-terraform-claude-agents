#!/usr/bin/env bash
# hash_scan.sh - produit un inventaire (chemin relatif, taille, date de modification, hash
# sha256) d'un dossier de photos. Utilise par les subagents duplicate-detector,
# backup-integrity-checker et storage-cost-optimizer via l'outil Bash.
# Ne fait aucun appel reseau et ne modifie jamais les fichiers scannes (lecture seule).
#
# Usage : ./scripts/hash_scan.sh <dossier> > inventaire.csv
#
# Sortie CSV (separateur ";") triee par chemin :
#   chemin_relatif;taille_octets;date_modification;sha256
# Les chemins sont RELATIFS au dossier scanne : on peut donc comparer directement
# l'inventaire d'une bibliotheque et celui de sa sauvegarde (meme photo = meme chemin relatif).
# Fonctionne sous Linux (GNU coreutils) et macOS (BSD stat + shasum).

set -euo pipefail

DIR="${1:-}"
if [ -z "$DIR" ] || [ ! -d "$DIR" ]; then
  echo "Usage: $0 <dossier-a-scanner>" >&2
  exit 1
fi

taille() { stat -c%s "$1" 2>/dev/null || stat -f%z "$1"; }
date_modif() { date -r "$1" "+%Y-%m-%dT%H:%M:%S"; }
hash_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | cut -d' ' -f1
  else
    shasum -a 256 "$1" | cut -d' ' -f1
  fi
}

echo "chemin_relatif;taille_octets;date_modification;sha256"

cd "$DIR"
find . -type f \( \
  -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.heic" \
  -o -iname "*.mov" -o -iname "*.mp4" -o -iname "*.raw" -o -iname "*.dng" \
  \) -print0 | sort -z | while IFS= read -r -d '' f; do
  chemin="${f#./}"
  echo "${chemin};$(taille "$f");$(date_modif "$f");$(hash_sha256 "$f")"
done
