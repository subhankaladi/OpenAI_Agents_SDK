from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    Runner,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    InputGuardrailTripwireTriggered
)
from dotenv import load_dotenv
import asyncio

load_dotenv()

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)

@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )

async def main():
    main_agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        input_guardrails=[math_guardrail],
    )
    try:
        result = await Runner.run(
            main_agent,
            "Solve for x: 2x + 3 = 11"  # Input that triggers the guardrail
        )
        print(result.final_output)
    except Exception as e:
        print(f"Exception raised: {type(e).__name__} - {str(e)}")

asyncio.run(main())