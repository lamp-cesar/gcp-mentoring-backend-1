import json
from agents.gemini_agent import get_completion

def workout_validator(anamnesis_result: str, workout_plan: str) -> dict:
    prompt_task = """Você é um Auditor Sênior de Fisiologia do Exercício. Sua única função é garantir que o treino prescrito seja SEGURO, EFICAZ e COERENTE com a anamnese fornecida."""

    prompt_instructions = """
    <Instructions>
    1. Analise se o volume (séries/repetições) é adequado para o nível de experiência do usuário.
    2. Verifique se a seleção de exercícios faz sentido para o objetivo principal.
    3. Identifique erros graves (ex: treinar o mesmo músculo todos os dias, falta de descanso, exercícios perigosos para iniciantes).
    4. Atribua uma nota (score) de 0.0 a 10.0.
    5. Se a nota for abaixo de 8.5, descreva exatamente o que o Agente Treinador deve corrigir em 'adjustments'.
    6. O retorno DEVE ser EXCLUSIVAMENTE um objeto JSON.
    </Instructions>
    """

    prompt_structure = """
    <Response_Format>
    {
        "score": float,
        "adjustments": "string detalhando o que melhorar ou confirmando a qualidade",
        "is_safe": boolean,
        "critical_flaw_detected": boolean
    }
    </Response_Format>
    """

    prompt_context = f"""
    <Anamnesis_Context>
    {anamnesis_result}
    </Anamnesis_Context>

    <Proposed_Workout>
    {workout_plan}
    </Proposed_Workout>
    """

    full_prompt = f"{prompt_task}\n{prompt_instructions}\n{prompt_structure}\n{prompt_context}"
    raw_response = get_completion(full_prompt, temperature=0.0)

    try:
        json_str = raw_response.replace("```json", "").replace("```", "").strip()
        validation_data = json.loads(json_str)
        
        if "score" not in validation_data:
            validation_data["score"] = 0.0
            
        return validation_data

    except Exception as e:
        print(f"Erro no parsing do Validador: {e}")
        return {
            "score": 0.0,
            "adjustments": "Erro técnico ao processar resposta do validador. Refazer geração.",
            "is_safe": False,
            "critical_flaw_detected": True
        }