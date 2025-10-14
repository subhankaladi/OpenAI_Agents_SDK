


from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()


@function_tool
def get_weather(city:str):
    """get weather for given number"""

    return f"the current weather in {city} is cloudy."


subhan_kaladi_agent = Agent(
    name="Subhan Kaladi Assistant",
    instructions="You are subhan kaladi assistant. Subhan kaladi is CEO of Codentic and AI Agents Developer."
)


main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    tools=[get_weather],
    handoffs=[subhan_kaladi_agent]
)


result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi and who is subhan kaladi?"
)

print(result.final_output)
