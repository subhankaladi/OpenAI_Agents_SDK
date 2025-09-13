from agents import Agent, Runner, enable_verbose_stdout_logging, handoff
from dotenv import load_dotenv
import os
from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI, BaseModel

load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
enable_verbose_stdout_logging()

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)










    
    # class Config:
    #     extra = "forbid"  # Explicitly forbid additional properties

# Define the handoff function
# def escalate_to_billing(context, input_data: EscalationData):
#     """Function called when handing off to billing support"""
#     print(f"Escalating to billing support. Reason: {input_data.reason}")
#     return f"Escalating to billing support due to: {input_data.reason}"









billing_agent = Agent(
    name="Billing Support Agent",
    model=model,
    instructions="You are a billing support agent. Help users with billing-related questions and issues."
)

class EscalationData(BaseModel):
    reason: str


handoff_obj = handoff(
    agent=billing_agent, 
    input_type=EscalationData,
)

main_agent = Agent(
    name="triage_agent",
    model=model,
    instructions="You are a triage agent. Determine if the user needs billing support and escalate if needed.",
    handoffs=[handoff_obj]
)

result = Runner.run_sync(
    main_agent,
    "hello"
)

print(result.final_output)