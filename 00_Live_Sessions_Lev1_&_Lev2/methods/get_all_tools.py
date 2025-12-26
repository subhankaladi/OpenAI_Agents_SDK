import asyncio
from agents import Agent, RunContextWrapper, function_tool

# Regular tools 
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@function_tool  
def get_time() -> str:
    """Get current time"""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

# Agent with tools
tool_agent = Agent(
    name="ToolBot",
    instructions="I have math and time tools",
    tools=[add_numbers, get_time]
)

# Check all available tools
async def check_all_tools():
    context = RunContextWrapper(context={})
    all_tools = await tool_agent.get_all_tools(context)
    
    print(f"Total tools: {len(all_tools)}")
    for tool in all_tools:
        print(f"- {tool.name}")

asyncio.run(check_all_tools())