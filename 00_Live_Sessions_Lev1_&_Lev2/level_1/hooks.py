from agents import ( Agent, Runner, function_tool )
from dotenv import load_dotenv

load_dotenv()

class AgentHooks():
    async def on_start(ctx, agent):
        print("On Agent Start")

    async def on_end(ctx, agent, output):
        print("On Agent End")

    async def on_handoff(ctx, agent, source):
        print("handoff ho gya")

    async def on_tool_start(ctx, agent, tool):
        print("Tool calling")

    async def on_tool_end(ctx, agent, tool, result):
        print("tool end ho gya")



class RunHooks():
    async def on_agent_start(ctx, agent):
        print("Run: agent start ho chuka ha")

    async def on_agent_end(ctx, agent, output):
        print("Run: agent ka output a gya")

    async def on_tool_start(ctx, agent, tool):
        print("Run: tool calling")

    async def on_tool_end(ctx, agent, tool, result):
        print("Run: tool end ho gya")

    async def on_handoff(context, from_agent, to_agent):
        print("Run: Handoff ho gya")

    


weather_agent = Agent(
    name="weather_agent",
    instructions="Today's karachi weather is cloudy with 30C",
)

# @function_tool
# def weather(city:str):
#     return f"today {city} weather is cloudy"


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    # hooks=AgentHooks,
    handoffs=[weather_agent]
)

result = Runner.run_sync(
    agent,
    input="what is current weather in karachi",
    hooks=RunHooks
)

print(result.final_output)