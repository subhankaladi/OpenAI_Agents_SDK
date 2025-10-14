

from agents import Agent, Runner, enable_verbose_stdout_logging
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()


get_weather = Agent(
    name="get_weather",
    instructions="you always respond today karachi weather is cloudy."
)

subhan_kaladi_agent = Agent(
    name="Subhan Kaladi Assistant",
    instructions="You are subhan kaladi assistant. Subhan kaladi is CEO of Codentic and AI Agents Developer."
)

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    handoffs=[subhan_kaladi_agent, get_weather]
)


result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi and who is subhan kaladi?"
)

print(result.final_output)
