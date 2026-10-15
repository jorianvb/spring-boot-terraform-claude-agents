---
name: spring-rest-client
description: A utiliser quand on doit appeler une API externe (appel sortant) depuis l'application Spring Boot. Ne pas utiliser pour exposer un endpoint entrant.
---

# Client HTTP declaratif Spring 6

1. Definir une interface annotee avec `@HttpExchange` decrivant les appels (GET/POST/...) : c'est une facade declarative au-dessus de RestClient/WebClient, pas un remplacement bas niveau.
2. Creer un `HttpServiceProxyFactory` configure avec un `RestClient` ou `WebClient` dans une classe `@Configuration`.
3. Gerer les erreurs HTTP avec un `ResponseErrorHandler` dedie (ne jamais laisser une exception technique remonter telle quelle au domaine).
4. Ecrire un test avec `MockWebServer` (ou `WireMock`) simulant les reponses de l'API externe.
5. Externaliser l'URL de base et les timeouts dans `application.yml` (jamais en dur dans le code).
