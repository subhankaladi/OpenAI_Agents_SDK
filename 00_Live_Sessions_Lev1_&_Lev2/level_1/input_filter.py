from agents import Agent, HandoffInputData, Runner, SQLiteSession, handoff, function_tool, ModelSettings
from dotenv import load_dotenv
from agents import enable_verbose_stdout_logging


enable_verbose_stdout_logging()
load_dotenv()

get_weather = Agent(
    name="get_weather",
    instructions="You must respond: 'Today the weather is cloudy."
)


@function_tool
def add_numbers(a:int, b:int):
    """sum for given numbers"""
    sum = a + b

    return f"a is {a} and b is {b} total {sum}"

def my_filter(data: HandoffInputData) -> HandoffInputData:

    return HandoffInputData(
        input_history=data.input_history,
        pre_handoff_items=(),
        new_items=data.new_items
    )


handoff_weather_obj = handoff(
    agent=get_weather,
    input_filter=my_filter
)

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant. if the user's query about add numbers you can call add_numbers tool. if the user's query about weather you can delegate get_weather.",
    handoffs=[handoff_weather_obj],
    tools=[add_numbers],
    model_settings=ModelSettings(
        parallel_tool_calls=False
    )
)

session = SQLiteSession("conversation_123")


result = Runner.run_sync(
    main_agent,
    "Hello",
    session=session
)
print(result.final_output)


result2 = Runner.run_sync(
    main_agent,
    "What is 5 + 3 and  the current weather in karachi.",
    # session=session
)
print(result2.final_output)

