import json
from agents import Agent, Runner, FunctionTool
from dotenv import load_dotenv

load_dotenv()
# enable_verbose_stdout_logging()

async def greet_invoke(ctx, input: str):
    """Ye function tool call par chalega"""
    args = json.loads(input) if input else {}
    name = args.get("name")
    return f"Hello, {name}!"


custom_func = FunctionTool(
    name="greeting",
    description="Greet user with their name",
    params_json_schema={
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "The name of the person"}
    },
    "required": ["name"],
    "additionalProperties": False   # ✅ Fix
},
    on_invoke_tool=greet_invoke

)

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    tools=[custom_func]
)

result = Runner.run_sync(
    main_agent,
    "my name is subhan"
)

print(result.final_output)