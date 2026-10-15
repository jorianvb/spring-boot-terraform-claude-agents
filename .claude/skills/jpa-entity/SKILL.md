---
name: jpa-entity
description: A utiliser quand on cree ou modifie une entite JPA et son repository Spring Data. Ne pas utiliser pour une classe du domaine pur (sans persistance).
---

# Entite JPA + repository

1. Creer l'entite JPA dans `infrastructure/persistence` (jamais dans `domain`).
2. Creer l'interface `Repository extends JpaRepository<Entity, Id>`.
3. Creer l'adapter qui implemente le port du domaine en s'appuyant sur ce repository.
4. Ecrire la migration de schema (Flyway ou Liquibase) correspondante dans `src/main/resources/db/migration`.
5. Ecrire un test d'integration avec `@DataJpaTest` + Testcontainers (base reelle, pas H2, pour rester fidele a la prod).
