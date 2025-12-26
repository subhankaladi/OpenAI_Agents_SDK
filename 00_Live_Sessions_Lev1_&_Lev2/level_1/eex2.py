from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    main_agent = Agent(
        name="Assistant",
        instructions="You are helpful assistant",
        model="groq/llama3-8b-8192"  # Use non-OpenAI
    )
    try:
        result = await Runner.run(
            main_agent,
            "hello"
        )
        print(result.final_output)
    except Exception as e:
        print(f"Exception raised: {type(e).__name__} - {str(e)}")

asyncio.run(main())