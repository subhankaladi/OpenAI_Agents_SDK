
from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
from dotenv import load_dotenv
import os
import chainlit as cl
# from agents.tool import WebSearchTool


load_dotenv()

# ========== Setup Model ==========
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# ========== Web Search Agent ==========
web_search_agent = Agent(
    name="WebSearchAgent",
    instructions="You are a tool that performs a web search and returns useful content for the query.",
    model=model,
    # tools=[WebSearchTool()]
)


web_search_agent_as_tool = web_search_agent.as_tool(
    tool_name="WebSearchAgent",
    tool_description="You are a tool that performs a web search and returns useful content for the query.",
)

# ========== Data Analysis Agent ==========
data_analysis_agent = Agent(
    name="DataAnalysisAgent",
    instructions="You are a tool that analyzes data related to the given topic and provides key insights.",
    model=model,
)


data_analysis_agent_as_tool = data_analysis_agent.as_tool(
    tool_name="DataAnalysisAgent",
    tool_description="You are a tool that analyzes climate-related data and provides key insights.",
)

# ========== Writer Agent ==========
writer_agent = Agent(
    name="WriterAgent",
    instructions="You write a formal and detailed report based on the given insights for the user's topic.",
    model=model,
)

writer_agent_as_tool = writer_agent.as_tool(
    tool_name="WriterAgent",
    tool_description="You are a tool that writes a full report based on climate analysis insights. Be formal and detailed."
)

# ========== Main Orchestrator Agent ==========
main_agent = Agent(
    name="LLM Orchestrator",
    instructions="""
You are an intelligent orchestrator agent.
1. Use 'WebSearchAgent' to gather information about the topic the user requested.
2. Send that information to 'DataAnalysisAgent' to generate insights.
3. Pass those insights to 'WriterAgent' to generate a final report.
Be sure to follow the user's topic exactly and not assume it is climate-related.
""",
    model=model,
    tools=[web_search_agent_as_tool, data_analysis_agent_as_tool, writer_agent_as_tool]
)

# ========== Chainlit Chat Setup ==========
@cl.on_chat_start
async def handle_start_chat():
    cl.user_session.set("history", [])
    await cl.Message(content="🧠 LLM Orchestrator is ready! Type your request like: 'Make a report on AI in education' or any topic of your choice.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    result = await Runner.run(
        main_agent,
        input=history,
        run_config=config
    )

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()
