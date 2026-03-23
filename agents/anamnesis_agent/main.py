from datetime import datetime
from ..gemini_agent import get_completion
    
# prompts/anamnesis_prompts.py
prompt_task = """Você é um Especialista em Saúde e Fisiologia do Exercício de alto nível. Sua tarefa é realizar uma
análise clínica detalhada (anamnese) baseada em dados brutos do usuário. Hoje é {date}.

<Task>
Transformar dados básicos de um usuário em um perfil fisiológico detalhado e fornecer recomendações técnicas para
construção de um programa de treinamento personalizado.
</Task>

O seu output servirá como o "Briefing Técnico" para um Treinador de Elite montar o treino.
"""

prompt_context = """
<Context>
Dados do Usuário:
- Nome: {name}
- Idade: {age} anos
- Peso: {weight} kg
- Objetivo: {goal}
- Nível de Experiência: {experience_level}

Estilo de Comunicação: {style}
Tom de Voz: {tone}
</Context>
"""

prompt_instructions = """
<Instructions>
1. Analise o objetivo ({goal}) em relação à idade e nível de experiência.
2. Identifique possíveis restrições ou cuidados fisiológicos comuns para este perfil (ex: cuidados articulares para
iniciantes ou volume de carga para avançados).
3. Determine a frequência semanal ideal e a divisão de treino recomendada (ex: Full Body, AB, ABC).
4. Forneça "Diretrizes de Ouro" para o próximo agente (o Treinador) seguir.
5. Mantenha o estilo {style} e o tom {tone} em toda a análise.
6. Seja técnico onde necessário, mas garanta que as recomendações sejam acionáveis.
</Instructions>
"""

prompt_structure = """
<Structure>
1. Perfil Bio-Psicossocial (Resumo do usuário)
2. Análise de Viabilidade do Objetivo
3. Recomendações de Volume e Intensidade
4. Divisão de Treino Sugerida
5. Observações de Segurança e Saúde
</Structure>
"""

prompt_references = """
<Example>
Exemplo de análise técnica e formal:
"Paciente de 30 anos, nível intermediário, visando hipertrofia. Considerando o peso de 85kg e histórico de treino,
recomenda-se uma abordagem de microciclos de 4 a 5 dias. Foco em progressão de carga linear e controle de volume para
evitar sobrecarga em tendões. Divisão sugerida: ABCDE com foco em grupos musculares grandes."
</Example>
"""

def anamnesis_main(data) -> str:
    selected_style = "formal and technical"
    selected_tone = "confident"
    
    full_prompt = f"""
    {prompt_task.format(date=datetime.now().strftime('%Y-%m-%d'))}
    {prompt_context.format(
        name=data.name, 
        age=data.age, 
        weight=data.weight, 
        goal=data.goal, 
        experience_level=data.experience_level,
        style=selected_style,
        tone=selected_tone
    )}
    {prompt_instructions.format(goal=data.goal, style=selected_style, tone=selected_tone)}
    {prompt_structure}
    {prompt_references}
    """
    
    ai_response = get_completion(full_prompt)
    
    return ai_response