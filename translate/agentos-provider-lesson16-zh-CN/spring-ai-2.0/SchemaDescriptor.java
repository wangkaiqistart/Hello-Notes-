import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.definition.ToolDefinition;

public record SchemaDescriptor(
        String name, String description, String inputSchemaJson)
        implements ToolCallback {

    @Override
    public ToolDefinition getToolDefinition() {
        return ToolDefinition.builder()
                .name(name)
                .description(description == null ? "" : description)
                .inputSchema(inputSchemaJson)
                .build();
    }

    @Override
    public String call(String arguments) {
        throw new IllegalStateException("Tool execution forbidden in Provider");
    }
}
