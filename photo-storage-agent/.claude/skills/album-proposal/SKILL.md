---
name: album-proposal
description: A utiliser pour produire une proposition de regroupement de photos en albums (evenement, date, lieu), dans un format Markdown standard. Utilise par le subagent album-curator.
---

# Skill : album-proposal

Format de sortie standard du subagent `album-curator`. Ecrit dans
`reports/albums/<lot>.md`.

## Format du document

```markdown
# Proposition d'albums - <nom du lot>

Date d'analyse : <AAAA-MM-JJ>
Nombre de photos considerees : <N>
(Necessite des photos deja enrichies en metadonnees — voir Skill `metadata-report`.)

## Albums proposes

### Album : "Lisbonne - decembre 2026"
- Periode : 2026-12-10 au 2026-12-15
- Lieu(x) : Lisbonne, Sintra
- Nombre de photos : 142
- Fichiers : voir `reports/albums/lisbonne-decembre-2026-liste.csv`

### Album : "Anniversaire - mars 2026"
- Periode : 2026-03-02
- Lieu(x) : domicile (pas de GPS, regroupement par date rapprochee uniquement)
- Nombre de photos : 38

## Photos orphelines (non rattachees a un album propose)
| Fichier | Raison |
|---|---|
| IMG_0500.jpg | Date isolee, aucune autre photo a +/- 2 jours |

## Action
Aucun fichier n'est deplace, renomme ou copie par l'agent. L'utilisateur valide les albums
proposes puis les cree lui-meme (ou via l'application de stockage photo utilisee).
```

## Regles
- Le regroupement se base sur la proximite de date et, quand elle existe, de geolocalisation —
  jamais sur une analyse du contenu visuel des personnes presentes.
- Un titre d'album propose reste descriptif (lieu + periode) ; il n'invente pas un contexte non
  verifiable ("voyage romantique", etc.).
- Les photos sans metadonnee suffisante restent listees comme "orphelines" plutot que forcees dans
  un album approximatif.
