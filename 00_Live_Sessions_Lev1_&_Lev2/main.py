
from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

main_agent = Agent(
    name="Assistant",
    instructions="you are helpful assistant.",
)

result = Runner.run_sync(
    main_agent,
    "hello",
)

print(result.final_output)

# 
class User:
    def __init__(self, name, instructions):
        self.name = name 