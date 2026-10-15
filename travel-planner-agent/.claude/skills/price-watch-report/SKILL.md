---
name: price-watch-report
description: A utiliser pour formater un rapport de veille tarifaire (vols/hebergements). Utiliser systematiquement en sortie du subagent price-watcher.
---

# Format du rapport de veille prix

Ajouter une ligne a `reports/price-history/<recherche>.md` (creer le fichier avec cet en-tete si absent) :

```markdown
# Historique de prix : <recherche>

Budget cible : <montant>

| Date | Prix releve | Source | Variation vs releve precedent | Alerte |
|---|---|---|---|---|
| 2026-10-15 | 480 EUR | <source> | - | non |
```

Si le prix est sous le budget cible ou en baisse significative (>= 15% vs le dernier releve),
mettre "ALERTE PRIX" en tete de la reponse, avant le tableau.
Ne jamais confondre un prix affiche sans taxes/bagages avec un prix final : preciser ce qui est inclus.
