from agents import (
    Agent, Runner, OpenAIChatCompletionsModel,
    AsyncOpenAI, trace,
    set_trace_processors
)
from agents.tracing.processors import TracingProcessor, TracingExporter, BatchTraceProcessor


# ✅ Helper function to safely extract label from span
def get_span_label(span):
    try:
        sd = span.span_data
        if hasattr(sd, "name"):
            return sd.name
        elif hasattr(sd, "model"):
            return f"GenerationSpan ({sd.model})"
        elif hasattr(sd, "tool_name"):
            return f"ToolCall: {sd.tool_name}"
        else:
            return sd.__class__.__name__
    except Exception:
        return "UnknownSpan"


# ✅ Custom processor for console logs
class MyProcessor(TracingProcessor):
    def on_trace_start(self, trace):
        print(f"\n[TRACE START] {trace.name}")

    def on_trace_end(self, trace):
        print(f"[TRACE END] {trace.name}\n")

    def on_span_start(self, span):
        print(f"  └── [SPAN START] {get_span_label(span)}")

    def on_span_end(self, span):
        print(f"  └── [SPAN END] {get_span_label(span)}")

    def shutdown(self):
        print("[SHUTDOWN]")

    def force_flush(self):
        print("[FLUSH]")


# ✅ Custom exporter to log file
class MyExporter(TracingExporter):
    def export(self, items):
        with open("log.txt", "a", encoding="utf-8") as f:
            for itm in items:
                try:
                    label = get_span_label(itm)
                    f.write(f"[EXPORT] {itm.__class__.__name__} -> {label}\n")
                except Exception as e:
                    f.write(f"[EXPORT ERROR] {e}\n")


# ✅ Register tracing processor + exporter
set_trace_processors([
    MyProcessor(),
    BatchTraceProcessor(MyExporter())
])


# ✅ Agent setup
client = AsyncOpenAI(
    api_key="",  
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)


python_agent = Agent(
    name="Python Expert",
    instructions="You are python expert",
    model=model
)
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model,
    handoffs=[python_agent]
)

# ✅ Run with trace
with trace("Assistant workflow"):
    result = Runner.run_sync(
        agent,
        input="what is python tell me in 3 lines"
    )

print("\n🧠 Final Output:\n", result.final_output)
