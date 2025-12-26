from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    Runner,
    output_guardrail,
    RunContextWrapper,
)
from dotenv import load_dotenv
import asyncio

load_dotenv()

class MessageOutput(BaseModel):
    response: str

class MathOutput(BaseModel):
    reasoning: str
    is_math: bool

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)

@output_guardrail
async def math_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )

async def main():
    main_agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Solve the equation in your response.",
        output_guardrails=[math_guardrail],
        output_type=MessageOutput,
    )
    try:
        result = await Runner.run(
            main_agent,
            "What is 2 + 2?"  # Input leading to math in output
        )
        print(result.final_output)
    except Exception as e:
        print(f"Exception raised: {type(e).__name__} - {str(e)}")

asyncio.run(main())