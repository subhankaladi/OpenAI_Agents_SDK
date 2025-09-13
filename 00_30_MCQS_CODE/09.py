from agents import Agent, GuardrailFunctionOutput, ModelSettings, Runner, enable_verbose_stdout_logging, function_tool, handoff, input_guardrail
from dotenv import load_dotenv
import os
from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
enable_verbose_stdout_logging()


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)








@input_guardrail
async def check_homework(ctx, agent, input_data):
 # guardrail logic
    return GuardrailFunctionOutput(
        output_info="Helo",
        tripwire_triggered=False
    )

agent = Agent(
    name="Weather Agent",
    model=model,
)

result = Runner.run_sync(
    agent,
    "hello"
)

print(result.final_output)