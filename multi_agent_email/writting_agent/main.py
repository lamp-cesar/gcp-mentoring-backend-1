# Import shared OpenAI helper. Support running as script or as package.
try:
    from multi_agent_email.openai_agent import get_completion, styles, tones, get_today_str, llm_model
except Exception:
    import sys, os
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)
    from openai_agent import get_completion, styles, tones, get_today_str, llm_model

customer_email = """\
Crie um email para um cliente corporativo apresentando nossa solução
de visão computacional para inspeção industrial. O estilo deve ser
formal e técnico, com tom confiante e persuasivo. Inclua um CTA para
agendar uma demonstração.
"""

def writting_main(reflection: str) -> str:
    prompt_formatted = reflection.format(
        customer_email=customer_email, style=styles[0], tone=tones[0], date=get_today_str()
    )
    result = get_completion(prompt_formatted)
    return result