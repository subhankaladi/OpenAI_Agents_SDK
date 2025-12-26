

from agents import Agent, Runner, custom_span, function_tool, trace
from dotenv import load_dotenv
from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor
from agents.tracing import add_trace_processor

load_dotenv()

# console_exporter = ConsoleSpanExporter()
# console_processor = BatchTraceProcessor(console_exporter)
# add_trace_processor(console_processor)

@function_tool
def get_weather(city:str):
    """get weather for given city"""

    return f"the current weather in {city} is cloudy"


main_agent = Agent(
    name="Assistant",
    instructions="you are helpfull assistant",
    tools=[get_weather]
)

user_query = "what is current weather in hyd ?"

normalized_city = "hyderabad" if "hyd" in user_query else user_query

try :
    with trace(workflow_name="Kaladi"):
        with custom_span("QueryPreprocessing", data={"raw_query": user_query, "normalized": normalized_city}):
            result = Runner.run_sync(
            main_agent,
            "what is current weather in hyd ?",
            )
        print(result.final_output)

except Exception as ae:
    print(f"Exception raise {ae}")


