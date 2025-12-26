from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import os
from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.agent import StopAtTools

load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
# enable_verbose_stdout_logging()


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)








@function_tool
def add_numbers(num1 : int, num2: int):

    sum = num1 + num2
    return f"num1 {num1} and {num2} total {sum}"


@function_tool
def get_weather(city):
    return f"the current weather in {city} is cloudy"


agent = Agent(
name="Assistant",
tools=[get_weather, add_numbers],
model=model,
tool_use_behavior=StopAtTools(
    stop_at_tool_names=["get_weather"] )
)

result = Runner.run_sync(
    agent,
    "what is current weather in karachi and what is 5 + 5 "
)

print(result.final_output)