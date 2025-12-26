import asyncio
from dataclasses import dataclass
from typing import Dict, Optional
from agents import Agent, RunContextWrapper, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BankingContext:
    # Bank account data - normally ye database se aaye ga
    account_balances: Dict[str, float]
    account_holders: Dict[str, str]
    current_user_account: Optional[str] = None
    bank_name: str = "ABC Bank"
    
    def verify_account(self, account_number: str) -> bool:
        """Check if account number exists"""
        return account_number in self.account_balances
    
    def get_balance(self, account_number: str) -> Optional[float]:
        """Get balance for specific account"""
        return self.account_balances.get(account_number)
    
    def get_account_holder(self, account_number: str) -> Optional[str]:
        """Get account holder name"""
        return self.account_holders.get(account_number)

@function_tool
async def check_bank_balance(wrapper: RunContextWrapper[BankingContext]) -> str:
    """Check bank balance for the user's account. User must provide their account number first."""
    
    if not wrapper.context.current_user_account:
        return "Please provide your account number first so I can check your balance."
    
    account_num = wrapper.context.current_user_account
    balance = wrapper.context.get_balance(account_num)
    holder_name = wrapper.context.get_account_holder(account_num)
    
    if balance is not None:
        return f"Account Holder: {holder_name}\nAccount Number: {account_num}\nCurrent Balance: PKR {balance:,.2f}"
    else:
        return "Account not found in our records."


@function_tool  
async def verify_account_number(wrapper: RunContextWrapper[BankingContext], account_number: str) -> str:
    """Verify and set user's account number. Call this when user provides their account number."""
    
    if wrapper.context.verify_account(account_number):
        wrapper.context.current_user_account = account_number
        holder_name = wrapper.context.get_account_holder(account_number)
        return f"Account verified successfully for {holder_name}. You can now check your balance."
    else:
        return f"Account number {account_number} not found. Please check your account number."

@function_tool
async def get_bank_services(wrapper: RunContextWrapper[BankingContext]) -> str:
    """Get available banking services information."""
    return f"""Available services at {wrapper.context.bank_name}:
    
1. Balance Inquiry - Check your current account balance
2. Account Verification - Verify your account details
3. Customer Support - Get help with banking queries

To check your balance, please provide your account number first."""

async def main():
    # Sample banking data - normally ye database se aaye ga
    banking_context = BankingContext(
        account_balances={
            "ACC001234": 125000.50,
            "ACC005678": 89750.25,
            "ACC009876": 450000.00,
            "ACC112233": 25600.75
        },
        account_holders={
            "ACC001234": "Muhammad Ali",
            "ACC005678": "Fatima Khan", 
            "ACC009876": "Ahmed Hassan",
            "ACC112233": "Sara Ahmed"
        },
        bank_name="Standard Bank Pakistan"
    )
    
    agent = Agent[BankingContext](
        name="Banking Assistant",
        instructions="""You are a helpful banking assistant. You can help users:
        
1. Verify their account numbers
2. Check their bank balance (after account verification)
3. Provide information about banking services

Always ask for the account number before checking balance. Be polite and professional.""",
        tools=[verify_account_number, check_bank_balance, get_bank_services],
    )
    
    print("=== Banking Assistant Started ===")
    print("Ask me to check your balance or ask about banking services!")
    print("Sample account numbers: ACC001234, ACC005678, ACC009876, ACC112233")
    print()
    
    # Test different scenarios
    test_inputs = [
        "What services do you provide?",
        "I want to check my balance. My account number is ACC001234",
        "What's my current balance?",
        "Can you verify account ACC999999?",
        "Check balance for account ACC005678"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n--- Test {i} ---")
        print(f"User: {user_input}")
        
        result = await Runner.run(
            starting_agent=agent,
            input=user_input,
            context=banking_context,
        )
        
        print(f"Assistant: {result.final_output}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())