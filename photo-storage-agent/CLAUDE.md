# CLAUDE.md

## Projet
Systeme d'agents Claude pour aider a gerer une bibliotheque de photos personnelles (une
application de stockage photo, pas une agence ni un service tiers) : enrichissement de
metadonnees, detection de doublons, verification de sauvegarde, proposition d'albums, analyse de
cout de stockage, verification de confidentialite avant partage. Aucun agent ne supprime, deplace,
renomme, partage ou publie un fichier a la place de l'utilisateur.

## Organisation des documents
- `reports/metadata/<lot>.md` : enrichissement de metadonnees (voir Skill `metadata-report`).
- `reports/duplicates/<lot>.md` : doublons et quasi-doublons detectes (voir Skill `duplicate-report`).
- `reports/backup-integrity/<date>.md` : verification de sauvegarde (voir Skill `backup-integrity-report`).
- `reports/albums/<lot>.md` : propositions d'albums (voir Skill `album-proposal`).
- `reports/storage-cost/<date>.md` et `reports/storage-history/historique.csv` : analyse de cout
  de stockage (voir Skill `storage-cost-report`).
- `reports/privacy-scan/<lot-ou-photo>.md` : verification de confidentialite avant partage (voir
  Skill `privacy-scan-report`).

## Enchainement normal
1. `metadata-enricher` : enrichit les metadonnees d'un nouvel import (date, lieu, legende).
2. `duplicate-detector` : a lancer avant tout archivage ou nettoyage (proactif).
3. `album-curator` : propose un regroupement une fois les metadonnees enrichies.
4. `storage-cost-optimizer` : a lancer quand le volume de stockage devient une preoccupation.
5. `backup-integrity-checker` : a lancer regulierement, idealement en tache planifiee (voir
   `agent-sdk/` et `scripts/`), pas seulement avant un evenement important.
6. `privacy-reviewer` : a lancer systematiquement avant tout partage ou publication externe.

## Regles
- Aucun agent ne supprime, deplace, renomme, archive, partage ou publie un fichier : ils
  analysent et rapportent, l'utilisateur decide et agit lui-meme (dans l'application de stockage
  photo ou son gestionnaire de fichiers).
- Un "quasi-doublon" ou un "candidat a l'archivage" n'est jamais presente comme une certitude.
- Les coordonnees GPS precises et les informations personnelles visibles sur une image sont
  traitees comme sensibles : jamais republiees ailleurs que dans le rapport interne concerne.
- Toute estimation (espace disque, cout de stockage) precise sa methode et sa date.
- Pas d'invention de donnees : si une metadonnee est absente, le dire explicitement plutot que de
  deviner.

## Documentation
Voir `docs/tutoriel-photo-storage-agent.md` pour le guide complet (architecture des agents,
automatisation, scenario complet, bonnes pratiques).
