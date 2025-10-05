from agents import Agent, Runner
from dotenv import load_dotenv
from agents import output_guardrail, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered
from pydantic import BaseModel

load_dotenv()

class OutputInfo(BaseModel):
    is_math_related:bool
    reasoning:str

output_guardrail_agent = Agent(
    name="output_guard_agent",
    instructions="check if the model response about math than you will return True",
    output_type=OutputInfo
)

@output_guardrail
async def output_guardrail_func(ctx, agent, output):

    result = await Runner.run(output_guardrail_agent, output)
    return GuardrailFunctionOutput(
        output_info=result.final_output.reasoning,
        tripwire_triggered=result.final_output.is_math_related
    )

main_agent = Agent(
    name="Orchestrator",
    instructions="you are helpful assistant.",
    output_guardrails=[output_guardrail_func]
)

try :
    result1 = Runner.run_sync(
    starting_agent=main_agent,
    input="what is 2+2?",
)
    print(result1.final_output)

except OutputGuardrailTripwireTriggered as e:
    print(f"Error occurred: {e}")

