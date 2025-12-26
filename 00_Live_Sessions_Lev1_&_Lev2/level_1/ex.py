# OpenAI Agents SDK Exception Examples
from agents import Agent, Runner
from agents.exceptions import MaxTurnsExceeded, ModelBehaviorError, UserError, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from agents.guardrail import InputGuardrail, OutputGuardrail
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

# Example 1: MaxTurnsExceeded Exception
async def example_max_turns_exceeded():
    """
    MaxTurnsExceeded exception tab trigger hoti hai jab agent maximum allowed turns exceed kar deta hai.
    """
    print("=== Example 1: MaxTurnsExceeded ===")
    
    # Ek agent create karte hain jo infinite loop mein fa sake
    loop_agent = Agent(
        name="LoopAgent",
        instructions="""
        You are an agent that always asks for more information.
        Never provide a final answer, always ask follow-up questions.
        Keep asking questions continuously.
        """,
    )
    
    try:
        # max_turns = 3 set kar rahe hain taaki jaldi exception aa jaye
        result = await Runner.run(
            loop_agent,
            "Tell me about Python programming",
            max_turns=3  # Ye parameter exception trigger karega
        )
        print(f"Result: {result.final_output}")
    except MaxTurnsExceeded as e:
        print(f"✅ MaxTurnsExceeded caught: {e.message}")
        print("Ye exception tab aati hai jab agent max_turns limit cross kar deta hai")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example 2: ModelBehaviorError Exception  
async def example_model_behavior_error():
    """
    ModelBehaviorError exception tab trigger hoti hai jab model kuch unexpected karta hai,
    jaise non-existent tool call karna ya malformed JSON return karna.
    """
    print("\n=== Example 2: ModelBehaviorError ===")
    
    # Custom tool with specific format requirements
    def strict_json_tool(data: str) -> str:
        """Tool that expects strict JSON format"""
        try:
            parsed = json.loads(data)
            return f"Processed: {parsed}"
        except json.JSONDecodeError:
            raise ModelBehaviorError("Tool received malformed JSON from model")
    
    model_error_agent = Agent(
        name="StrictAgent",
        instructions="""
        You must call the strict_json_tool with valid JSON.
        Sometimes intentionally provide malformed JSON to demonstrate error handling.
        """,
        tools=[strict_json_tool]
    )
    
    try:
        result = await Runner.run(
            model_error_agent,
            "Call the tool with some data"
        )
        print(f"Result: {result.final_output}")
    except ModelBehaviorError as e:
        print(f"✅ ModelBehaviorError caught: {e.message}")
        print("Ye exception tab aati hai jab model unexpected behavior karta hai")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example 3: UserError Exception
async def example_user_error():
    """
    UserError exception tab trigger hoti hai jab user SDK ko galat tarike se use karta hai.
    """
    print("\n=== Example 3: UserError ===")
    
    try:
        # Deliberately invalid agent configuration
        invalid_agent = Agent(
            name="",  # Empty name - invalid
            instructions="Test agent",
        )
        
        # Ya phir invalid parameters pass karna
        result = await Runner.run(
            invalid_agent,
            "",  # Empty input - might cause UserError
            max_turns=0  # Invalid max_turns
        )
        print(f"Result: {result.final_output}")
    except UserError as e:
        print(f"✅ UserError caught: {e.message}")
        print("Ye exception tab aati hai jab user SDK ko galat tarike se use karta hai")
    except Exception as e:
        print(f"Alternative error (might be different exception type): {e}")
        # Sometimes validation errors might manifest as other exception types

