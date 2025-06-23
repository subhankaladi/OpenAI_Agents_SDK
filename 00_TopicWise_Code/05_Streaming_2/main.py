import random
from agents import ItemHelpers, Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool, set_tracing_disabled
from dotenv import load_dotenv
import os
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent
import requests

set_tracing_disabled(disabled=True)
load_dotenv()

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


# # 🔧 Joke tool
# @function_tool
# def how_many_jokes():
#     return random.randint(1, 10)

# # 🌤️ Weather tool
# @function_tool
# def get_weather(city: str) -> str:
#     """
#     Get the current weather for a given city.
#     """
#     try:
#         result = requests.get(
#             f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
#         )
#         data = result.json()
#         return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
#     except Exception as e:
#         return f"Could not fetch weather data due to: {str(e)}"

# # 🧠 Agent definition
# web_search_agent = Agent(
#     name="WebSearchAgent",
#     instructions="Perform web searches and return relevant content for climate-related queries.",
#     model=model,
# )

# web_search_agent_as_tool = web_search_agent.as_tool(
#     tool_name="WebSearchAgent",
#     tool_description="Performs web searches for climate-related information.",
# )

# # ========== Data Analysis Agent ==========
# data_analysis_agent = Agent(
#     name="DataAnalysisAgent",
#     instructions="Analyze climate-related data and provide key insights.",
#     model=model,
# )

# data_analysis_agent_as_tool = data_analysis_agent.as_tool(
#     tool_name="DataAnalysisAgent",
#     tool_description="Analyzes climate data and provides insights.",
# )

# # ========== Writer Agent ==========
# writer_agent = Agent(
#     name="WriterAgent",
#     instructions="Write formal detailed climate reports based on provided insights.",
#     model=model,
# )

# writer_agent_as_tool = writer_agent.as_tool(
#     tool_name="WriterAgent",
#     tool_description="Writes comprehensive climate reports based on analysis."
# )

# # ========== Main Orchestrator Agent ==========
# main_agent = Agent(
#     name="Climate Orchestrator",
#     instructions="""
# You are a specialized climate report orchestrator. Strictly handle only climate-related topics:
# 1. Use 'WebSearchAgent' for climate information gathering
# 2. Send results to 'DataAnalysisAgent' for insights
# 3. Pass insights to 'WriterAgent' for final report
# Reject non-climate topics immediately.
# """,
#     model=model,
#     tools=[web_search_agent_as_tool, data_analysis_agent_as_tool, writer_agent_as_tool],
# )



# # 🔧 Joke tool
# @function_tool
# def how_many_jokes():
#     return random.randint(1, 10)

# # 🌤️ Weather tool
# @function_tool
# def get_weather(city: str) -> str:
#     """
#     Get the current weather for a given city.
#     """
#     try:
#         result = requests.get(
#             f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
#         )
#         data = result.json()
#         return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
#     except Exception as e:
#         return f"Could not fetch weather data due to: {str(e)}"

# # 🧠 Agent definition
# agent = Agent(
#     name="Subhan Kaladi",
#     instructions=(
#         "If the user asks for jokes, first call `how_many_jokes`, then tell that many jokes with numbers. "
#         "If the user asks for weather, call the `get_weather` function with the city name."
#     ),
#     model=model,
#     tools=[how_many_jokes, get_weather]
# )




backend_agent = Agent(
    name="Backend Expert",
    instructions="""
You are a backend development expert. You help users with backend topics like APIs, databases, authentication, server frameworks (e.g., Express.js, Django).

Do NOT answer frontend or UI questions.
""",

)

frontend_agent = Agent(
    name="Frontend Expert",
    instructions="""
You are a frontend expert. You help with UI/UX using HTML, CSS, JavaScript, React, Next.js, and Tailwind CSS.

Do NOT answer backend-related questions.
"""
)

web_dev_agent = Agent(
    name="Web Developer Agent",
    instructions="""
You are a generalist web developer who decides whether a question is about frontend or backend.
Your job is to analyze the user's message and then hand off the task accordingly.
""",
handoffs=[frontend_agent, backend_agent],

)


@cl.on_chat_start
async def handle_start_chat():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello from subhan kaladi").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    msg = cl.Message(content="")
    await msg.send()

    history.append({"role": "user", "content": message.content})
    result = Runner.run_streamed(
        web_dev_agent,
        input=history,
        run_config=config
    )

    print("=== Run starting ===")

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            # Streaming to frontend UI
            if isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)
            continue

        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue

        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")

    print("=== Run complete ===")

    history.append({"role": "user", "content": result.final_output})
    cl.user_session.set("history", history)
