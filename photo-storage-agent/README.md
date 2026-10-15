# photo-storage-agent

Systeme d'agents Claude pour aider a gerer une bibliotheque de photos personnelles : enrichir les
metadonnees, detecter les doublons, verifier les sauvegardes, proposer des albums, suivre le cout
de stockage, verifier la confidentialite avant un partage. Ce n'est pas une application de
stockage photo en soi : c'est une couche d'agents qui analysent et rapportent au-dessus d'une
bibliotheque existante (locale, NAS, ou cloud). Aucun agent ne supprime, deplace, partage ou
publie un fichier a la place de l'utilisateur.

👉 [Tutoriel complet](docs/tutoriel-photo-storage-agent.md)

## Structure
```
photo-storage-agent/
├── CLAUDE.md                  # memoire du projet, regles, enchainement des agents
├── .claude/
│   ├── agents/                # 6 subagents (lecture/analyse/rapport uniquement)
│   └── skills/                # format de sortie standard pour chaque subagent
├── agent-sdk/                 # execution planifiee des subagents hors session interactive
├── scripts/                   # script local d'inventaire (hash, taille, date)
├── docs/                      # tutoriel
└── reports/                   # rapports generes (metadonnees, doublons, sauvegarde, albums,
                                # cout de stockage, confidentialite) — pas commis par defaut
```

## Les 6 subagents
| Subagent | Role | Skill de sortie |
|---|---|---|
| `metadata-enricher` | Lit et complete les metadonnees (date, lieu, legende) | `metadata-report` |
| `duplicate-detector` | Repere les doublons et quasi-doublons | `duplicate-report` |
| `backup-integrity-checker` | Verifie qu'une sauvegarde est complete et non corrompue | `backup-integrity-report` |
| `album-curator` | Propose un regroupement de photos en albums | `album-proposal` |
| `storage-cost-optimizer` | Analyse la croissance du stockage, propose un archivage | `storage-cost-report` |
| `privacy-reviewer` | Verifie les metadonnees/contenus sensibles avant partage | `privacy-scan-report` |
