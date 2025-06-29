# Gemini Agent Project

## Overview
This project demonstrates a simple chatbot implementation using the Gemini API through an OpenAI-compatible interface. It utilizes the `agents` library to create and run an agent specialized as a "Frontend Expert" that processes user input and generates responses.

## Prerequisites
- Python 3.8+
- Gemini API key 
- Required Python packages:
  - `openai-agents`
  - `python-dotenv`

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/subhankaladi/OpenAI_Agents_SDK.git
   ```

2. Install dependencies:
   ```
   pip install openai-agents python-dotenv
   cd 00_TopicWise_Code/00_Agent
   ```

3. Create a `.env` file in the project root and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage
1. Ensure the `.env` file is configured with your Gemini API key.
2. Run the script:
   ```
   python main.py
   ```
3. The script will initialize a "Frontend Expert" agent and process the input "Helo how are you". The response will be printed to the console.

## Code Explanation
- **Environment Setup**: Loads environment variables from a `.env` file using `python-dotenv`.
- **API Configuration**: Configures an `AsyncOpenAI` client with the Gemini API key and a custom base URL for the Gemini API.
- **Model Setup**: Uses `OpenAIChatCompletionsModel` with the `gemini-2.0-flash` model.
- **Agent Creation**: Creates a `Frontend Expert` agent with specific instructions.
- **Execution**: Runs the agent synchronously with a sample input using `Runner.run_sync`.
- **Output**: Prints the agent's final response.

## Example
Running the script with the input "Helo how are you" will generate a response from the Gemini model, which is then printed to the console.

## Notes
- Ensure your Gemini API key is valid and has appropriate permissions.
- The `tracing_disabled=True` setting in `RunConfig` disables tracing for this example.
- Modify the `instructions` in the `Agent` class to customize the agent's behavior.

## License
This project is licensed under the MIT License.
