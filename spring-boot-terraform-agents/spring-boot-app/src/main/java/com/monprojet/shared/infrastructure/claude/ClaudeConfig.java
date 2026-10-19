package com.monprojet.shared.infrastructure.claude;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Déclare un unique client Claude pour toute l'application (il est fait pour être réutilisé).
 * Spring appelle automatiquement sa méthode close() à l'arrêt de l'application.
 */
@Configuration
public class ClaudeConfig {

    @Bean
    public AnthropicClient anthropicClient(ClaudeProperties properties) {
        return AnthropicOkHttpClient.builder()
                .apiKey(properties.apiKey())
                .build();
    }
}
