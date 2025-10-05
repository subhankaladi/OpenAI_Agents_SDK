from agents import Agent, Runner
from dotenv import load_dotenv
from agents import input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from pydantic import BaseModel

load_dotenv()

class OutputInfo(BaseModel):
    is_math_related: bool
    reasoning: str

input_guardrail_agent = Agent(
    name="Input_guardrail",
    instructions="Check if the user query is related to math. If it is, return True",
    output_type=OutputInfo
)

@input_guardrail
async def guardrail_function(ctx, agent, input)-> GuardrailFunctionOutput:
    result = await Runner.run(
        input_guardrail_agent,
        input
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output.reasoning,
        tripwire_triggered=result.final_output.is_math_related
    )

main_agent = Agent(
    name="Orchestrator",
    instructions="you are helpful assistant.",
    input_guardrails=[guardrail_function],
)

try :
    result1 = Runner.run_sync(
    starting_agent=main_agent,
    input="what is 2+2?",
)
    print(result1.final_output)

except InputGuardrailTripwireTriggered as e:
    print("Tripwire Triggered!", e)
