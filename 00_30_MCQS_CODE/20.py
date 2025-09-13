from agents import Agent, Runner, enable_verbose_stdout_logging, handoff
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










agent = Agent(
    name="Biiling Support Agent",
    model=model
)
handoff_obj = handoff(agent=agent, tool_name_override="trasfer_to_billig_agent")

main_agent = Agent(
    name="triage_agent",
    model=model,
    handoffs=[handoff_obj]
)

result = Runner.run_sync(
    main_agent,
    "hello"
)

print(result.final_output)