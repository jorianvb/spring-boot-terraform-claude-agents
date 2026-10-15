---
name: privacy-scan-report
description: A utiliser pour produire un rapport de verification de confidentialite avant partage ou publication d'une photo, dans un format Markdown standard. Utilise par le subagent privacy-reviewer.
---

# Skill : privacy-scan-report

Format de sortie standard du subagent `privacy-reviewer`. Ecrit dans
`reports/privacy-scan/<lot-ou-photo>.md`.

## Format du document

```markdown
# Rapport de confidentialite avant partage - <nom du lot ou de la photo>

Date d'analyse : <AAAA-MM-JJ>

VERDICT : OK POUR PARTAGE
<!-- ou : VERDICT : A NETTOYER AVANT PARTAGE -->

## Elements trouves

### Metadonnees
| Fichier | Geolocalisation precise presente | Autres metadonnees sensibles |
|---|---|---|
| IMG_0012.jpg | Oui (GPS EXIF, precision ~5m) | Modele d'appareil, horodatage precis |

### Contenu visible sur l'image
| Fichier | Element visible | Description |
|---|---|---|
| IMG_0030.jpg | Plaque d'immatriculation | Vehicule visible en arriere-plan, plaque lisible |
| IMG_0031.jpg | Ecran d'ordinateur | Contenu de l'ecran partiellement lisible |

## Recommandation
- Retirer les metadonnees GPS avant tout partage (l'agent ne le fait pas lui-meme).
- Flouter ou recadrer les elements listes ci-dessus si le partage est public.

## Notes
- Les elements "visibles sur l'image" sont uniquement ceux reellement identifiables a l'oeil sur
  l'image analysee, jamais une supposition sur ce qui pourrait s'y trouver.
- Le verdict "OK POUR PARTAGE" signifie seulement qu'aucun element sensible n'a ete detecte parmi
  ceux recherches (GPS precis, information personnelle visible) — pas une garantie absolue.
```

## Regles
- Le VERDICT est toujours la premiere information du document, en une ligne sans ambiguite.
- L'agent ne retire jamais lui-meme les metadonnees ni ne modifie l'image : il recommande.
- A utiliser proactivement avant toute action de partage externe (reseau social, lien public,
  envoi a un tiers), pas seulement sur demande explicite.
