import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-key-if-not-using-env")
os.environ["ANTHROPIC_API_KEY"] = os.getenv(
    "ANTHROPIC_API_KEY", "your-key-if-not-using-env"
)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "your-key-if-not-using-env")

MODEL = "gpt-4o-mini"
openai = OpenAI()


def chat(message, history):
    messages = [{"role": "system", "content": system_message}]
    for user_message, assistant_message in history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": assistant_message})

    if "belt" in message:
        messages.append(
            {
                "role": "system",
                "content": "For added context, the store does not sell belts, \
but be sure to point out other items on sale",
            }
        )

    messages.append({"role": "user", "content": message})

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response


system_message = "You are a helpful assistant in a clothes store. You should try to gently encourage \
the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. \
For example, if the customer says 'I'm looking to buy a hat', \
you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.'\
Encourage the customer to buy hats if they are unsure what to get. \
If the customer asks for shoes, you should respond that shoes are not on sale today, \
but remind the customer to look at hats!"


gr.ChatInterface(fn=chat).launch()
