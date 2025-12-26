import asyncio
from agents import Agent, RunContextWrapper

agent = Agent(
    name="TestBot",
    instructions="You are a test assistant"
)

# Manual prompt get (rarely needed)
async def check_prompt():
    # Empty context 
    context = RunContextWrapper(context={})
    prompt = await agent.get_system_prompt(context)
    print(f"Agent prompt: {prompt}")

# Run 
asyncio.run(check_prompt())