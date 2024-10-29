import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from openai import OpenAI
from time import sleep
from urllib.parse import urlparse

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-key-if-not-using-env")
MODEL = "gpt-4o-mini"
openai = OpenAI()


class Website:
    url: str
    title: str
    body: str
    links: List[str]
    text: str

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        links = [link.get("href") for link in soup.find_all("a")]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"


link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""


def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


def get_links(url):
    website = Website(url)
    completion = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)},
        ],
        response_format={
            "type": "json_object"
        },  # MUST RESPOND IN JSON USING THE FORMAT SPECIFIED IN SYSTEM PROMPT
    )
    result = completion.choices[0].message.content
    return json.loads(result)


def get_all_details(url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result


system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short humorous, jokey, entertaining brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."


def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:20_000]  # Truncate if more than 20,000 characters
    return user_prompt


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def create_brochure(company_name, url, use_stream=False):

    if not is_valid_url(url=url):
        print("Please provide a valid URL")
        return

    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)},
        ],
        stream=use_stream,
    )

    result = ""
    console = Console()
    if not use_stream:
        result = response.choices[0].message.content
        markdown_summary = Markdown(result)
        console.print(markdown_summary)
    else:
        with Live(console=console, refresh_per_second=4) as live:
            for chunk in response:
                result += chunk.choices[0].delta.content or ""
                live.update(Markdown(result))


create_brochure("", "", use_stream=True)