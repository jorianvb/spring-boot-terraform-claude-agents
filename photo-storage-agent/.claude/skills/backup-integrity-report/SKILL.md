---
name: backup-integrity-report
description: A utiliser pour produire un rapport de verification d'integrite d'une sauvegarde photo, dans un format Markdown standard. Utilise par le subagent backup-integrity-checker.
---

# Skill : backup-integrity-report

Format de sortie standard du subagent `backup-integrity-checker`. Ecrit dans
`reports/backup-integrity/<AAAA-MM-JJ>.md` (un fichier par execution, pour garder l'historique).

## Format du document

```markdown
# Rapport d'integrite de sauvegarde - <AAAA-MM-JJ>

STATUT GLOBAL : SAUVEGARDE A JOUR
<!-- ou : STATUT GLOBAL : ACTION REQUISE -->

Source : <chemin ou identifiant de la bibliotheque principale>
Sauvegarde : <chemin, service ou identifiant de la sauvegarde>
Nombre de fichiers source : <N>
Nombre de fichiers sauvegardes : <N>

## Resume
- Fichiers presents dans la source mais absents de la sauvegarde : <N>
- Fichiers avec hash different entre source et sauvegarde (corruption possible) : <N>
- Fichiers presents uniquement dans la sauvegarde (orphelins) : <N>

## Fichiers non sauvegardes
| Fichier | Date de creation | Taille |
|---|---|---|
| IMG_0099.jpg | 2026-10-10 | 4.2 Mo |

## Fichiers avec hash different (corruption suspectee)
| Fichier | Hash source | Hash sauvegarde | Derniere sauvegarde connue |
|---|---|---|---|

## Fichiers orphelins (presents seulement dans la sauvegarde)
| Fichier | Date dans la sauvegarde |
|---|---|

## Action recommandee
<Ce que l'utilisateur devrait faire : relancer une sauvegarde, verifier manuellement tel fichier,
rien a faire.>
```

## Regles
- La premiere ligne du document est toujours le statut global, en une phrase sans ambiguite :
  "SAUVEGARDE A JOUR" ou "ACTION REQUISE" — c'est ce qu'une personne presse doit voir en premier.
- L'agent compare des hash et des listes de fichiers, il ne restaure et ne supprime jamais rien.
- Concu pour une execution reguliere planifiee (voir `agent-sdk/` et le dossier `scripts/`), pas
  seulement avant un evenement important : la valeur vient de la regularite.
