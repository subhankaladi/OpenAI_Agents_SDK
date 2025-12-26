from agents import Agent, Runner, function_tool, trace
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_weather(city: str):
    return f"The current weather in {city} is cloudy"

main_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[get_weather]
)

t = trace(workflow_name="kld1")
t.start(mark_as_current=True)

print("Trace started:", t.trace_id)

# --- Agent run ---
result = Runner.run_sync(main_agent, "what is current weather in hyd ?")
print("Agent output:", result.final_output)

t.finish(reset_current=True)


result2 = Runner.run_sync(
    main_agent,
    "hello"
)
print(result2.final_output)