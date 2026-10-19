package com.monprojet.shared.infrastructure.claude;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

/**
 * Configuration de l'appel à Claude, lue depuis application.yml (préfixe "anthropic").
 * La clé API vient de la variable d'environnement ANTHROPIC_API_KEY, jamais du code.
 */
@Validated
@ConfigurationProperties(prefix = "anthropic")
public record ClaudeProperties(
        String apiKey,
        @NotBlank String model,
        @Positive long maxTokens) {
}
