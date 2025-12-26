import json
from agents import Agent, RunContextWrapper



python_agent = Agent(
    name="PythonAgent",
    instructions="You are a Python code execution agent.",
    handoff_description="Handles Python-related code execution.",
)



async def invoke_python_agent(ctx: RunContextWrapper, args: str) -> Agent:
    """
    args: JSON string containing handoff input
    """
    data = json.loads(args)  # args ko JSON me convert karte hain
    print(f"[Handoff Triggered] Code received for execution: {data.get('code')}")
    # Yahan aap Python code execute karwana chaho to kar sakte ho
    return python_agent