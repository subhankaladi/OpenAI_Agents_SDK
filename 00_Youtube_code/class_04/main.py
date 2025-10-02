from agents import Agent, Runner, enable_verbose_stdout_logging
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




weather_agent = Agent(
    name="weather_agent",
    instructions="you always respond today's weather is cloudy.",
    model=model
)

subhan_kaladi_agent = Agent(
    name="subhan_kaladi_agent",
    instructions="you are a subhan kaladi agent. subhan kaladi is full stack and AI Developer",
    model=model
)

weather_agent_as_tool = weather_agent.as_tool(
    tool_name="weather_tool",
    tool_description="you are weather tool"
)

subhan_kaladi_agent_as_tool = subhan_kaladi_agent.as_tool(
    tool_name="subhan_kaladi_tool",
    tool_description="you are subhan kaladi assistant."
)

main_agent = Agent(
    name="Orchestrator",
    instructions="you are helpful assistant.",
    model=model,
    # handoffs=[weather_agent, subhan_kaladi_agent]
    tools=[subhan_kaladi_agent_as_tool, weather_agent_as_tool]
)

result = Runner.run_sync(
    starting_agent=main_agent,
    input="what is the current weather in karachi and who is subhan kaladi?",
)

print(result.final_output)