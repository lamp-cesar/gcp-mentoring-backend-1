try:
    from multi_agent_email.openai_agent import get_completion, styles, tones, get_today_str, llm_model
except Exception:
    import sys, os
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)
    from openai_agent import get_completion, styles, tones, get_today_str, llm_model


def appraisal_agent(email: str) -> str:
    prompt = f"""
    Avalie o seguinte email:
    {email}
    
    Forneça uma avaliação técnica e construtiva sobre o conteúdo, estilo e tom do email.
    Também de uma nota de 1 a 10 sobre a clareza, profissionalismo e adequação ao público-alvo.
    """
    appraisal = get_completion(prompt)
    return appraisal