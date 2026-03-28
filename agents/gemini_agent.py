# agents/gemini_agent.py
import os
from google import genai
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# Configuration - gemini-2.5-flash is excellent for PoCs due to speed and cost
llm_model = "gemini-2.5-flash"

styles = [
    "formal and technical",
    "casual and friendly",
    "enthusiastic and persuasive",
    "concise and to the point",
    "storytelling and engaging",
]

tones = ["confident", "empathetic", "urgent", "optimistic", "serious"]

_client = None


def _get_client():
    """Get or create the Gemini API client."""
    global _client
    if _client is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY is not set in environment."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def list_available_models():
    client = _get_client()
    for m in client.models.list():
        if hasattr(m, 'supported_generation_methods') and 'generateContent' in m.supported_generation_methods:
            print(m.name)


if __name__ == "__main__":
    list_available_models()


def get_today_str() -> str:
    dt = datetime.now()
    return f"{dt.strftime('%a %b')} {dt.day}, {dt.year}"


def get_completion(prompt: str, model: str | None = None, temperature: float = 0.0) -> str:
    """
    Sends the prompt to Google Gemini API and returns the generated text.
    """
    client = _get_client()
    model_name = model or llm_model

    # Generation configuration
    config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config,
    )

    return response.text
