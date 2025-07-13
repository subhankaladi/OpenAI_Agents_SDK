from agents import Agent,set_tracing_disabled, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, trace, enable_verbose_stdout_logging
enable_verbose_stdout_logging()


set_tracing_disabled(disabled=True)
gemini_api_key = ""

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
    
)

agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=model
)
with trace("Joke workflow"):
    result = Runner.run_sync(
        agent,
        input="how are you"
    )

print(result.final_output)