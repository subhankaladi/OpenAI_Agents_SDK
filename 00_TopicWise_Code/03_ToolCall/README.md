# 🌦️ Joke & Weather Agent using OpenAI Agents SDK

This project demonstrates how to create a simple Language Learning Model (LLM) agent using the **OpenAI Agents SDK**. The agent can handle external function calls (tool calling) such as fetching weather data for a city or generating a random number of jokes using the `@function_tool` decorator.

## 🚀 Features

- 🌤️ Get real-time weather for any city using WeatherAPI
- 🤣 Get a random number of jokes using built-in Python random module
- 🧠 Tool calling powered by `@function_tool` using OpenAI Agents SDK
- 🔑 Gemini (Google's LLM) support using OpenAIChatCompletionsModel adapter

---

## 🛠️ Tech Stack

- Python
- [OpenAI Agents SDK](https://github.com/openai/openai-agents)
- Gemini 2.0 Flash model (via OpenAI compatibility layer)
- WeatherAPI
- `requests`, `dotenv`

---

## 📆 Requirements

- Python 3.9+
- API Key for:
  - [WeatherAPI](https://www.weatherapi.com/)
  - [Gemini via OpenAI-compatible endpoint](https://ai.google.dev/)

---

## 📁 Project Structure

```
.
├── .env
├── main.py          # Your agent code
└── README.md
```

---

## 📄 Environment Variables

Make sure to set your environment variables in a `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🧠 How It Works

### ✅ 1. Agent Initialization

The agent is initialized with:

- A Gemini-compatible model
- Instructions that tell the agent **how to behave**
- Tools that it can call using decorators

```python
agent = Agent(
    name="Assistant",
    instructions="""
if the user asks for jokes, first call 'how_many_jokes' function, then tell that jokess with numbers.
if the user asks for weather, call the 'get_weather' funciton with city name
""",
    model=model,
    tools=[get_weather, how_many_jokes]
)
```

---

### 🔧 2. Tool Functions

#### `how_many_jokes`

Generates a random number between 1 and 10.

```python
@function_tool
def how_many_jokes():
    return random.randint(1, 10)
```

#### `get_weather`

Fetches the current weather using the WeatherAPI.

```python
@function_tool
def get_weather(city: str) -> str:
    ...
```

---

### ▶️ 3. Run the Agent

You can run the agent and provide it with user input:

```python
result = Runner.run_sync(
    agent,
    input="tell me karachi weather",
)
print(result.final_output)
```

The agent will:

- Detect the user's intent (weather or joke)
- Automatically call the appropriate tool
- Return a final response based on tool output

---

## 📦 Installation

```bash
pip install openai-agents python-dotenv requests
```

---

## 🌐 Example Output

```
The current weather in Karachi is 34°C with Partly Cloudy.
```

---

## 📌 Notes

- Ensure your Gemini API supports the OpenAI compatible endpoint
- This setup is ideal for learning **tool calling**, **LLM orchestration**, and **real-world API usage** with agents.

---

## 📜 License

MIT License

---

## 🤝 Contributing

Feel free to fork the repo and add more tools like:

- News API
- Currency converter
- Random facts

