from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered, RunContextWrapper, TResponseInputItem, input_guardrail, output_guardrail
from dotenv import load_dotenv
import os
import chainlit as cl
from pydantic import BaseModel

load_dotenv()


# ========== Model Setup ==========
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


# ========== Guardrail Models ==========
class ClimateCheck(BaseModel):
    is_climate_related: bool
    reasoning: str



    

# ========== Input Guardrail ==========
input_guardrail_agent = Agent(
    name="InputClimateGuard",
    instructions="Check if the user request is related to climate change or environmental topics. Return true only for climate topics.",
    output_type=ClimateCheck,
    model=model
)

@input_guardrail
async def input_climate_guardrail(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    # Extract last user message
    user_input = input[-1]["content"] if isinstance(input, list) else input
    
    result = await Runner.run(input_guardrail_agent, user_input)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_climate_related
    )





# ========== Output Guardrail ==========
output_guardrail_agent = Agent(
    name="OutputClimateGuard",
    instructions="Verify if the generated content is about climate change. Return true only for climate topics.",
    output_type=ClimateCheck,
    model=model
)

@output_guardrail
async def output_climate_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: str
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_climate_related
    )


# ========== Web Search Agent ==========
web_search_agent = Agent(
    name="WebSearchAgent",
    instructions="Perform web searches and return relevant content for climate-related queries.",
    model=model,
)

web_search_agent_as_tool = web_search_agent.as_tool(
    tool_name="WebSearchAgent",
    tool_description="Performs web searches for climate-related information.",
)

# ========== Data Analysis Agent ==========
data_analysis_agent = Agent(
    name="DataAnalysisAgent",
    instructions="Analyze climate-related data and provide key insights.",
    model=model,
)

data_analysis_agent_as_tool = data_analysis_agent.as_tool(
    tool_name="DataAnalysisAgent",
    tool_description="Analyzes climate data and provides insights.",
)

# ========== Writer Agent ==========
writer_agent = Agent(
    name="WriterAgent",
    instructions="Write formal detailed climate reports based on provided insights.",
    model=model,
)

writer_agent_as_tool = writer_agent.as_tool(
    tool_name="WriterAgent",
    tool_description="Writes comprehensive climate reports based on analysis."
)

# ========== Main Orchestrator Agent ==========
main_agent = Agent(
    name="Climate Orchestrator",
    instructions="""
You are a specialized climate report orchestrator. Strictly handle only climate-related topics:
1. Use 'WebSearchAgent' for climate information gathering
2. Send results to 'DataAnalysisAgent' for insights
3. Pass insights to 'WriterAgent' for final report
Reject non-climate topics immediately.
""",
    model=model,
    tools=[web_search_agent_as_tool, data_analysis_agent_as_tool, writer_agent_as_tool],
    input_guardrails=[input_climate_guardrail],
    output_guardrails=[output_climate_guardrail]
)

# ========== Chainlit Chat Setup ==========
@cl.on_chat_start
async def handle_start_chat():
    cl.user_session.set("history", [])
    await cl.Message(content="🌍 Climate Report Orchestrator is ready! Ask about climate topics like renewable energy, carbon emissions, or climate policies.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    
    try:
        result = await Runner.run(
            main_agent,
            input=history,
            run_config=config
        )
        
        # Output guardrail will be automatically triggered during processing
        history.append({"role": "assistant", "content": result.final_output})
        await cl.Message(content=result.final_output).send()
    
    except InputGuardrailTripwireTriggered as e:
        # Use correct attribute name: guardrail_result
        reason = e.guardrail_result
        error_msg = f"❌ Input rejected: {reason}"
        history.append({"role": "assistant", "content": error_msg})
        await cl.Message(content=error_msg).send()
    
    except OutputGuardrailTripwireTriggered as e:
        reason = e.guardrail_result.output_info.reasoning
        error_msg = f"⚠️ Output blocked: {reason}"
        history.append({"role": "assistant", "content": error_msg})
        await cl.Message(content=error_msg).send()
    
    cl.user_session.set("history", history)