---
name: itinerary-format
description: A utiliser pour formater un itineraire de voyage jour par jour. Utiliser systematiquement en sortie du subagent itinerary-builder.
---

# Format de l'itineraire (Skill itinerary-format)

Ecrire le resultat dans `docs/itineraries/<voyage>.md` avec cette structure :

```markdown
# Itineraire : <voyage> (<dates>)

## Vue d'ensemble
<nombre de jours, rythme (intense/tranquille), budget total estime>

## Jour 1 - <date> - <theme ou zone geographique>
- Matin : <activite> (horaire d'ouverture, duree estimee)
- Midi : <suggestion repas / zone>
- Apres-midi : <activite>
- Soir : <activite ou repos>
- A reserver a l'avance : <oui/non, lien si connu>
- Alternative mauvais temps : <option>

## Jour 2 - ...

## Budget estime par jour
| Jour | Transport | Repas | Activites | Total |
|---|---|---|---|---|

## A reserver avant le depart
- <liste des billets/reservations a prendre en avance, avec delai conseille>
```

Grouper les activites par proximite geographique pour limiter les trajets inutiles.
