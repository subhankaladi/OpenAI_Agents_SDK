from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()


#add value error in tool and add 1 turn in run

@function_tool
def get_weather(city:str):
    """get weather for given number"""

    return f"the current weather in {city} is cloudy."


main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    tools=[get_weather]
)


result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi ?"
)

print(result.final_output)
