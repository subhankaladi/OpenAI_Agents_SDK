from agents import OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig,Runner, Agent
import os
from dotenv import load_dotenv



load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

agent_one = Agent(
    name="Frontend Expert",
    instructions="you are a forntend expert",
)

result = Runner.run_sync(
    agent_one,
    input="Helo how are you",
    run_config=config
)

print(result.final_output)