import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, trace, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
from dotenv import load_dotenv
load_dotenv()
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)
# --------------------------

# Agent 1: Generate Curriculum
# --------------------------
curriculum_agent = Agent(
    name="curriculum_agent",
    instructions="Generate a structured curriculum outline to help someone achieve the programming learning goal they provide.",
    model=model
)

# --------------------------
# Output Schema for Agent 2
# --------------------------
class CurriculumCheckOutput(BaseModel):
    good_quality: bool
    matches_goal: bool

# --------------------------
# Agent 2: Check Curriculum (quality + match)
# --------------------------
curriculum_checker_agent = Agent(
    name="curriculum_checker_agent",
    instructions="""
You are given two things:
1. A learning goal (what the user wants to learn)
2. A curriculum outline (generated to achieve that goal)

Your job is to evaluate:
- Is the curriculum of good quality? (clear, complete, logical structure)
- Does it match the user’s learning goal?

Return your answer as two booleans:
- good_quality: true or false
- matches_goal: true or false
""",
    output_type=CurriculumCheckOutput,
        model=model

)

# --------------------------
# Agent 3: Generate Full Lessons
# --------------------------
lesson_writer_agent = Agent(
    name="lesson_writer_agent",
    instructions="""
Given a structured curriculum outline, write a detailed coding lesson for each section.

For each section:
- Provide a short explanation
- Include 1-2 code examples
- Add one small practice question
""",
    output_type=str,
        model=model

)


# --------------------------
# Main Flow
# --------------------------
async def main():
    learning_goal = input("What do you want to learn? ")

    # Step 1: Generate Curriculum
    curriculum_result = await Runner.run(
        curriculum_agent,
        learning_goal,
    )
    print("\n✅ Curriculum Generated.")

    # Step 2: Check Curriculum with both goal and curriculum
    check_result = await Runner.run(
        curriculum_checker_agent,
        curriculum_result.final_output
    )

    assert isinstance(check_result.final_output, CurriculumCheckOutput)

    if not check_result.final_output.good_quality:
        print("❌ Curriculum is low quality. Stopping.")
        return

    if not check_result.final_output.matches_goal:
        print("❌ Curriculum does not match the learning goal. Stopping.")
        return

    print("✅ Curriculum looks good. Proceeding to generate lessons...")

    # Step 3: Generate Lessons
    lessons_result = await Runner.run(
        lesson_writer_agent,
        curriculum_result.final_output,
    )
    print(f"\n📘 Generated Lessons:\n\n{lessons_result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())