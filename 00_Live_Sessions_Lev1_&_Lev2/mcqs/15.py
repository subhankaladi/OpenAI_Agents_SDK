import asyncio
from agents import Agent, Runner, enable_verbose_stdout_logging, function_tool
from dotenv import load_dotenv
import os
from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
# enable_verbose_stdout_logging()


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)








@function_tool(name_override="custom_tool")
def fetch_data(): 
    return asyncio.sleep(2)

agent = Agent(
 name="Assistant",
 tools=[fetch_data],
 model=model,
 )

result = Runner.run_sync(
    agent,
    "fetch data "
)

print(result.final_output)