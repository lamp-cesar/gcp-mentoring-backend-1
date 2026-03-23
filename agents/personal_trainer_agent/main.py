from datetime import datetime
from ..gemini_agent import get_completion
    
# prompts/workout_prompts.py
prompt_task = """Você é um Treinador de Musculação de Elite (Strength and Conditioning Coach). 
Sua tarefa é converter um briefing técnico de anamnese em um plano de treinamento de musculação prático, 
detalhado e periodizado. Hoje é {date}.

<Task>
Criar um programa de treinamento completo, especificando exercícios, séries, repetições, tempos de descanso e a 
lógica de grupamentos musculares por dia.
</Task>
"""

prompt_context = """
<Context>
Análise Técnica (Anamnese):
{anamnesis_result}

Estilo de Comunicação: {style}
Tom de Voz: {tone}
</Context>
"""

prompt_instructions = """
<Instructions>
1. Respeite rigorosamente o nível de experiência e o objetivo citados na anamnese.
2. Defina a divisão semanal (ex: Segunda: Peito/Tríceps, Terça: Costas/Bíceps, etc.) com base na frequência recomendada.
3. Para cada exercício, inclua: Nome do exercício, Séries x Repetições, e Tempo de Descanso.
4. Adicione uma breve nota técnica de "Dica do Treinador" para exercícios complexos.
5. Utilize tabelas ou listas claras para facilitar a leitura no mobile.
6. Mantenha o estilo {style} e o tom {tone}.
</Instructions>
"""

prompt_structure = """
<Structure>
1. Resumo da Estratégia de Treino (O "Porquê" desse plano)
2. Cronograma Semanal (Dias de treino vs. Dias de descanso)
3. Fichas de Treino Detalhadas (Treino A, B, C...)
4. Orientações de Progressão de Carga
</Structure>
"""

prompt_references = """
<Example>
Treino A: Membros Superiores (Foco Empurrar)
- Supino Reto com Barra: 4 x 8-10 (90s descanso)
- Desenvolvimento com Halteres: 3 x 12 (60s descanso)
...
Dica: Mantenha as escápulas retraídas no supino para proteger os ombros.
</Example>
"""

prompt_feedback = """
<Refinement_Feedback>
O seu treino anterior foi avaliado por um auditor e recebeu as seguintes críticas para correção:
{feedback}

Por favor, mantenha o que estava bom e corrija especificamente os pontos citados acima.
</Refinement_Feedback>
"""
    
def workout_plan_main(anamnesis_result: str, feedback: str = "") -> str:
    selected_style = "concise and to the point"
    selected_tone = "confident"

    feedback_section = ""
    if feedback and feedback != "First Version.":
        feedback_section = prompt_feedback.format(feedback=feedback)

    full_prompt = f"""
    {prompt_task.format(date=datetime.now().strftime('%Y-%m-%d'))}
    
    {prompt_context.format(
        anamnesis_result=anamnesis_result,
        style=selected_style,
        tone=selected_tone
    )}
    
    {feedback_section}

    {prompt_instructions.format(style=selected_style, tone=selected_tone)}
    
    {prompt_structure}
    
    {prompt_references}
    """
    
    workout_plan = get_completion(full_prompt, temperature=0.7)
    
    return workout_plan