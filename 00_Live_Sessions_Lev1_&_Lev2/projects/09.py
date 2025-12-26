from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()

@function_tool
def weather_tool(city:str):
    """get the weather for given city"""

    return f"the current weather in {city} is cloudy"
    

get_weather = Agent(
    name="get_weather",
    instructions="if the user's query related to weather you can call weather_tool function.",
    tools=[weather_tool]
)


main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    handoffs=[get_weather]
)

result = Runner.run_sync(
    main_agent,
    "what is current weather in karachi?",
    max_turns=2
)

print(result.final_output)
