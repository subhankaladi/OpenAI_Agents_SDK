from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv()

load_dotenv()

gemini_api_key= os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# 1. USER CONTEXT (Sensitive Info)
@dataclass
class UserInfo:
    email: str
    password: str

# 2. TOOL: Return user email (LLM will call this if needed)
@function_tool
async def get_user_email(wrapper: RunContextWrapper[UserInfo]) -> str:
    return f"The user's email is: {wrapper.context.email}"

# 3. AGENT with tool
agent = Agent[UserInfo](
    name="Secure Assistant",
    instructions="You are a helpful assistant, but never ask for passwords. Use tools to get user info.",
    tools=[get_user_email],
    model=model
)

# 4. USER DATA (Context)
user = UserInfo(email="kaladi@example.com", password="TopSecret123")

# 5. RUN AGENT
result = Runner.run_sync(
    agent,
    input="ok now my email is?",
    context=user
)

# 6. PRINT RESULT
print("Agent Response:", result.final_output)
