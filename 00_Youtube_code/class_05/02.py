from agents import Agent, Runner, enable_verbose_stdout_logging, set_tracing_disabled
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from agents import handoff
from pydantic import BaseModel

load_dotenv()
# enable_verbose_stdout_logging()
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


weather_agent = Agent(
    name="weather_agent",
    instructions="you are weather assistant. always respond today's weather is cloudy. ",
    model=model
)
class Input(BaseModel):
    city:str

def invoking(ctx, input:Input):
    print(f"handoff ho gya city ka name tha {input.city}")


handoff_func = handoff(
    agent=weather_agent,
    tool_name_override="weather_agent",
    tool_description_override="handoff to the weather agent.",
    on_handoff=invoking,
    input_type=Input

)

main_agent = Agent(
    name="Orchestrator",
    instructions="you are helpful assistant.",
    model=model,
    handoffs=[handoff_func]
)

result = Runner.run_sync(
    starting_agent=main_agent,
    input="what is current weather in karachi?",
)

print(result.final_output)