package com.monprojet.shared.infrastructure.claude;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlock;
import com.anthropic.models.messages.TextBlock;
import java.util.List;
import org.junit.jupiter.api.Test;

/** Tests unitaires purs : aucun appel réseau, aucun contexte Spring. */
class ClaudeAssistantServiceTest {

    @Test
    void extraitUniquementLeTexteDesBlocs() {
        List<ContentBlock> blocs = List.of(
                ContentBlock.ofText(TextBlock.builder().text("Point 1").citations(List.of()).build()),
                ContentBlock.ofText(TextBlock.builder().text("Point 2").citations(List.of()).build()));

        assertThat(ClaudeAssistantService.extraireTexte(blocs)).isEqualTo("Point 1\nPoint 2");
    }

    @Test
    void refuseUnTicketVide() {
        AnthropicClient client = AnthropicOkHttpClient.builder().apiKey("cle-de-test").build();
        ClaudeAssistantService service =
                new ClaudeAssistantService(client, new ClaudeProperties("cle-de-test", "claude-sonnet-5", 1024));

        assertThatThrownBy(() -> service.resumerTicket("  "))
                .isInstanceOf(IllegalArgumentException.class);
        client.close();
    }
}
