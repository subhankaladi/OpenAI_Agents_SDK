from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal
import os
from agents import Agent, ItemHelpers, Runner, TResponseInputItem, trace,set_tracing_disabled, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
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


@dataclass
class EvaluationFeedback:
    feedback: str
    score: Literal["pass", "needs_improvement", "fail"]


exercise_generator = Agent(
    name="story_outline_generator",
    instructions=(
        "You generate a coding exercise based on the user's topic of interest.If there is any feedback provided, use it to improve the exercise."
    ),
    model=model
)


evaluator = Agent[None](
    name="evaluator",
    instructions=(
        "You evaluate the exercise and decide if it's good enough. If it's not good enough, you provide feedback on what needs to be improved. Never give it a pass on the first try."
    ),
    output_type=EvaluationFeedback,
    model=model
)


async def main() -> None:
    msg = input("What kind of coding exercise would you like? ")
    input_items: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    latest_outline: str | None = None

    # We'll run the entire workflow in a single trace
    with trace("LLM as a judge"):
        while True:
            exercise_result = await Runner.run(
                exercise_generator,
                input_items,
            )

            input_items = exercise_result.to_input_list()
            latest_outline = ItemHelpers.text_message_outputs(exercise_result.new_items)
            print("Exercise generated")

            evaluator_result = await Runner.run(evaluator, input_items)
            result: EvaluationFeedback = evaluator_result.final_output

            print(f"Evaluator score: {result.score}")

            if result.score == "pass":
                print("Coding exercise is good enough, exiting.")
                break

            print("Re-running with feedback")

            input_items.append({"content": f"Feedback: {result.feedback}", "role": "user"})

    print(f"Final exercise: {latest_outline}")


if __name__ == "__main__":
    asyncio.run(main())