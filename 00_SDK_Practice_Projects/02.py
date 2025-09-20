from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()


@function_tool
def get_weather(city:str):
    """get weather for given number"""

    raise ValueError("Error a gya")


@function_tool
def add_numbers(a: int, b: int):
    """sum the for given number"""
    sum = a + b
    return f"first num is {a} and sec is {b} total {sum}"

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    tools=[get_weather, add_numbers]
)


result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi and also what is 5 + 3 ?"
)

print(result.final_output)
