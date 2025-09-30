from agents import Agent, Runner, enable_verbose_stdout_logging, FunctionTool
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os

load_dotenv()
enable_verbose_stdout_logging()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=GEMINI_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash"
)

SCHEMA = {
    "additionalProperties": False,
    "type": "object",
    "properties": {
        "city": {"type": "string", "description": "the name of city"}
    },
    "required": [],

}

async def get_weather(ctx, city:str):
    return f"the current weather in {city} is cloudy."

weather_tool = FunctionTool(
    name="get_Weather",
    description="get the current weather for given city",
    params_json_schema=SCHEMA,
    on_invoke_tool=get_weather
)

main_agent = Agent(
    name="Orchestrator",
    instructions="you are helpful assistant",
    model=model,
    tools=[weather_tool]
)

result = Runner.run_sync(
    starting_agent=main_agent,
    input="what is the current weather in karachi ?.",
)

print(result.final_output)