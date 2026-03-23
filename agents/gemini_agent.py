# agents/gemini_agent.py
import os
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# Configuration - gemini-2.5-flash é excelente para PoCs pela velocidade e custo
llm_model = "gemini-2.5-flash"

styles = [
    "formal and technical",
    "casual and friendly",
    "enthusiastic and persuasive",
    "concise and to the point",
    "storytelling and engaging",
]

tones = ["confident", "empathetic", "urgent", "optimistic", "serious"]

_client_initialized = False

def list_available_models():
    _init_client()
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

if __name__ == "__main__":
    list_available_models()

def _init_client():
    global _client_initialized
    if _client_initialized:
        return

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set in environment."
        )

    genai.configure(api_key=api_key)
    _client_initialized = True

def get_today_str() -> str:
    dt = datetime.now()
    return f"{dt.strftime('%a %b')} {dt.day}, {dt.year}"

def get_completion(prompt: str, model: str | None = None, temperature: float = 0.0) -> str:
    """
    Envia o prompt para a API do Google Gemini e retorna o texto gerado.
    """
    _init_client()
    model_name = model or llm_model
    
    # Configuração de geração
    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model_instance = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )

    response = model_instance.generate_content(prompt)
    
    return response.text