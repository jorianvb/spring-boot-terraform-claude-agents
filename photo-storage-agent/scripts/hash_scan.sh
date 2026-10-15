#!/usr/bin/env bash
# hash_scan.sh — produit un inventaire (chemin, taille, date de modification, hash sha256)
# d'un dossier de photos. Utilise par les subagents duplicate-detector et
# backup-integrity-checker via l'outil Bash, pour comparer deux inventaires sans jamais
# faire d'appel reseau et sans jamais modifier les fichiers scannes.
#
# Usage : ./hash_scan.sh <dossier> > inventaire.csv
#
# Sortie CSV : chemin;taille_octets;date_modification_iso;sha256

set -euo pipefail

DIR="${1:-}"
if [ -z "$DIR" ] || [ ! -d "$DIR" ]; then
  echo "Usage: $0 <dossier-a-scanner>" >&2
  exit 1
fi

echo "chemin;taille_octets;date_modification;sha256"

find "$DIR" -type f \( \
    -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.heic" \
    -o -iname "*.mov" -o -iname "*.mp4" -o -iname "*.raw" -o -iname "*.dng" \
  \) -print0 | while IFS= read -r -d '' f; do
    size=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f")
    mtime=$(stat -c%y "$f" 2>/dev/null || stat -f%Sm "$f")
    hash=$(sha256sum "$f" 2>/dev/null | cut -d' ' -f1 || shasum -a 256 "$f" | cut -d' ' -f1)
    echo "${f};${size};${mtime};${hash}"
done
