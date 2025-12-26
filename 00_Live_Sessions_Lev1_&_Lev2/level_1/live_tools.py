from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import requests
load_dotenv()

@function_tool
def get_weather(city: str) -> str:
    """
    Get the weather for a given city
    """
    try:
        result = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
        )

        data = result.json()

        return f"The current weather in {city} is {data["current"]["temp_c"]}C with {data["current"]["condition"]["text"]}."
    
    except Exception as e :
        return f"Could not fetch weather data due to {e}"
    
main_agent = Agent(
    name="main_agent",
    instructions="you are helpful assistant.",
    tools=[get_weather]
)

result = Runner.run_sync(
    main_agent,
    "get current weather of karachi."
)

print(result.final_output)