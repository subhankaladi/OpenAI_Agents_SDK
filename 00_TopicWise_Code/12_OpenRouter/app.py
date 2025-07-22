from agents import Agent,Runner, set_tracing_disabled, AsyncOpenAI, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("OPENROUTER_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://openrouter.ai/api/v1"
)


model = OpenAIChatCompletionsModel(
    model="deepseek/deepseek-r1",
    openai_client=client
)


# 🧠 Main Python Expert Agent
one_agent = Agent(
    name="PythonExpert",
    instructions="You are a Python expert. Only respond to Python programming questions.",
    model=model,
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
        input=message.content
    )
    await cl.Message(content=result.final_output).send()

