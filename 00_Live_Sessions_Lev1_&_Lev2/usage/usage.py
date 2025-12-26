
from agents import Agent, Runner, ModelSettings, RunContextWrapper, function_tool
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class User(BaseModel):
    user_id : int
    user_name : str

user_ctx = User(
    user_id=12345,
    user_name="subhan"
)

@function_tool
def main(ctx: RunContextWrapper[User]):
    print(ctx.usage) # <<<< print usage
    return f"user id :{ctx.context.user_id} and user name {ctx.context.user_name}"

agent = Agent[User](
    name="Assistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(
        include_usage=False # False
    ),
    model="gpt-3.5-turbo",
    tools=[main]
)


result = Runner.run_sync(
    agent,
    "tell me user id",
    context=user_ctx
)

print(result.final_output)

