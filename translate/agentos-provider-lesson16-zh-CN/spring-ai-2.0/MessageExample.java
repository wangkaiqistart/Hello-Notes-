import java.util.List;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.ToolResponseMessage;
public class MessageExample {
    public static void messages() {
var intent = AssistantMessage.builder()
        .content("")
        .toolCalls(List.of(new AssistantMessage.ToolCall(
                "call-1", "function", "http_get",
                "{\"url\":\"https://example.com\"}")))
        .build();

var result = ToolResponseMessage.builder()
        .responses(List.of(new ToolResponseMessage.ToolResponse(
                "call-1", "http_get", "{\"status\":200}")))
        .build();
    }
}
