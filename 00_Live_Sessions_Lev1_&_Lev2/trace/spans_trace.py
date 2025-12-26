from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor
from agents.tracing import add_trace_processor

load_dotenv()


console_exporter = ConsoleSpanExporter()
# console_processor = BatchTraceProcessor(console_exporter)
add_trace_processor(console_exporter)


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
)
    print(result.final_output)

except Exception as ae:
    print(f"Exception raise {ae}")


