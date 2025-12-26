import json
from agents import Agent, Runner, ModelBehaviorError, SQLiteSession, UserError
from dotenv import load_dotenv
import asyncio

load_dotenv()


async def main():
    main_agent = Agent(
        name="",
        instructions="You are a helpful assistant.",
    )

    
    session = SQLiteSession("conversation_12345")
    list_input = [ {"role": "user", "content": "Hello"} ]

    try:
        result = await Runner.run(
            main_agent,
            list_input,
            session=session
        )
        print(f"Result: {result.final_output}")
    except UserError as e:
        print(f"✅ UserError caught: {e.message}")
        print(f"Error type: {type(e).__name__}")
        


asyncio.run(main())

