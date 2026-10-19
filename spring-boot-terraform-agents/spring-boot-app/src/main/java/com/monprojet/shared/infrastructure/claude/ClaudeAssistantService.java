package com.monprojet.shared.infrastructure.claude;

import com.anthropic.client.AnthropicClient;
import com.anthropic.models.messages.ContentBlock;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.TextBlock;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

/**
 * Adapter d'infrastructure qui appelle l'API Messages de Claude.
 * Dans une architecture DDD, le domaine ne connaît pas cette classe : il passe par un port
 * (interface) que cet adapter implémente.
 */
@Service
public class ClaudeAssistantService {

    private final AnthropicClient client;
    private final ClaudeProperties properties;

    public ClaudeAssistantService(AnthropicClient client, ClaudeProperties properties) {
        this.client = client;
        this.properties = properties;
    }

    public String resumerTicket(String texteDuTicket) {
        if (texteDuTicket == null || texteDuTicket.isBlank()) {
            throw new IllegalArgumentException("Le texte du ticket est vide");
        }

        MessageCreateParams params = MessageCreateParams.builder()
                .model(properties.model())
                .maxTokens(properties.maxTokens())
                .addUserMessage("Résume ce ticket client en 3 points : " + texteDuTicket)
                .build();

        Message message = client.messages().create(params);
        return extraireTexte(message.content());
    }

    /** La réponse est une liste de blocs : on ne garde que les blocs de texte. */
    static String extraireTexte(List<ContentBlock> blocs) {
        return blocs.stream()
                .flatMap(bloc -> bloc.text().stream())
                .map(TextBlock::text)
                .collect(Collectors.joining("\n"));
    }
}
