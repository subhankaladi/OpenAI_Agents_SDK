from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()


@function_tool
def get_weather(city:str):
    """get weather for given city"""

    return f"the current weather in {city} is cloudy"


main_agent = Agent(
    name="Assistant",
    instructions="you are helpfull assistant",
    tools=[get_weather],
)


try :
    result = Runner.run_sync(
    main_agent,
    "what is current weather in karachi ?",
)
    print(result.final_output)

except Exception as ae:
    print(f"Exception raised: {type(ae).__name__} - {str(ae)}")

