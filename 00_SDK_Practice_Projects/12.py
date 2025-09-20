
from agents import Agent, Runner, RunHooks
from dotenv import load_dotenv

load_dotenv()


class CustomRunHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        print("agent start hua ha.", agent.name)


get_weather = Agent(
    name="get_weather",
    instructions="you always respond today karachi weather is cloudy."
)


main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    handoffs=[get_weather]
)

result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi",
    hooks=CustomRunHooks()
)

print(result.final_output)
