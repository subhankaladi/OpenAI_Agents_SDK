import asyncio
from agents import Agent, GuardrailFunctionOutput, Runner,  input_guardrail
from dotenv import load_dotenv

load_dotenv()


check_agent=Agent(
    name="Checker",
    instructions="You are a checker agent. You need to check if the user query is related to math.",
)

@input_guardrail
async def input_guardrail_function(ctx, agent, input)-> GuardrailFunctionOutput:
    result = await Runner.run(
        check_agent,
        input
    )
    return GuardrailFunctionOutput(
         output_info=result.final_output,
         tripwire_triggered=result.final_output
)

async def main():

    main_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    input_guardrails=[input_guardrail_function],
)
    
    try:
        result = await Runner.run(
            main_agent,
            "solve 2+ 5 - 6",
            )
        print(result.final_output)

    except Exception as ig:
        print(f"Exception raise: {type(ig).__name__} - {str(ig)}")


asyncio.run(main())