from agents import Agent, Runner, enable_verbose_stdout_logging, set_tracing_disabled
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from agents import Handoff

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


weather_agent = Agent(
    name="weather_agent",
    instructions="you are weather assistant. always respond today's weather is cloudy. ",
    model=model
)

SCHEMA = {
    "additionalProperties": False,
    "type": "object",
    "properties": {},
    "required": [],
}

async def invoking_weather_agent(ctx, input):
    return weather_agent

handoff_obj = Handoff(
    tool_name="transfer_to_weather_agent",
    tool_description="handoff to the weather agent",
    input_json_schema=SCHEMA,
    on_invoke_handoff=invoking_weather_agent,
    agent_name="weather_agenttt"
)


main_agent = Agent(
    name="Orchestrator",
    instructions="you are helpful assistant.",
    model=model,
    handoffs=[handoff_obj]
)

result = Runner.run_sync(
    starting_agent=main_agent,
    input="what is current weather in karachi?",
)

print(result.final_output)