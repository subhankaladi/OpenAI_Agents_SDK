from agents import (
    Agent,
    set_tracing_disabled,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    trace,
    set_trace_processors,  

)

from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor, default_processor
# from agents.tracing.processor_interface import TracingExporter

# # ✅ STEP 1: Enable tracing
# set_tracing_disabled(disabled=True)  



# ✅ STEP 2: Setup your custom exporter/processor
exporter = ConsoleSpanExporter()  # or use BackendSpanExporter()
processor = BatchTraceProcessor(exporter)
set_trace_processors([processor, 
                      default_processor() # sent to the dashbaord openai
                      ])  # override default processor(s)

# ✅ STEP 3: Gemini model setup
gemini_api_key = ""

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# ✅ STEP 4: Define agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model
)

# ✅ STEP 5: Wrap in a custom trace
with trace("Subhan workflow"):
    result = Runner.run_sync(
        agent,
        input="how are you"
    )

# ✅ STEP 6: Output
print(result.final_output)
