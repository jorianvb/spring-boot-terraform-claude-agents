# CLAUDE.md

## Projet
Systeme d'agents Claude pour planifier un voyage soi-meme : recherche de destination, veille
tarifaire, construction d'itineraire, reperage d'evenements locaux, budget. Ce n'est PAS une
agence de voyage : aucun agent ne reserve, n'achete ni ne cree de compte a la place de l'utilisateur.

## Organisation des documents
- `docs/destinations/<ville>.md` : dossiers de recherche destination (voir Skill `destination-dossier`).
- `docs/itineraries/<voyage>.md` : itineraires jour par jour (voir Skill `itinerary-format`).
- `docs/trips/<voyage>.md` : suivi consolide d'un voyage (tenu par le subagent `trip-journal-writer`).
- `reports/price-history/<recherche>.md` : historique de veille tarifaire (voir Skill `price-watch-report`).

## Enchainement normal pour planifier un voyage
1. `destination-researcher` : produit le dossier destination.
2. `itinerary-builder` : produit l'itineraire a partir du dossier destination + contraintes (dates, budget, interets).
3. `local-events-scout` : verifie les evenements locaux sur la fenetre de dates choisie.
4. `price-watcher` : surveille les prix (manuellement ou en tache planifiee, voir agent-sdk/ et
   `.github/workflows/price-watch.yml` a la racine du depot).
5. `trip-journal-writer` : consolide tout dans un document de suivi unique.

## Regles
- Aucun agent ne reserve, n'achete, ne cree de compte ou n'entre une information de paiement : ils
  cherchent et rapportent, l'utilisateur decide et agit lui-meme.
- Toute information sensible (visa, securite, change) doit etre datee et sourcee.
- Un prix releve est toujours accompagne de sa source et de la date de releve.
- Pas d'invention de chiffres : si une info n'est pas trouvee, le dire explicitement.

## Documentation
Voir `docs/tutoriel-travel-planner-agent.md` pour le guide complet (architecture des agents,
veille automatisee, bonnes pratiques).
