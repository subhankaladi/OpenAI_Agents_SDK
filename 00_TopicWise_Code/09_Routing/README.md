# 🤖 Web Dev Assistant with Routing via OpenAI Agent SDK

This project is a web-based AI assistant that intelligently routes user questions to the appropriate domain expert using the **OpenAI Agents SDK** and **Anthropic-style design patterns** (handoff routing).

---

## 🚀 Features

- 💡 Detects whether a question is about **frontend** or **backend**.
- 🧠 Uses multiple **specialized AI agents**:
  - `Frontend Expert`
  - `Backend Expert`
  - `Web Developer Agent` (handles routing)
- 🔁 Dynamic **handoff** between agents using `handoffs=[]`.
- 🧰 Uses **OpenAI Agents SDK** and **Chainlit** for UI.
- 🔐 Loads API key securely via `.env`.

---

## 🧩 Architecture Overview

---

## 🧠 Agents Explanation

### 1. **Frontend Expert**
Helps with:
- HTML, CSS
- JavaScript, React, Next.js
- Tailwind CSS

🚫 Won’t answer backend questions.

---

### 2. **Backend Expert**
Helps with:
- APIs (REST, GraphQL)
- Databases
- Server-side frameworks (Express.js, Django)

🚫 Won’t answer frontend questions.

---

### 3. **Web Developer Agent** (Router)
- Acts like a router.
- Analyzes user's input.
- Forwards (or **handsoff**) the question to the relevant expert agent.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/subhankaladi/OpenAI_Agents_SDK.git
cd 00_TopicWise_Code/09_Routing
