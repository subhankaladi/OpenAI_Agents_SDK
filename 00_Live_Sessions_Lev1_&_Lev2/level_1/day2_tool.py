from agents import ( Agent, Runner, function_tool, enable_verbose_stdout_logging )
from dotenv import load_dotenv


load_dotenv()
enable_verbose_stdout_logging()


@function_tool
def get_time() -> str:
    """Get the current time"""
    from datetime import datetime
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@function_tool
def add_numbers(a: int, b: int) -> str:
    """Add two numbers together
    Args:
        a: First number
        b: Second number
    """
    result = a + b
    return f"The sum of {a} and {b} is {result}"


agent = Agent(
    name="Assistant",
    instructions="you are helpful assistant",
    tools=[get_time, add_numbers]   
)


result = Runner.run_sync(
    agent,
    input="get current time and add number 5 + 3 "
)

print(result.final_output)