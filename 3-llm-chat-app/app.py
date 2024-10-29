import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai
import anthropic
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live


# Connect to OpenAI, Anthropic and Google
# All 3 APIs are similar
# Having problems with API files? You can use openai = OpenAI(api_key="your-key-here") and same for claude
# Having problems with Google Gemini setup? Then just skip Gemini; you'll get all the experience you need from GPT and Claude.

openai = OpenAI()

claude = anthropic.Anthropic()

google.generativeai.configure()


# Let's make a conversation between GPT-4o-mini and Claude-3-haiku
# We're using cheap versions of models so the costs will be minimal

gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307"

gpt_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

claude_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."


def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, claude in zip(gpt_messages, claude_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": claude})
    completion = openai.chat.completions.create(model=gpt_model, messages=messages)
    return completion.choices[0].message.content


def call_claude():
    messages = []
    for gpt, claude_message in zip(gpt_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": claude_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    message = claude.messages.create(
        model=claude_model, system=claude_system, messages=messages, max_tokens=500
    )
    return message.content[0].text


gpt_messages = ["Hi there"]
claude_messages = ["Hi"]


print(f"GPT:\n{gpt_messages[0]}\n")
print(f"Claude:\n{claude_messages[0]}\n")

for i in range(5):
    gpt_next = call_gpt()
    print(f"GPT:\n{gpt_next}\n")
    gpt_messages.append(gpt_next)

    claude_next = call_claude()
    print(f"Claude:\n{claude_next}\n")
    claude_messages.append(claude_next)
