---
name: duplicate-report
description: A utiliser pour produire un rapport de doublons/quasi-doublons detectes dans une bibliotheque photo, dans un format Markdown standard. Utilise par le subagent duplicate-detector.
---

# Skill : duplicate-report

Format de sortie standard du subagent `duplicate-detector`. Ecrit dans
`reports/duplicates/<lot>.md`.

## Format du document

```markdown
# Rapport de doublons - <nom du lot>

Date d'analyse : <AAAA-MM-JJ>
Nombre de photos analysees : <N>
Methode : hash de contenu (sha256) pour les doublons exacts, comparaison perceptuelle pour les
quasi-doublons.

## Resume
- Groupes de doublons exacts trouves : <N>
- Groupes de quasi-doublons (a verifier) trouves : <N>
- Espace disque potentiellement recuperable (si suppression des doublons) : <taille estimee>

## Doublons exacts (meme contenu, hash identique)

### Groupe 1
| Fichier | Resolution | Date de creation | Emplacement | Recommandation |
|---|---|---|---|---|
| IMG_0012.jpg | 4032x3024 | 2026-07-03 | /Photos/2026/07 | Conserver (resolution la plus haute) |
| IMG_0012_copy.jpg | 4032x3024 | 2026-07-03 | /Photos/Backup | Doublon exact, candidat suppression |

## Quasi-doublons (a verifier, pas certains)
| Fichier A | Fichier B | Similarite estimee | Difference probable |
|---|---|---|---|
| IMG_0020.jpg | IMG_0021.jpg | ~95% | Rafale, legere difference de cadrage |

## Action
Aucune suppression n'est effectuee par l'agent. Ce rapport est une proposition a valider ligne par
ligne par l'utilisateur avant toute suppression ou archivage.

## Notes
- Un "quasi-doublon" n'est jamais presente comme un doublon certain.
- La recommandation "a conserver" se base sur la resolution, puis la date la plus ancienne en cas
  d'egalite — jamais sur une suppression automatique.
```

## Regles
- Jamais de suppression, deplacement ou renommage de fichier par l'agent lui-meme.
- Toujours distinguer clairement "doublon exact" (hash identique) de "quasi-doublon" (similarite
  estimee, incertaine).
- L'estimation d'espace recuperable est indicative, pas un chiffre d'engagement.
