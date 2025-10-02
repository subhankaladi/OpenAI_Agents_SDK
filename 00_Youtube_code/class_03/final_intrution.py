from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, enable_verbose_stdout_logging
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os

load_dotenv()
enable_verbose_stdout_logging()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=GEMINI_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash"
)


@dataclass
class BankContext:
    accounts_data: dict = None  # Sirf database chahiye

# Local data banao
accounts_database = {
    "12345": {"name": "Subhan Kaladi", "balance": 50000},
    "67890": {"name": "Shahid Ali", "balance": 75000},
    "11111": {"name": "Jawad Hassan", "balance": 25000}
}

account_no = input("Enter your account number! ")


async def prompt(wrapper: RunContextWrapper[BankContext], agent) -> str:
    """Check account balance for given account number"""
    
    ctx = wrapper.context

    account_number = account_no
    
    # Get balance from local dictionary
    account_info = ctx.accounts_data.get(account_number)
    
    if account_info:
        return f"Your name is {account_info['name']}, your balance is PKR {account_info['balance']:,}"
    else:
        return f"Account number {account_number} not found"
    

bank_context = BankContext(
    accounts_data=accounts_database
)


main_agent = Agent(
    name="Orchestrator",
    instructions=prompt,
    model=model
)


result = Runner.run_sync(
    starting_agent=main_agent,
    input="what is my account balance.",
    context=bank_context
)

print(result.final_output)