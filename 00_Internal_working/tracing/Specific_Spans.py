from agents.tracing.processor_interface import TracingExporter
from agents.tracing.spans import Span
from agents.tracing.traces import Trace
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    trace,
    set_trace_processors

)
from agents.tracing.processors import BatchTraceProcessor


class CustomConsoleSpanExporter(TracingExporter):
    def export(self, items: list[Trace | Span]):
        for item in items:
            if isinstance(item, Trace):
                print(f"[Trace] ID: {item.trace_id} | Name: {item.name}")
            elif item.span_data.type == "generation":
                usage = item.span_data.usage or {}
                model = item.span_data.model
                user_input = item.span_data.input or []
                output = item.span_data.output or []

                print("🧠 Model Used:", model)
                print("📥 Input Tokens:", usage.get("input_tokens", "N/A"))
                print("📤 Output Tokens:", usage.get("output_tokens", "N/A"))

                if user_input:
                    print("🙋 User Asked:", user_input[-1].get("content", "N/A"))
                if output:
                    print("🤖 Bot Replied:", output[0].get("content", "N/A"))



exporter = CustomConsoleSpanExporter()
processor = BatchTraceProcessor(exporter)
set_trace_processors([processor,
                    #   default_processor() # sent to the dashbaord openai
                      ])  # override default processor(s)


gemini_api_key = ""

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model
)

# Wrap in a custom trace
with trace("Custom workflow"):
    result = Runner.run_sync(
        agent,
        input="What is my name"
    )

print(result.final_output)
