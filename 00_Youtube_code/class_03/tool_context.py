from dataclasses import dataclass
from agents import ( Agent, RunContextWrapper, Runner, function_tool )
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BankContext:
    accounts_data: dict = None  # Sirf database chahiye

# Local data banao
accounts_database = {
    "12345": {"name": "Subhan Kaladi", "balance": 50000},
    "67890": {"name": "Shahid Ali", "balance": 75000},
    "11111": {"name": "Jawad Hassan", "balance": 25000}
}

@function_tool
async def check_balance(wrapper: RunContextWrapper[BankContext], account_number: str) -> str:
    """Check account balance for given account number"""
    
    ctx = wrapper.context
    
    # Get balance from local dictionary
    account_info = ctx.accounts_data.get(account_number)
    
    if account_info:
        return f"{account_info['name']}, your balance is PKR {account_info['balance']:,}"
    else:
        return f"Account number {account_number} not found"

agent = Agent(
    name="Bank Assistant",
    instructions="You are a helpful bank assistant. When user asks for balance, use the check_balance tool with their account number.",
    tools=[check_balance]
)

bank_context = BankContext(
    accounts_data=accounts_database
)

result = Runner.run_sync(
    starting_agent=agent,
    input="my acc no is 12345 and please check my balance.",
    context=bank_context
)

print(result.final_output)