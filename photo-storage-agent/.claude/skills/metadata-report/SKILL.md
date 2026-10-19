---
name: metadata-report
description: A utiliser pour produire un rapport d'enrichissement de metadonnees photo (date, lieu, legende) dans un format Markdown standard. Utilise par le subagent metadata-enricher.
---

# Skill : metadata-report

Cette Skill definit le format de sortie standard du subagent `metadata-enricher`. Le rapport est
ecrit dans `reports/metadata/<lot>.md` (un lot = un dossier ou un import traite en une fois).

## Format du document

```markdown
# Rapport de metadonnees - <nom du lot>

Date d'analyse : <AAAA-MM-JJ>
Nombre de photos analysees : <N>

## Resume
- Photos avec date complete : <N>
- Photos sans date (metadonnee manquante) : <N>
- Photos avec geolocalisation : <N>
- Photos sans geolocalisation : <N>

## Detail par photo

| Fichier | Date (EXIF) | Lieu resolu | Source de la resolution | Legende proposee | Alerte |
|---|---|---|---|---|---|
| IMG_0012.jpg | 2026-07-03 | Lisbonne, Portugal | GPS EXIF -> geocodage inverse hors ligne | Vue sur le pont du 25 avril au coucher du soleil | - |
| IMG_0013.jpg | absente | inconnu | - | Interieur, piece non identifiable | Date manquante |

## Photos a verifier manuellement
Liste des fichiers pour lesquels l'agent n'est pas sur (date suspecte, legende incertaine,
plusieurs lieux possibles a quelques metres d'ecart). A valider par l'utilisateur.

## Notes
- Le lieu resolu doit toujours venir des coordonnees GPS presentes dans le fichier (geocodage
  inverse **hors ligne**, sans envoyer la coordonnee a un service web), jamais d'une supposition
  sur le contenu de l'image.
- La legende proposee decrit uniquement ce qui est visible sur l'image, sans extrapoler sur les
  personnes, leur identite ou le contexte.
- Aucune modification n'est faite sur les fichiers originaux : ce rapport est une proposition.
```

## Regles
- Toujours dater le rapport (ligne "Date d'analyse" en tete).
- Ne jamais indiquer une date ou un lieu comme certain si la source est une supposition : marquer
  "a verifier" dans la colonne Alerte.
- Ne jamais republier les coordonnees GPS precises ailleurs que dans ce rapport interne (pas dans
  un album public, une legende partagee, etc. — voir le subagent `privacy-reviewer` avant tout
  partage).
