
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, handoff
from agents import set_tracing_disabled, enable_verbose_stdout_logging
from dotenv import load_dotenv
import os


load_dotenv()
enable_verbose_stdout_logging()
set_tracing_disabled(True)


client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client   
)


python_agent = Agent(
    name="PythonAgent",
    instructions="You are a Python code execution agent.",
    handoff_description="Handles Python-related code execution.",
    model=model
)

triage_agent = Agent(
    name="Assistant",
    instructions="""If the user query is about Python, you MUST always call the tool transfer_to_python_agent with the code field containing the query.
    Do not answer Python queries yourself""",
    handoffs=[handoff(python_agent, tool_description_override="Handoff to the PythonAgent agent", tool_name_override="transfer_to_python_agentttt")],
    model=model
)

result = Runner.run_sync(
    triage_agent,
    "what is python response in 2 lines use transfer_to_python_agent"
    )

print(result.final_output)

