---
name: security-review
description: A utiliser avant une mise en production pour une revue de securite ciblee du code modifie. Ne pas utiliser comme substitut a un vrai audit de securite externe.
---

# Revue de securite ciblee

Sur le diff ou le module concerne, verifier :
1. Injections (SQL, commande, LDAP) : toute entree utilisateur doit passer par des requetes parametrees.
2. Secrets en dur dans le code, les logs, ou les messages de commit.
3. Configuration CORS trop permissive.
4. Controles d'authentification/autorisation sur chaque nouvel endpoint.
5. Dependances avec vulnerabilites connues (verifier le rapport `mvn dependency-check` si disponible).

Produire une liste de constats classes par severite, avec pour chacun un correctif propose.
Ne jamais appliquer un correctif de securite sans validation humaine explicite.
