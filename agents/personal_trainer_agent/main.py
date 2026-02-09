from ..gemini_agent import get_completion

# Import shared OpenAI helper. Support running as script or as package.
try:
    from agents.gemini_agent import get_completion, styles, tones, get_today_str, llm_model
except Exception:
    import sys, os
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)
    from agents.gemini_agent import get_completion, styles, tones, get_today_str, llm_model
    
def workout_plan_main(anamnesis) -> str:
    return "Oi sou seu treinador, aqui está sua Anamnesis: " + anamnesis