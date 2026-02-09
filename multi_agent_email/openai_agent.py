import os
import openai
from datetime import datetime

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file if present

# Configuration
llm_model = "gpt-4o-mini"

styles = [
    "formal and technical",
    "casual and friendly",
    "enthusiastic and persuasive",
    "concise and to the point",
    "storytelling and engaging",
]

tones = ["confident", "empathetic", "urgent", "optimistic", "serious"]


# Lazy OpenAI client initialization to make the module safe for import
_client = None


def _init_client():
    global _client
    if _client is not None:
        return _client

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set in environment. Set it or call after configuring the env."
        )

    openai.api_key = api_key
    _client = openai.OpenAI()
    return _client


def get_client():
    return _init_client()


def get_today_str() -> str:
    dt = datetime.now()
    return f"{dt.strftime('%a %b')} {dt.day}, {dt.year}"


def get_completion(prompt: str, model: str | None = None, temperature: float = 0.0) -> str:
    """Send `prompt` to the OpenAI chat completion API and return text.

    This wraps the client call and uses lazy initialization so importing
    this module doesn't require `OPENAI_API_KEY` to be present.
    """
    client = get_client()
    model = model or llm_model

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(model=model, messages=messages, temperature=temperature)

    return response.choices[0].message.content
