from agents import Agent, Runner, function_tool, ModelSettings, enable_verbose_stdout_logging
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()


@function_tool
def get_weather(city:str):
    """get weather for given number"""

    return f"the current weather in {city} is cloudy."


main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    # tools=[get_weather],
    model_settings=ModelSettings(
        tool_choice="required"
    )
)


result = Runner.run_sync(
    main_agent,
    "hello?"
)

print(result.final_output)
