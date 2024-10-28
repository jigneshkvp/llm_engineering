import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich.markdown import Markdown
from rich.console import Console
from openai import OpenAI
from urllib.parse import urlparse

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-key-if-not-using-env")
openai = OpenAI()


class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)


system_prompt = (
    "You are an assistant that analyzes the contents of a website "
    "and provides a short summary, ignoring text that might be navigation related. "
    "Respond in markdown."
)


def user_prompt_for(website: Website):
    user_prompt = f"You are looking at a website titled {website.title}. "
    user_prompt += "The contents of this website are as follows; "
    user_prompt += "please provide a short summary of this website in markdown. "
    user_prompt += "If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)},
    ]


def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model="gpt-4o-mini", messages=messages_for(website)
    )
    return response.choices[0].message.content


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def display_summary(url):

    if not is_valid_url(url=url):
        print("Please provide a valid URL")
        return

    summary = summarize(url)
    console = Console()
    markdown_summary = Markdown(summary)
    console.print(markdown_summary)


# To display the summary, uncomment the following line:
display_summary("")
