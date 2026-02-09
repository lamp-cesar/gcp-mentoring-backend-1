AI Personal Trainer: Multi-Agent Workout Generator
Este projeto consiste em uma aplicação Python baseada em Arquitetura Multi-Agente para a criação de treinos de musculação hiper-personalizados. O diferencial da solução é o seu loop de refinamento autonômo, onde agentes especializados colaboram para garantir que a prescrição final atinja um padrão de qualidade superior a 8.5/10 antes de ser entregue ao usuário.

🤖 A Arquitetura dos Agentes
A aplicação opera através de três núcleos de inteligência:

Agente de Anamnese: Processa os dados brutos do usuário (idade, peso, lesões, objetivos, disponibilidade) e extrai os requisitos técnicos.

Agente Treinador (Personal Trainer): Recebe os requisitos e monta a estrutura de treino (exercícios, séries, repetições e períodos de descanso).

Agente Avaliador (QA/Validador): Atua como um auditor. Ele avalia o treino gerado comparando-o com as melhores práticas de fisiologia do exercício e atribui uma nota. Se a nota for inferior a 8.5, o treino retorna ao Treinador com o feedback detalhado para ajustes.

🚀 Como Executar
Atualmente, a aplicação está configurada para execução em ambiente local via terminal.

1. Pré-requisitos
Python 3.10 ou superior.

Uma chave de API (OpenAI, Anthropic ou Google Gemini) configurada no .env.

2. Instalação
Clone o repositório e instale as dependências:

Bash
# Clone o repositório
git clone https://github.com/seu-usuario/ai-personal-trainer.git
cd ai-personal-trainer

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
3. Configuração
Crie um arquivo .env na raiz do projeto e adicione suas variáveis de ambiente:

Snippet de código
# Exemplo de configuração
API_KEY=sua_chave_aqui
LOG_LEVEL=INFO
4. Execução
Para iniciar o processo de geração do treino:

Bash
python main.py
☁️ Roadmap de Deploy
[ ] Containerização via Docker.

[ ] Criação de CI/CD via GitHub Actions.

[ ] Deploy em GCP Cloud Run.

[ ] Exposição de endpoint via API Fast API.