---
name: ddd-module
description: A utiliser quand on cree un nouveau module metier (bounded context) dans l'application Spring Boot DDD. Ne pas utiliser pour une simple classe utilitaire.
---

# Creer un module DDD

Quand on te demande de creer un nouveau module metier :
1. Cree les packages `domain`, `application`, `infrastructure` sous `com.monprojet.<module>`.
2. Dans `domain` : entites, value objects, et le port du repository (interface), sans dependance Spring.
3. Dans `application` : les use cases (services applicatifs), sans dependance Spring.
4. Dans `infrastructure` : l'implementation JPA du repository et le controller REST.
5. Ecris un test unitaire du domaine et un test du use case avec mock du port (pas de Spring dans ces tests).
6. Lance `mvn test` sur le module avant de proposer le commit.
