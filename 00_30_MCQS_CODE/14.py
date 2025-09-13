


from agents import Agent, Runner, function_tool, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, MaxTurnsExceeded
import os
from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()

load_dotenv()
set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)












@function_tool
def get_weather(city:str):
 return f"The current weather is {city} is cloudy"

main_agent = Agent(
    name="Assistant",
    instructions="you are python asssitant",
    model=model,
    tools=[get_weather]

)

try:
 result = Runner.run_sync(main_agent, "what is cuurent weather in karachi", max_turns=2)
 print(result.final_output)

except MaxTurnsExceeded as e:
 print("Too many turns")

