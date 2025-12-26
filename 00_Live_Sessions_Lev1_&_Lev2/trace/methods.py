
from agents import Agent, Runner, function_tool, trace
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_weather(city: str):
    """get weather for given city"""
    return f"The current weather in {city} is cloudy"

# Agent banate hain
main_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[get_weather]
)

# Trace manually banate hain (context manager ke bagair)
trace = trace(workflow_name="kld")

# 1️⃣ Start the trace manually
trace.start(mark_as_current=True)
print("Trace started:", trace.trace_id)

try:
    # Agent ko run karte hain
    result = Runner.run_sync(main_agent, "what is current weather in hyd ?")
    print("Agent output:", result.final_output)

finally:
    # 2️⃣ Trace ko finish karte hain
    trace.finish(reset_current=True)
    print("Trace finished:", trace.trace_id)

    # 3️⃣ Export the trace data (dict form)
    exported = trace.export()
    print("Exported trace data:", exported)
