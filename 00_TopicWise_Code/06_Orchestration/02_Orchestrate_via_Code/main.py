from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_default_openai_api

from dotenv import load_dotenv
import os
import chainlit as cl

load_dotenv()

# ========== Setup Model ==========
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
# set_default_openai_api("chat_completions")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# ========== Updated Agents ==========

web_search_agent = Agent(
    name="WebSearchAgent",
    instructions="You perform a web search and return useful content for the given topic.",
    model=model,

)

data_analysis_agent = Agent(
    name="DataAnalysisAgent",
    instructions="You analyze topic-related information and extract key insights, regardless of the subject.",
    model=model,
)

writer_agent = Agent(
    name="WriterAgent",
    instructions="You write a formal, structured report based on provided analysis for the user's topic.",
    model=model,
)


# ========== Chainlit Chat Setup ==========
@cl.on_chat_start
async def handle_start_chat():
    cl.user_session.set("history", [])
    await cl.Message(content="📄 Manual Flow Orchestrator ready! Type a topic like: 'Climate change trends'").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    history = cl.user_session.get("history")
    


    # Step 1: Web Search
    await cl.Message(content="🔍 Step 1: Searching the web for data...").send()
    web_search_output = await Runner.run(
        web_search_agent,
        input=f"Search about: {user_input}",
        run_config=config
    )
    await cl.Message(content=f"🧾 Search Result:\n{web_search_output.final_output}").send()

    # Step 2: Data Analysis
    await cl.Message(content="📊 Step 2: Analyzing the collected data...").send()
    data_analysis_output = await Runner.run(
        data_analysis_agent,
        input=f"Analyze this: {web_search_output.final_output}",
        run_config=config
    )
    await cl.Message(content=f"📌 Analysis:\n{data_analysis_output.final_output}").send()

    # Step 3: Write Final Report
    await cl.Message(content="🖋️ Step 3: Writing final report...").send()
    final_report = await Runner.run(
        writer_agent,
        input=f"Write a formal report based on this analysis: {data_analysis_output.final_output}",
        run_config=config
    )

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": final_report.final_output})
    cl.user_session.set("history", history)

    await cl.Message(content=final_report.final_output).send()
