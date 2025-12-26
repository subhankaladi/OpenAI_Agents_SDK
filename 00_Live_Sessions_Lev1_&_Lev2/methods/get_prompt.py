import asyncio
from agents import Agent, RunContextWrapper


prompt_agent = Agent(
    name="PromptBot",
    prompt={
    "id": "pmpt_68a223bf2d5481978ba45a6e854f78bc0a2e94c42bb38ff1",
    "version": "4"
  }
)

async def check_structured_prompt():
    context = RunContextWrapper(context={})
    prompt_param = await prompt_agent.get_prompt(context)
    print(f"Structured prompt: {prompt_param}")

asyncio.run(check_structured_prompt())