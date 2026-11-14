import java.util.List;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.openai.OpenAiChatOptions;
import org.springframework.ai.tool.ToolCallback;

public final class ModelRound {
    public static ChatResponse call(
            ChatModel client, String modelName,
            Double temperature, Integer maxOutputTokens,
            List<Message> messages, List<ToolCallback> toolDescriptions) {

        var options = OpenAiChatOptions.builder()
                .model(modelName)
                .temperature(temperature)
                .maxCompletionTokens(maxOutputTokens)
                .toolCallbacks(toolDescriptions)
                .strict(false)
                .maxRetries(0)
                .build();

        return client.call(new Prompt(messages, options));
    }
}
