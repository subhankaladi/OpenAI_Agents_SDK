from agents import Agent, Runner, FileSearchTool
from dotenv import load_dotenv
from dotenv import load_dotenv

load_dotenv()


agent = Agent(
    name="Assistant",
    instructions="you are helpful assistant.",
    tools=[FileSearchTool()]
)

result = Runner.run_sync(
    agent,
    "who is subhan kaladi"
)

print(result.final_output)