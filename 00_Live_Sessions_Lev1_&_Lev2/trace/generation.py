
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_trace_processors,  

)
from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor




exporter = ConsoleSpanExporter() 
processor = BatchTraceProcessor(exporter)
set_trace_processors([processor]) 


# ✅ STEP 3: Gemini model setup
gemini_api_key = "AIzaSyCW7VQCE4YLJocF8YcXijzp9l8StXXm5BQ"

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

result = Runner.run_sync(
    agent,
    input="how are you"
)

print(result.final_output)