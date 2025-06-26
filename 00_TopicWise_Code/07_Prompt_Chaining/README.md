
# 🧠 Notes on Multi-Agent Prompt Chaining System

## 🎯 Goal of the Project:
Build an AI Tutor system using **OpenAI Agents SDK** that:

1. Takes a learning goal from the user (e.g., _“I want to learn Python”_)
2. **Agent 1**: Generates a curriculum outline
3. **Agent 2**: Validates the curriculum for quality and goal alignment
4. **Agent 3**: Writes full lessons based on the curriculum

---

## 🧠 Prompt Chaining Concept

Each step’s output is passed as input to the next agent.  
This is called **Prompt Chaining**.

```
User Input → Agent 1 → Output A
                ↓
            Agent 2 → Validates A
                ↓ (if valid)
            Agent 3 → Uses A to create full lessons
```

---

## 🧪 Behavior of Agent 2

Agent 2 gave:
```json
good_quality: True  
matches_goal: True
```

> ❗Even though the input was “eyeglasses,” the LLM still considered the curriculum logically structured and aligned with a learning goal.

⚠️ **Note:** LLMs can sometimes be **confidently wrong**.

---

## ⚙️ Agents Overview

### 🔹 Agent 1: `curriculum_agent`
- **Task**: Generate a step-by-step curriculum
- **Input**: User’s learning goal
- **Output**: Curriculum as logically ordered text topics

---

### 🔹 Agent 2: `curriculum_checker_agent`
- **Task**: Validate the curriculum for quality and relevance
- **Input**: Curriculum (from Agent 1)  
- **Note**: Does *not* directly receive the user’s goal

Relies on LLM inference and returns:

```json
{
  good_quality: true/false,
  matches_goal: true/false
}
```

---

### 🔹 Agent 3: `lesson_writer_agent`
- **Task**: Generate full lessons from the curriculum
- **Input**: Final curriculum output from Agent 1
- **Code**:

```python
# Step 3: Generate Lessons
lessons_result = await Runner.run(
    lesson_writer_agent,
    curriculum_result.final_output,
)
```

**Instructions for Agent 3**:

> Given a structured curriculum outline, write a detailed coding lesson for each section.  
> For each section:
> - Provide a short explanation  
> - Include 1–2 code examples  
> - Add one small practice question

---

## 🧐 What went wrong?

- You entered: `"what is eyeglasses"`
- Agent 3 was expecting a **coding** curriculum
- But it received a **non-coding topic**

### 🤖 What did the LLM do?
- Read the instruction: _“Write a detailed coding lesson”_
- Got input: Curriculum about **eyeglasses**
- LLM got confused and politely clarified:

> _“I interpreted your initial request as wanting a curriculum outline about coding...”_

---

## 💥 Final Insight

- **Agent 2 mistakenly validated** a non-coding topic
- **Agent 3** was built to generate **coding** lessons
- When input didn’t match, Agent 3 tried to **auto-correct** and responded accordingly

---  
