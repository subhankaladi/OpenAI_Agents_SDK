from agents import Agent, Runner, AgentsException, function_tool
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_weather(city:str):
    """get weather for given city"""

    return f"the current weather in {city} is cloudy"


main_agent = Agent(
    name="Assistant",
    instructions="you are helpfull assistant",
    tools=[get_weather]
)


try :
    result = Runner.run_sync(
    main_agent,
    "what is current weather in karachi ?",
    max_turns=1
)
    print(result.final_output)

except AgentsException as ae:
    print(f"Agent Base exception is raise {ae}")

