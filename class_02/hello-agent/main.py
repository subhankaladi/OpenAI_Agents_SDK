import nest_asyncio
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
nest_asyncio.apply()

gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disable = True
)

agent: Agent = Agent(name="Assistant", instructions="Your are a helpful assistant", model=model)

result =  Runner.run_sync(agent, input="Hello how are you", run_config=config)

print("Calling")
print(result.final_output)