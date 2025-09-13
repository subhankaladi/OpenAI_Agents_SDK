from agents import Agent, GuardrailFunctionOutput, Runner, output_guardrail
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







@output_guardrail
async def content_filter(ctx, agent, output):
 # filter logic
    return GuardrailFunctionOutput(...)


agent = Agent(
    name="Assistant",
    model=model
)


result = Runner.run_sync(
    agent,
    "what is current weather in karachi "
)

print(result.final_output)