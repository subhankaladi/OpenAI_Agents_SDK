










# Kaiseeeeeee Lagiiiiiiiiiii Ajjjjjjjjjj Keeeeeeee Meeeeeeting





from agents import Agent, Runner, ModelSettings
from dotenv import load_dotenv


load_dotenv()



agent = Agent(
    name="assista",
    model_settings=ModelSettings(
        temperature=0.8
    ),
    model="gpt-5"
)


result = Runner.run_sync(
    agent,
    "hello"
)



