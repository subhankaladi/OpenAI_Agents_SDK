
import json
from agents.extensions import handoff_filters

import os
from agents import Agent, Handoff, RunContextWrapper, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled, enable_verbose_stdout_logging
from dotenv import load_dotenv


load_dotenv()
# enable_verbose_stdout_logging()
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

input_schema = {
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "Python code snippet to execute"
        }
    },
    "required": ["code"],
    "additionalProperties": False
}


async def invoke_python_agent(ctx: RunContextWrapper, args: str) -> Agent:
    """
    args: JSON string containing handoff input
    """
    data = json.loads(args)  # args ko JSON me convert karte hain
    print(f"[Handoff Triggered] Code received for execution: {data.get('code')}")
    # Yahan aap Python code execute karwana chaho to kar sakte ho
    return python_agent



python_handoff = Handoff(
    tool_name="transfer_to_python_agenttt",
    tool_description="Handoff to PythonAgent for Python code execution.",
    agent_name=python_agent.name,
    input_json_schema=input_schema,
    on_invoke_handoff=invoke_python_agent,
)

agent = Agent(
    name="Assistant",
    instructions="""If the user query is about Python, you MUST always call the tool transfer_to_python_agent with the code field containing the query.
    Do not answer Python queries yourself""",
    handoffs=[python_handoff],
    model=model
)

result = Runner.run_sync(
    agent,
    "what is print(15) in python response in 2 lines"
    )

print(result.final_output)

