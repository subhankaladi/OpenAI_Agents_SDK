from agents import Agent,Runner, set_tracing_disabled
import os
from dotenv import load_dotenv
import chainlit as cl
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

MODEL = "gemini/gemini-2.0-flash"

# 🧠 Main Python Expert Agent
one_agent = Agent(
    name="PythonExpert",
    instructions="You are a Python expert. Only respond to Python programming questions.",
    model=LitellmModel(api_key=gemini_api_key, model=MODEL),
)

# 💬 Chat Start (optional)
@cl.on_chat_start
async def start():
    await cl.Message(content="👋 I’m a Python Expert Assistant. Ask me anything about Python programming!").send()

# 💬 Message Handling
@cl.on_message
async def main(message: cl.Message):
    result = await Runner.run(
        one_agent,
        input=message.content,
    )
    await cl.Message(content=result.final_output).send()

