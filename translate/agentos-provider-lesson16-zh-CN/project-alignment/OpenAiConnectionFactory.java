import java.time.Duration;
import io.micrometer.observation.ObservationRegistry;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.ai.openai.OpenAiChatOptions;

public final class OpenAiConnectionFactory {
    public static OpenAiChatModel create(
            String apiBaseUrl, String apiKey, Duration timeout,
            ObservationRegistry observationRegistry) {
        var options = OpenAiChatOptions.builder()
                .baseUrl(apiBaseUrl)
                .apiKey(apiKey)
                .timeout(timeout)
                .maxRetries(0)
                .build();

        return OpenAiChatModel.builder()
                .options(options)
                .observationRegistry(observationRegistry)
                .build();
    }
}
