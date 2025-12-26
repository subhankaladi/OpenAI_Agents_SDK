from agents import Agent, Runner, function_tool, MaxTurnsExceeded, AgentsException, set_tracing_disabled
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os

# from agents import enable_verbose_stdout_logging

# enable_verbose_stdout_logging()
load_dotenv()


set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

@function_tool
def get_weather(city:str):
    """get the weather for given city"""

    return f"the current weather in {city} is cloudy"

main_agent = Agent(
    name="Assistant",
    instructions="you are a helpfull assistant",
    tools=[get_weather],
    model=model
)

try :
    result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi?",
    max_turns=1
)
    print(result.final_output)

except MaxTurnsExceeded as max:
    print(f"max turns exception is raise {max}")








# from agents import Agent, Runner, function_tool, ModelSettings, enable_verbose_stdout_logging
# from dotenv import load_dotenv
# from agents import OpenAIChatCompletionsModel
# from openai import AsyncOpenAI


# load_dotenv()
# enable_verbose_stdout_logging()

# set_tracing_disabled(disabled=True)

# gemini_api_key = os.getenv("GEMINI_API_KEY")


# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider
# )


# @function_tool
# def get_weather(city:str):
#     """get weather for given city"""

#     return f"the current weather in {city} is cloudy"


# main_agent = Agent(
#     name="Assistant",
#     instructions="you are helpfull assistant",
#     tools=[get_weather],
#     model_settings=ModelSettings(
#         tool_choice="get_math"
#     ),
    # model=model

# )


# try :
#     result = Runner.run_sync(
#     main_agent,
#     "what is current weather in karachi ?",
# )
#     print(result.final_output)

# except Exception as ae:
#     print(f"Exception raised: {type(ae).__name__} - {str(ae)}")








# from agents import Agent, Runner, UserError
# from dotenv import load_dotenv
# from agents import OpenAIChatCompletionsModel
# from openai import AsyncOpenAI


# load_dotenv()


# set_tracing_disabled(disabled=True)

# gemini_api_key = os.getenv("GEMINI_API_KEY")


# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider
# )

# main_agent = Agent(
#     name="Assistant",
#     instructions="you are a helpfull assistant",
#     model="groq/llama3-8b-8192",
    # model=model

# )

# try :
#     result = Runner.run_sync(
#     main_agent,
#     "hello",
# )
#     print(result.final_output)

# except Exception as UE:
#     print(f"Exception raised {type(UE).__name__} - {UE}")





# from agents import OpenAIChatCompletionsModel
# from openai import AsyncOpenAI

# from pydantic import BaseModel
# from agents import (
#     Agent,
#     GuardrailFunctionOutput,
#     Runner,
#     input_guardrail,
#     RunContextWrapper,
#     TResponseInputItem,
#     InputGuardrailTripwireTriggered
# )
# from dotenv import load_dotenv
# import asyncio

# load_dotenv()

# set_tracing_disabled(disabled=True)

# gemini_api_key = os.getenv("GEMINI_API_KEY")


# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider
# )

# class MathHomeworkOutput(BaseModel):
#     is_math_homework: bool
#     reasoning: str

# guardrail_agent = Agent(
#     name="Guardrail check",
#     instructions="Check if the user is asking you to do their math homework.",
#     output_type=MathHomeworkOutput,
    # model=model

# )

# @input_guardrail
# async def math_guardrail(
#     ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     result = await Runner.run(guardrail_agent, input, context=ctx.context)
#     return GuardrailFunctionOutput(
#         output_info=result.final_output,
#         tripwire_triggered=result.final_output.is_math_homework,
#     )

# async def main():
#     main_agent = Agent(
#         name="Assistant",
#         instructions="You are a helpful assistant.",
#         input_guardrails=[math_guardrail],
    # model=model

#     )
#     try:
#         result = await Runner.run(
#             main_agent,
#             "Solve for x: 2x + 3 = 11"  # Input that triggers the guardrail
#         )
#         print(result.final_output)
#     except InputGuardrailTripwireTriggered as e:
#         print(f"Exception raised: {str(e)}")

# asyncio.run(main())




# from agents import OpenAIChatCompletionsModel
# from openai import AsyncOpenAI

# from pydantic import BaseModel
# from agents import (
#     Agent,
#     GuardrailFunctionOutput,
#     OutputGuardrailTripwireTriggered,
#     Runner,
#     output_guardrail,
#     RunContextWrapper
# )
# from dotenv import load_dotenv
# import asyncio

# load_dotenv()
# set_tracing_disabled(disabled=True)

# gemini_api_key = os.getenv("GEMINI_API_KEY")


# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider
# )

# class MessageOutput(BaseModel):
#     response: str

# class MathOutput(BaseModel):
#     reasoning: str
#     is_math: bool

# guardrail_agent = Agent(
#     name="Guardrail check",
#     instructions="Check if the output includes any math.",
#     output_type=MathOutput,
    # model=model

# )

# @output_guardrail
# async def math_guardrail(
#     ctx: RunContextWrapper, agent: Agent, output: MessageOutput
# ) -> GuardrailFunctionOutput:
#     result = await Runner.run(guardrail_agent, output.response, context=ctx.context)
#     return GuardrailFunctionOutput(
#         output_info=result.final_output,
#         tripwire_triggered=result.final_output.is_math,
#     )

# async def main():
#     main_agent = Agent(
#         name="Assistant",
#         instructions="You are a helpful assistant. Solve the equation in your response.",
#         output_guardrails=[math_guardrail],
#         output_type=MessageOutput,
    # model=model

#     )
#     try:
#         result = await Runner.run(
#             main_agent,
#             "What is 2 + 2?"  # Input leading to math in output
#         )
#         print(result.final_output)
#     except OutputGuardrailTripwireTriggered as e:
#         print(f"Exception raised: - {str(e)}")

# asyncio.run(main())