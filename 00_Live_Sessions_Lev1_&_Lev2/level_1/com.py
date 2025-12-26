# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI()

# resp = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "hello"}],
# )

# print(resp)  # yahan usage field absent/missing honi chahiye


from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# initialize client
client = OpenAI()

# request completion with logprobs
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",   # logprobs works on instruct models, not chat
    prompt="Explain Python in short.",
    max_tokens=30,
    logprobs=5   # return logprobs for top 5 tokens at each step
)

# print tokens with logprobs
for choice in response.choices:
    for token, logprob in zip(choice.logprobs.tokens, choice.logprobs.token_logprobs):
        print(f"Token: {token}, LogProb: {logprob}")
