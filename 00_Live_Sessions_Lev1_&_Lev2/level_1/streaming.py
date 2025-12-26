from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()


async def main():
    main_agent = Agent(
        name="Assistant",
        instructions="you are helpfull assistant"
    )

    result = Runner.run_streamed(
        main_agent,
        "hello"
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(main())