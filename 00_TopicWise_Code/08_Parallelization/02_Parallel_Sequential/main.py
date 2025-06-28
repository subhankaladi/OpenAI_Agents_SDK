import asyncio
import os
from dotenv import load_dotenv
import Parallel_Candidates as cl

from agents import Agent, ItemHelpers, Runner, trace, set_tracing_disabled, AsyncOpenAI, OpenAIChatCompletionsModel

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# === Define Agents for Multi-step Flow ===

code_summarizer = Agent(
    name="code_summarizer",
    instructions="You are a code summarizer. Read the given code and write a short summary explaining what it does in simple English.",
    model=model
)

translator_agent = Agent(
    name="translator_agent",
    instructions="You are a translator. Translate the given English summary into simple Urdu.",
    model=model
)

report_generator = Agent(
    name="report_generator",
    instructions="You are a report writer. Format the translated summary into a professional short report.",
    model=model
)

# === Chainlit Entry Point ===
@cl.on_message
async def on_message(message: cl.Message):
    code_snippet = message.content  # User input from Chainlit UI

    await cl.Message(content="⏳ Step 1: Summarizing code...").send()

    with trace("Multi-Step Agent Flow"):
        # Step 1: Summarize
        summary_result = await Runner.run(code_summarizer, code_snippet)
        summary_text = ItemHelpers.text_message_outputs(summary_result.new_items)
        await cl.Message(content=f"📝 **Code Summary:**\n\n{summary_text}").send()

        # Step 2: Translate
        await cl.Message(content="🌐 Step 2: Translating summary to Urdu...").send()
        translation_result = await Runner.run(translator_agent, summary_text)
        translated_text = ItemHelpers.text_message_outputs(translation_result.new_items)
        await cl.Message(content=f"🌍 **Urdu Translation:**\n\n{translated_text}").send()

        # Step 3: Final Report
        await cl.Message(content="🗂️ Step 3: Generating final report...").send()
        report_result = await Runner.run(report_generator, translated_text)
        final_report = ItemHelpers.text_message_outputs(report_result.new_items)

    await cl.Message(content=f"✅ **Final Report:**\n\n{final_report}").send()
