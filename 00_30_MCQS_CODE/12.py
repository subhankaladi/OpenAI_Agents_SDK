from agents import Agent, Runner, RunConfig
from dotenv import load_dotenv
# from agents import set_tracing_disabled
import asyncio
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
# set_tracing_disabled(True)


async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())