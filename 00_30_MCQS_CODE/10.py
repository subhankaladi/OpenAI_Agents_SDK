from agents import Agent, Runner, RunConfig
from dotenv import load_dotenv
# from agents import set_tracing_disabled
import asyncio

load_dotenv()
# set_tracing_disabled(True)

python_agent = Agent(
    name="python_assistant",
    instructions="you are python asssitant",
)

nextjs_agent = Agent(
    name="nextjs_assistant",
    instructions="you are nextjs assistant.",
    handoffs=[python_agent]
)

config = RunConfig(
    model="gpt-3.5-turbo"
)

async def main():
    # Trace disabled only this workflow
    result = await Runner.run(
        nextjs_agent,
        "hello",
        run_config=config
    )
    print(f"result {result.final_output}")

asyncio.run(main())