
from agents import Agent, Runner, enable_verbose_stdout_logging, ModelSettings, function_tool
from dotenv import load_dotenv

# enable_verbose_stdout_logging()
load_dotenv()

@function_tool
def get_weather(city:str):
    """get the weather for given city"""
    return f"the current weather in {city} is cloudy."

main_agent = Agent(
    name="Assistant",
    instructions="you must be use get weather tools for user's query.",
    tools=[get_weather],
    model_settings=ModelSettings(
        tool_choice="none"
    )
)


result2 = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi?",
)

print(result2.final_output)


