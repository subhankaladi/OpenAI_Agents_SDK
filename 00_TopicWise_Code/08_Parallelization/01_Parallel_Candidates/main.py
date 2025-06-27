import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, ItemHelpers, Runner, trace, set_tracing_disabled, AsyncOpenAI, OpenAIChatCompletionsModel

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# === Define 3 unique agents ===
coding_explainer_1 = Agent(
    name="coding_explainer_1",
    instructions="You are a coding tutor. Explain the code snippet in a beginner-friendly way.",
    model=model
)

coding_explainer_2 = Agent(
    name="coding_explainer_2",
    instructions="You are a patient coding mentor. Provide a very simple explanation of this code.",
    model=model
)

coding_explainer_3 = Agent(
    name="coding_explainer_3",
    instructions="You are a programming teacher for kids. Explain the code like you're teaching a child.",
    model=model
)

# Agent to pick the best explanation
explanation_picker = Agent(
    name="explanation_picker",
    instructions="From the given explanations, pick the most technically correct and beginner-friendly one.",
    model=model
)

# === Chainlit UI Entry Point ===
@cl.on_message
async def on_message(message: cl.Message):
    code_snippet = message.content  # User input from Chainlit UI

    await cl.Message(content="⏳ Generating 3 parallel explanations...").send()

    with trace("Parallel Explanation Generation"):
        # Parallel run of 3 independent agents
        result_1, result_2, result_3 = await asyncio.gather(
            Runner.run(coding_explainer_1, code_snippet),
            Runner.run(coding_explainer_2, code_snippet),
            Runner.run(coding_explainer_3, code_snippet)
        )

        # Format their outputs
        explanations = [
            ItemHelpers.text_message_outputs(result_1.new_items),
            ItemHelpers.text_message_outputs(result_2.new_items),
            ItemHelpers.text_message_outputs(result_3.new_items),
        ]

        all_explanations = "\n\n".join(explanations)

        await cl.Message(content=f"📚 **3 Candidate Explanations:**\n\n{all_explanations}").send()

        # Let explanation_picker choose the best one
        best_explanation = await Runner.run(
            explanation_picker,
            f"Code:\n{code_snippet}\n\nExplanations:\n{all_explanations}"
        )

    # Show the final best explanation
    await cl.Message(content=f"✅ **Best Explanation:**\n\n{best_explanation.final_output}").send()
