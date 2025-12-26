from agents import Agent, ModelSettings, Runner
from openai.types import Reasoning
from dotenv import load_dotenv
load_dotenv()


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(
        temperature=0.7
    ),
)

result = Runner.run_sync(
    agent,
    "helo"
)

print(result.final_output)
# print(agent.model_settings.to_json_dict)
print(agent.model_settings.resolve(override=ModelSettings(temperature=0.5)))
print(agent.model_settings.to_json_dict)
