import os
from random import random
from agents import Agent, OpenAIChatCompletionsModel,enable_verbose_stdout_logging, Runner, function_tool, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI
import requests

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)


@function_tool()
def how_many_jokes():
    """
    Get Random Number for jokes
    """
    print("how_many_jokes called")
    return random.randint(1, 10)

@function_tool
def get_weather(city: str) -> str:
    """
    Get the weather for a given city
    """
    print("get_weather called")
    try:
        result = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
        )

        data = result.json()

        return f"The current weather in {city} is {data["current"]["temp_c"]}C with {data["current"]["condition"]["text"]}."
    
    except Exception as e :
        return f"Could not fetch weather data due to {e}"

python_agent = Agent(
    name="PythonAgent",
    instructions="""
You are a Python programming assistant. You can help with Python code-related queries.
""",
    model=model,
)

agent = Agent(
    name="Assistant",
    instructions="""
if the user asks for jokes, first call 'how_many_jokes' function, then tell that jokess with numbers.
if the user asks for weather, call the 'get_weather' funciton with city name
If the user asks anything related to Python (definition, code, explanation, error, libraries, etc.) → always call 'transfer_to_pythonagent' function. 
""",
    model=model,
    handoffs=[python_agent],
    tools=[how_many_jokes, get_weather]
)

result = Runner.run_sync(
    agent,
    "tell me what is python in 3 lines and also the weather in Karachi"
)

print(result.final_output)