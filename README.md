📟 Market Intelligence Terminal (MVP)
Um terminal de notícias financeiras de alta performance desenvolvido em Python e Streamlit, inspirado na experiência de terminais profissionais como Bloomberg e InfoMoney. 
O sistema automatiza a coleta, categorização e análise de sentimento de notícias provenientes das principais fontes do mercado financeiro.

🎯 Objetivo
O sistema foi projetado para fornecer um "Daily Briefing" ultra-focado, consolidando exatamente as notícias mais relevantes do dia, evitando a sobrecarga de informações e garantindo diversidade de fontes.

🚀 Funcionalidades

- Agregação Multi-fonte: Coleta em tempo real via RSS/HTTP de fontes como InfoMoney, Investing.com, Valor Econômico, CNBC e Reuters.

- Lógica de Diversidade (Round Robin): Garante a exibição de pelo menos uma notícia relevante de cada portal cadastrado.

- Análise de Sentimento: Motor de inteligência que classifica as manchetes em BULLISH 🟢, BEARISH 🔴 ou NEUTRAL ⚪.

- Categorização Automática: Filtra conteúdos por Política Monetária, Ações, Câmbio e Macroeconomia.

- Interface Terminal: UX otimizada em Dark Mode para leitura rápida e profissional.

🛠️ Stack Técnica

- Linguagem: Python 3.10+

- Interface: Streamlit

- Data Handling: Pandas

- Parser: Feedparser / Requests

- NLP: TextBlob (Processamento de Linguagem Natural)

📁 Estrutura do Projeto

Plaintext
/fin-terminal-mvp
│-- app.py              # Interface do usuário e renderização
│-- terminal_core.py    # Engine de coleta e lógica de negócio
│-- requirements.txt    # Dependências do sistema
│-- README.md           # Documentação

🔧 Instalação e Execução

Clone o repositório ou crie a pasta do projeto.

Instale as dependências:
Bash
pip install streamlit feedparser pandas textblob requests

Baixe os pacotes de NLP necessários:
Bash
python -m textblob.download_corpora

Execute o Terminal:
Bash
streamlit run app.py

📈 Roadmap de Evolução (Versão PRO)
[ ] Integração com LLM (Gemini/GPT-4): Resumos automáticos de 3 linhas para cada notícia.
[ ] Alertas Push: Envio do briefing matinal via Telegram ou WhatsApp.
[ ] Data Scraping Avançado: Coleta de balanços diretamente do site da CVM.
[ ] Dashboard de Ativos: Integração de tickers em tempo real ao lado das notícias.

Contato
@ofernandodoc
