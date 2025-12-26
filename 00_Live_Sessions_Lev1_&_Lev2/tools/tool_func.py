import json
from agents import FunctionToolResult, ToolsToFinalOutputResult, function_tool


def get_time() -> str:
    """Get the current time"""
    from datetime import datetime
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def add_numbers(a: int, b: int) -> str:
    """Add two numbers together
    
    Args:
        a: First number
        b: Second number
    """

    result = a + b
    return f"The sum of {a} and {b} is {result}"



def my_behavior(context, tool_results: list[FunctionToolResult]) -> ToolsToFinalOutputResult:
    tool_name = tool_results[0].tool.name
    tool_output = tool_results[0].output

    if tool_name == "get_time":
        # Time wale tool ka result direct return kar do
        return ToolsToFinalOutputResult(
            is_final_output=True,
            final_output=tool_output
        )
    else:
        # Baaki sab tools ke liye LLM ko phir run karne do
        return ToolsToFinalOutputResult(
            is_final_output=False,
            final_output=None
        )


async def greet_invoke(ctx, input: str):
    """Ye function tool call par chalega"""
    args = json.loads(input) if input else {}
    name = args.get("name")
    return f"Hello, {name}!"


params_json_schema={
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "The name of the person"}
    },
    "required": ["name"],
    "additionalProperties": False   # ✅ Fix
},











@function_tool(docstring_style="numpy")
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.

    Parameters
    ----------
    a : int
        First number.
    b : int
        Second number.

    Returns
    -------
    int
        Product of numbers.
    """
    return a * b




@function_tool(docstring_style="sphinx")
def subtract(a: int, b: int) -> int:
    """
    Subtract two numbers.

    :param a: First number
    :type a: int
    :param b: Second number
    :type b: int
    :return: Difference of numbers
    :rtype: int
    """
    return a - b




@function_tool(docstring_style="google")
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: Product of numbers.
    """
    return a * b
