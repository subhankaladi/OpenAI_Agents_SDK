from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
from dotenv import load_dotenv
import os
import random
import requests

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# 🔧 Joke tool
@function_tool
def how_many_jokes():
    return random.randint(1, 10)

# 🌤️ Weather tool
@function_tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        result = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
        )
        data = result.json()
        return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    except Exception as e:
        return f"Could not fetch weather data due to: {str(e)}"

# 🧠 Agent definition
agent = Agent(
    name="Subhan Kaladi",
    instructions=(
        "If the user asks for jokes, first call `how_many_jokes`, then tell that many jokes with numbers. "
        "If the user asks for weather, call the `get_weather` function with the city name."
    ),
    model=model,
    tools=[how_many_jokes, get_weather]
)

# 🏃 Run Agent
result = Runner.run_sync(
    agent,
    "What's the weather in Mumbai?",
    run_config=config
)

print(result.final_output)
