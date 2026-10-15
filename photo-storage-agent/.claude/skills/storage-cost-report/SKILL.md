---
name: storage-cost-report
description: A utiliser pour produire un rapport d'analyse de croissance du stockage photo et une proposition de politique d'archivage, dans un format Markdown standard. Utilise par le subagent storage-cost-optimizer.
---

# Skill : storage-cost-report

Format de sortie standard du subagent `storage-cost-optimizer`. Ecrit dans
`reports/storage-cost/<AAAA-MM-JJ>.md`, avec un historique cumule dans
`reports/storage-history/historique.csv` (une ligne par execution : date, taille totale, nombre de
fichiers) pour pouvoir calculer une tendance.

## Format du document

```markdown
# Rapport de cout de stockage - <AAAA-MM-JJ>

Taille totale actuelle : <X Go>
Nombre total de fichiers : <N>
Croissance depuis la derniere mesure (<date precedente>) : <+X Go / +N fichiers>
(Si aucune mesure precedente : "Premiere mesure, pas de tendance disponible".)

## Repartition
| Categorie | Taille | % du total |
|---|---|---|
| Photos de l'annee en cours | <X Go> | <X%> |
| Photos de plus de 2 ans, jamais revues depuis l'import | <X Go> | <X%> |
| Videos | <X Go> | <X%> |

## Candidats a l'archivage (stockage moins cher / froid)
| Fichier ou dossier | Taille | Derniere consultation connue | Raison du candidat |
|---|---|---|---|
| /Photos/2021/voyage-ete | 3.1 Go | inconnue (pas de metadonnee d'acces) | Ancien et volumineux |

## Economie potentielle estimee
<Estimation chiffree si l'utilisateur valide l'archivage des candidats ci-dessus, avec la methode
de calcul explicitee (ex: difference de tarif entre stockage standard et stockage froid d'un
fournisseur donne, a la date du rapport).>

## Action
Aucun fichier n'est deplace ou archive par l'agent. Proposition a valider par l'utilisateur.
```

## Regles
- "Ancien" ne veut pas dire "sans valeur" : l'agent propose des candidats, il ne juge jamais qu'une
  photo doit etre supprimee ou merite moins d'etre gardee.
- Toute estimation de cout doit preciser sa source (tarif d'un fournisseur, a quelle date) plutot
  que d'inventer un chiffre.
- Ce rapport est pertinent a executer quand le volume devient une preoccupation (ex: alerte de
  quota), pas a chaque ajout de photo.
