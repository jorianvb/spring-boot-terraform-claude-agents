---
name: jpa-entity
description: A utiliser quand on cree ou modifie une entite JPA et son repository Spring Data. Ne pas utiliser pour une classe du domaine pur (sans persistance).
---

# Entite JPA + repository

1. Creer l'entite JPA dans `infrastructure/persistence` (jamais dans `domain`).
2. Creer l'interface `Repository extends JpaRepository<Entity, Id>`.
3. Creer l'adapter qui implemente le port du domaine en s'appuyant sur ce repository.
4. Ecrire la migration Flyway correspondante dans `src/main/resources/db/migration` (ex: `V2__ajoute_commande.sql`).
   Le projet utilise `spring-boot-starter-flyway` (obligatoire avec Spring Boot 4) et `ddl-auto: validate`.
5. Ecrire un test d'integration avec `@DataJpaTest` + Testcontainers (base reelle, pas H2, pour rester fidele a la prod).
   Avec Spring Boot 4, ajouter les dependances de test `spring-boot-starter-data-jpa-test` et
   `spring-boot-testcontainers` + `org.testcontainers:postgresql` si elles ne sont pas deja dans le `pom.xml`.
