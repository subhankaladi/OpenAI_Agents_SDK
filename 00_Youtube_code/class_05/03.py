from agents import Agent, Runner, SQLiteSession, enable_verbose_stdout_logging, function_tool, set_tracing_disabled
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from agents import handoff
from agents import HandoffInputData
from agents import ModelSettings

load_dotenv()
enable_verbose_stdout_logging()
set_tracing_disabled(True)


GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=GEMINI_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash"
)

def input_history(data: HandoffInputData)-> HandoffInputData:
    return HandoffInputData(
        input_history=(),
        pre_handoff_items=data.pre_handoff_items,
        new_items=data.new_items
)

weather_agent = Agent(
    name="weather_agent",
    instructions="you are weather assistant. always respond today's weather is cloudy. ",
    model=model
)


handoff_func = handoff(
    agent=weather_agent,
    input_filter=input_history
    
)


main_agent = Agent(
    name="Orchestrator",
    instructions="you are helpful assistant.",
    model=model,
    handoffs=[handoff_func],
)


session = SQLiteSession("conversation_123")


result1 = Runner.run_sync(
    starting_agent=main_agent,
    input="hello",
    session=session
)
print(result1.final_output)

print("Runnnnnnnnnnnnnnnnnnnneeeeeeerrrrrrr 22222")

result2 = Runner.run_sync(
    starting_agent=main_agent,
    input="who is subhan kaladi and what is current weather in karachi?",
    session=session
)

print(result2.final_output)