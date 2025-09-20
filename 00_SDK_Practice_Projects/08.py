from agents import Agent, HandoffInputData, Runner, handoff
from dotenv import load_dotenv
from agents import enable_verbose_stdout_logging


enable_verbose_stdout_logging()
load_dotenv()

get_weather = Agent(
    name="get_weather",
    instructions="You must respond: 'Today the weather is cloudy."
)


def my_filter(data: HandoffInputData) -> HandoffInputData:

    return HandoffInputData(
        input_history=data.input_history,
        pre_handoff_items=data.pre_handoff_items,
        new_items=()
    )


handoff_weather_obj = handoff(
    agent=get_weather,
    input_filter=my_filter
)

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    handoffs=[handoff_weather_obj],
)


result = Runner.run_sync(
    main_agent,
    "What is the current weather in karachi.",
)
print(result.final_output)

