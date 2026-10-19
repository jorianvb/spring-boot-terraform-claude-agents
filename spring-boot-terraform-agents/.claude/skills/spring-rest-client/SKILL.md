---
name: spring-rest-client
description: A utiliser quand on doit appeler une API externe (appel sortant) depuis l'application Spring Boot. Ne pas utiliser pour exposer un endpoint entrant.
---

# Client HTTP declaratif (Spring Framework 6+ / Spring Boot 3+)

1. Definir une interface annotee avec `@HttpExchange` decrivant les appels (GET/POST/...) : c'est une facade declarative au-dessus de RestClient/WebClient, pas un remplacement bas niveau.
2. Enregistrer l'interface : avec Spring Boot 4 / Spring Framework 7, `@ImportHttpServices` sur une classe
   `@Configuration` suffit (l'URL de base se regle dans `application.yml`) ; sinon, creer un
   `HttpServiceProxyFactory` a partir d'un `RestClient` (via `RestClientAdapter.create(restClient)`).
3. Gerer les erreurs HTTP avec `RestClient.Builder#defaultStatusHandler(...)` (ne jamais laisser une exception technique remonter telle quelle au domaine).
4. Ecrire un test avec `MockWebServer` (ou `WireMock`) simulant les reponses de l'API externe.
5. Externaliser l'URL de base et les timeouts dans `application.yml` (jamais en dur dans le code).
