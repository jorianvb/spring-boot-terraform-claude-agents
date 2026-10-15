---
name: packing-list
description: A utiliser pour generer une liste de bagages adaptee a une destination, une duree et un climat. Utiliser une fois l'itineraire et la periode fixes.
---

# Liste de bagages

Se baser sur le dossier destination (climat, culture, activites prevues dans l'itineraire) pour
produire une liste dans `docs/trips/<voyage>-bagages.md` organisee par categorie :

```markdown
# Bagages : <voyage>

## Vetements
- <adaptes au climat et a la duree>

## Sante et hygiene
- <adaptations climat/destination (moustiques, soleil fort, eau potable...)>

## Documents
- Passeport, visa, assurance voyage, reservations imprimees/telechargees

## Electronique
- Adaptateur de prise (<type utilise dans le pays>), chargeurs, batterie externe

## Specifique a la destination
- <equipement lie a une activite prevue dans l'itineraire : randonnee, plongee, etc.>
```
