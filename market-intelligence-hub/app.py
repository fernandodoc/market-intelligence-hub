import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import feedparser
import requests
from datetime import datetime
from textblob import TextBlob

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Elite Financial Hub", layout="wide")

# --- ESTILIZAÇÃO TERMINAL BLOOMBERG ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    div[data-testid="stMetricValue"] { color: #00ff41; }
    .news-card { padding: 15px; border-bottom: 1px solid #30363d; background-color: #161b22; margin-bottom: 10px; border-radius: 5px; }
    .news-title { color: #58a6ff; font-weight: bold; text-decoration: none; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DO TERMINAL DE NOTÍCIAS (CORE) ---
class NewsEngine:
    def __init__(self):
        self.sources = {
            "InfoMoney": "https://www.infomoney.com.br/feed/",
            "Investing.com": "https://br.investing.com/rss/news.rss",
            "Valor": "https://valor.globo.com/rss/valor/",
            "CNBC Markets": "https://search.cnbc.com/rs/search/combinedfeed.view?articlePubDate=0&output=rss&searchterm=markets"
        }

    def _analyze(self, text):
        score = TextBlob(text).sentiment.polarity
        if score > 0.05: return "BULLISH 🟢"
        if score < -0.05: return "BEARISH 🔴"
        return "NEUTRAL ⚪"

    def fetch(self):
        all_news = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        for name, url in self.sources.items():
            try:
                resp = requests.get(url, headers=headers, timeout=5)
                feed = feedparser.parse(resp.content)
                for entry in feed.entries[:3]:
                    all_news.append({
                        "title": entry.title, "link": entry.link, "source": name,
                        "sentiment": self._analyze(entry.title),
                        "date": entry.get("published", "")
                    })
            except: continue
        return pd.DataFrame(all_news).drop_duplicates(subset=['title']).head(7)

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2632/2632283.png", width=100)
    st.title("Elite Hub")
    page = st.radio("Navegação", ["📊 Diagnóstico Patrimonial", "📟 Terminal de Notícias", "👤 Perfil do Especialista"])
    st.info(f"Usuário: Fernando Cláudio\nCertificações: CEA, ANCORD")

# --- PÁGINA 1: DIAGNÓSTICO ---
if page == "📊 Diagnóstico Patrimonial":
    st.header("🏛️ Inteligência Wealth Management")
    
    with st.form("diagnostico"):
        c1, c2 = st.columns(2)
        receita = c1.number_input("Receita Mensal Líquida", value=25000.0)
        patrimonio = c1.number_input("Patrimônio Atual", value=300000.0)
        meta = c2.number_input("Meta de Patrimônio", value=1000000.0)
        ipca = st.slider("Expectativa IPCA (% a.a.)", 2.0, 12.0, 4.5) / 100
        btn = st.form_submit_button("PROCESSAR ALGORITMO")

    if btn:
        perda = patrimonio * ipca
        st.metric("Risco de Erosão (12 meses)", f"R$ {perda:,.2f}")
        st.error(f"Atenção: A inflação pode subtrair o poder de compra de {perda:,.2f} do seu patrimônio atual.")
        
        fig, ax = plt.subplots()
        ax.pie([patrimonio - perda, perda], labels=['Patrimônio Protegido', 'Erosão IPCA'], colors=['#00ff41', '#ff4b4b'])
        fig.patch.set_facecolor('#0e1117')
        st.pyplot(fig)

# --- PÁGINA 2: TERMINAL DE NOTÍCIAS ---
elif page == "📟 Terminal de Notícias":
    st.header("📟 Market Intelligence Terminal")
    engine = NewsEngine()
    with st.spinner("Sincronizando com as mesas de operações..."):
        df = engine.fetch()
        for _, row in df.iterrows():
            st.markdown(f"""
                <div class="news-card">
                    <span style="font-size: 0.8rem; color: #8b949e;">{row['source']} | {row['sentiment']}</span><br>
                    <a class="news-title" href="{row['link']}" target="_blank">{row['title']}</a>
                </div>
            """, unsafe_allow_html=True)

# --- PÁGINA 3: PERFIL ---
elif page == "👤 Perfil do Especialista":
    st.header("Especialista de Investimentos")
    st.subheader("Fernando de Oliveira Cláudio")
    st.write("Expert em alocação de ativos e inteligência financeira para clientes de alto patrimônio.")
    st.markdown("""
    - **Certificações:** C-PRO I, C-PRO R, ANCORD, CEA, CPA-20
    - **Foco:** Captação acima de R$ 300.000,00
    - **Local:** Ribeirão Preto / SP
    """)
    st.button("Entrar em Contato via WhatsApp")
