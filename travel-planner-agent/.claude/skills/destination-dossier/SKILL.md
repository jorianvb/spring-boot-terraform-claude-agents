---
name: destination-dossier
description: A utiliser pour formater le resultat d'une recherche de destination (securite, visa, budget, climat, transport, culture). Utiliser systematiquement en sortie du subagent destination-researcher.
---

# Format du dossier destination

Ecrire le resultat dans `docs/destinations/<ville-ou-pays>.md` avec cette structure :

```markdown
# Destination : <nom>

_Derniere mise a jour : <date>_

## Resume en une ligne
<une phrase : ce qu'il faut savoir avant tout>

## Meilleure periode
<mois conseilles, climat attendu, periodes a eviter (mousson, canicule, haute saison touristique)>

## Formalites d'entree
- Visa : <regle, duree de validite, lien source officiel>
- Vaccins/sante : <recommandations, lien source officiel>
- Duree de validite du passeport exigee

## Securite
<niveau de vigilance recommande, zones a eviter si mentionnees, source (ministere des affaires
etrangeres ou equivalent), date de consultation>

## Budget indicatif
- Hebergement (nuit) : <fourchette>
- Repas (jour) : <fourchette>
- Transport local (jour) : <fourchette>
- Monnaie et taux indicatif

## Transport local
<comment se deplacer sur place : metro, bus, taxi, location de vehicule, applications utiles>

## Culture et usages
<pourboires, habillement, jours feries locaux, particularites a connaitre>

## Sources
- <lien> (consulte le <date>)
- <lien> (consulte le <date>)
```

Toujours dater chaque information sensible (visa, securite, change) : elle peut changer rapidement.
