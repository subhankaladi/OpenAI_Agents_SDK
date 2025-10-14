from agents import Agent, Runner, handoff
from dotenv import load_dotenv

load_dotenv()

get_weather = Agent(
    name="get_weather",
    instructions="You must always respond: 'Today the weather is cloudy."
)

def invoking(ctx):
    print("handoff ho gya")


handoff_weather_obj = handoff(
    agent=get_weather,
    on_handoff=invoking
)

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    handoffs=[handoff_weather_obj]
)

result = Runner.run_sync(
    main_agent,
    "what is current weather?",
)

print(result.final_output)
