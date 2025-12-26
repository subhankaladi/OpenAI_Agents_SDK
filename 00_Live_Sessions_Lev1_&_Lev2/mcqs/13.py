from agents import Agent, Runner, RunConfig
from dotenv import load_dotenv
# from agents import set_tracing_disabled
import asyncio

load_dotenv()
# set_tracing_disabled(True)

main_agent = Agent(
    name="Assistant",
    instructions="you are python asssitant",
)

sec_agent = Agent(
    name="nextjs_assistant",
    instructions="you are nextjs assistant."
)

config = RunConfig(
    tracing_disabled=True
)

async def main():
    # Trace disabled only this workflow
    result_one = await Runner.run(
        main_agent,
        "hello",
        run_config=config
    )
    print(f"result_one {result_one.final_output}")

    # No tracing disabled
    result_two = await Runner.run(
        sec_agent,
        "hello, how are you"
    )
    print(f"result_two {result_two.final_output}")


asyncio.run(main())