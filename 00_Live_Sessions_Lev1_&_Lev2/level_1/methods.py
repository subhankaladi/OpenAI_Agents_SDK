import asyncio
from agents import (Agent, RunContextWrapper,Runner, enable_verbose_stdout_logging, function_tool)
from dotenv import load_dotenv
from agents import ModelSettings, Prompt, CodeInterpreterTool


load_dotenv()
# enable_verbose_stdout_logging()

# python_agent = Agent(
#     name="python_Expert",
#     instructions="you are python assistant"
# )

# python_clone = python_agent.clone(model="gpt-3.5-turbo", instructions="you are nextjs assistant." )
# python_tool = python_agent.as_tool(tool_name="python_tool", tool_description="python assistant.")



# main_agent = Agent(
#     name="triage_agent",
#     instructions="you are helpful assistant.",

# )




# Regular tools 
@function_tool(is_enabled=False)
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@function_tool  
def get_time() -> str:
    """Get current time"""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

code_interpreter = CodeInterpreterTool(
    {
        "container":{
            "type":"auto"
        },
        "type":"code_interpreter"
        
    }
)

# Agent with tools
tool_agent = Agent(
    name="ToolBot",
    instructions="I have math and time tools",
    tools=[add_numbers, get_time, code_interpreter]
)

# Check all available tools
async def check_all_tools():
    context = RunContextWrapper(context={})
    all_tools = await tool_agent.get_all_tools(context)
    
    print(f"Total tools: {len(all_tools)}")
    for tool in all_tools:
        print(f"- {tool.name}")

asyncio.run(check_all_tools())
















# result = Runner.run_sync(
#     main_agent,
#     input="hello"
# )

# print(result.final_output)



# async def get_system_prmpt():
#     context : RunContextWrapper = {}
#     get_prompt = await main_agent.get_system_prompt(context)
#     print("get prompt", get_prompt)

# asyncio.run(get_system_prmpt())