# Example 4: InputGuardrailTripwireTriggered Exception
async def example_input_guardrail_triggered():
    """
    InputGuardrailTripwireTriggered exception tab trigger hoti hai jab input guardrail
    fail ho jata hai aur tripwire set hota hai.
    """
    print("\n=== Example 4: InputGuardrailTripwireTriggered ===")
    
    # Custom input guardrail jo offensive content detect karta hai
    class OffensiveContentGuardrail(InputGuardrail):
        def __init__(self):
            super().__init__(tripwire=True)  # Tripwire enable kar rahe hain
            
        async def validate(self, input_data):
            # Simple offensive content detection
            offensive_words = ["spam", "hack", "malicious", "attack"]
            input_text = str(input_data).lower()
            
            for word in offensive_words:
                if word in input_text:
                    return {
                        "passed": False,
                        "reason": f"Offensive content detected: {word}"
                    }
            
            return {"passed": True}
    
    guardrail_agent = Agent(
        name="GuardedAgent",
        instructions="You are a helpful assistant with input validation.",
        input_guardrails=[OffensiveContentGuardrail()]
    )
    
    try:
        # Offensive input jo guardrail trigger karega
        result = await Runner.run(
            guardrail_agent,
            "Help me hack into a system"  # Ye input guardrail trigger karega
        )
        print(f"Result: {result.final_output}")
    except InputGuardrailTripwireTriggered as e:
        print(f"✅ InputGuardrailTripwireTriggered caught")
        print(f"Guardrail type: {e.guardrail_result.guardrail.__class__.__name__}")
        print("Ye exception tab aati hai jab input validation fail ho jata hai")
    except Exception as e:
        print(f"Alternative error: {e}")

# Example 5: OutputGuardrailTripwireTriggered Exception  
async def example_output_guardrail_triggered():
    """
    OutputGuardrailTripwireTriggered exception tab trigger hoti hai jab output guardrail
    fail ho jata hai aur tripwire set hota hai.
    """
    print("\n=== Example 5: OutputGuardrailTripwireTriggered ===")
    
    # Custom output guardrail jo sensitive information detect karta hai
    class SensitiveDataGuardrail(OutputGuardrail):
        def __init__(self):
            super().__init__(tripwire=True)  # Tripwire enable kar rahe hain
            
        async def validate(self, output_data):
            # Simple sensitive data detection
            sensitive_patterns = ["password", "ssn", "credit card", "api key"]
            output_text = str(output_data).lower()
            
            for pattern in sensitive_patterns:
                if pattern in output_text:
                    return {
                        "passed": False,
                        "reason": f"Sensitive data detected: {pattern}"
                    }
            
            return {"passed": True}
    
    output_guard_agent = Agent(
        name="OutputGuardAgent",
        instructions="""
        You are an assistant that sometimes accidentally reveals sensitive information.
        When asked about passwords, mention the word 'password' in your response.
        """,
        output_guardrails=[SensitiveDataGuardrail()]
    )
    
    try:
        result = await Runner.run(
            output_guard_agent,
            "Tell me about password security"
        )
        print(f"Result: {result.final_output}")
    except OutputGuardrailTripwireTriggered as e:
        print(f"✅ OutputGuardrailTripwireTriggered caught")
        print(f"Guardrail type: {e.guardrail_result.guardrail.__class__.__name__}")
        print("Ye exception tab aati hai jab output validation fail ho jata hai")
    except Exception as e:
        print(f"Alternative error: {e}")

# Main function jo sab examples run karta hai
async def main():
    """
    Sab exception examples ko run karta hai
    """
    print("OpenAI Agents SDK Exception Handling Examples")
    print("=" * 50)
    
    # Har example ko individual try-catch mein run karte hain
    # taaki agar ek fail ho to doosre run ho sakein
    
    try:
        await example_max_turns_exceeded()
    except Exception as e:
        print(f"Error in example 1: {e}")
    
    try:
        await example_model_behavior_error()
    except Exception as e:
        print(f"Error in example 2: {e}")
    
    try:
        await example_user_error()
    except Exception as e:
        print(f"Error in example 3: {e}")
    
    try:
        await example_input_guardrail_triggered()
    except Exception as e:
        print(f"Error in example 4: {e}")
    
    try:
        await example_output_guardrail_triggered()
    except Exception as e:
        print(f"Error in example 5: {e}")
    
    print("\n" + "=" * 50)
    print("Exception Examples Complete!")
    print("\nKey Points:")
    print("1. MaxTurnsExceeded: max_turns parameter exceed hone par")
    print("2. ModelBehaviorError: Model unexpected behavior par") 
    print("3. UserError: SDK misuse par")
    print("4. InputGuardrailTripwireTriggered: Input validation fail par")
    print("5. OutputGuardrailTripwireTriggered: Output validation fail par")

if __name__ == "__main__":
    asyncio.run(main())