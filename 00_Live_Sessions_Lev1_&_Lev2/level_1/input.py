from agents import Agent, Runner, handoff, function_tool, SQLiteSession
from dotenv import load_dotenv
from agents import enable_verbose_stdout_logging
enable_verbose_stdout_logging()
from agents.extensions import handoff_filters
from agents.handoffs import HandoffInputData


load_dotenv()

@function_tool
def add_numbers(a: int, b:int):
    """add given two numbers """

    sum = a + b
    return f"first num is {a} and sec num is {b} and total is {sum}"

weather_agent = Agent(
    name="get_weather",
    instructions="today karachi weather is cloudy and 30C Temp",
)

session = SQLiteSession("conversation_123")

main_agent = Agent(
    name="Assistant",
    instructions="you are helpfull assistant",
    handoffs=[handoff(agent=weather_agent, input_filter="")],
    tools=[add_numbers]
)

result = Runner.run_sync(
main_agent,
"add 5 + 7",
session=session
)

print(result.final_output)


result2 = Runner.run_sync(
main_agent,
"what is current weather in karachi ?",
session=session
)

print(result2.final_output)
