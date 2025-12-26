from agents import ( Agent, Runner )
from agents import input_guardrail, GuardrailFunctionOutput, output_guardrail, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import function_tool, ModelSettings

load_dotenv()

#Input Agent Output_Type
class MathOutput(BaseModel):
    is_math_related : bool
    reasoning : str


#Input Guardrails Agent
input_check_agent = Agent(
    name="Checker",
    instructions="check if the input includes any math.",
    output_type=MathOutput
)

#Input Guardrails Function
@input_guardrail
async def input_guard_func(ctx, agent, input) -> GuardrailFunctionOutput:
    result = await Runner.run(
        input_check_agent,
        input
)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_related
)


#Output Agent Output_Type
class OutputMath(BaseModel):
     is_python_related : bool
     reasoning : str


#Output Guadrails Agent
output_guard_agent = Agent(
     name="output checker",
     instructions="check if the output includes any python.",
     output_type=OutputMath
)

#Output Guardrails Function
@output_guardrail
async def output_guard_func(ctx, agent, output)-> GuardrailFunctionOutput:
     result = await Runner.run(
          output_guard_agent,
          output
)
     return GuardrailFunctionOutput(
          output_info=result.final_output,
          tripwire_triggered=result.final_output.is_python_related
)

#Customer Support Main_Agent
triage_agent = Agent(
    name="triage_agent",
    instructions="you are helfull assistant",
    input_guardrails=[input_guard_func],
    output_guardrails=[output_guard_func],
)

try:
    result = Runner.run_sync(triage_agent, "capital of pakistan.")
    print(result.final_output)
    print("Guardrail didn't trip - this is unexpected")

except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

except OutputGuardrailTripwireTriggered:
        print("output guard tripped ")