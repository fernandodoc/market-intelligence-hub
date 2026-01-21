import streamlit as st
from terminal_core import FinanceTerminal
from datetime import datetime

st.set_page_config(page_title="Terminal Financeiro Elite", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .card {
        padding: 1.2rem;
        border-radius: 8px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 12px;
    }
    .title-link { color: #58a6ff; font-size: 1.15rem; font-weight: bold; text-decoration: none; }
    .title-link:hover { text-decoration: underline; color: #79c0ff; }
    .label { font-size: 0.7rem; font-weight: bold; padding: 2px 8px; border-radius: 10px; }
    .source-label { color: #f0883e; font-family: monospace; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("📟 MARKET NEWS TERMINAL")
    st.markdown(f"**Monitor Global** | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    if st.button("🔄 ATUALIZAR TERMINAL"):
        st.cache_data.clear()
        st.rerun()

    terminal = FinanceTerminal()
    
    with st.spinner("Sincronizando múltiplas fontes (Investing, CNBC, Valor, InfoMoney)..."):
        df = terminal.fetch_news()

    if not df.empty:
        for _, row in df.iterrows():
            st.markdown(f"""
                <div class="card">
                    <span class="label" style="background:#238636; color:white;">{row['category']}</span>
                    <span style="margin-left:10px; font-weight:bold;">{row['sentiment']}</span>
                    <br><br>
                    <a class="title-link" href="{row['link']}" target="_blank">{row['title']}</a>
                    <br><br>
                    <span class="source-label">FONTE: {row['source'].upper()}</span> 
                    <span style="color:#8b949e; font-size:0.8rem; margin-left:15px;">| {row['published']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Nenhuma notícia encontrada. Verifique sua conexão com a internet.")

if __name__ == "__main__":
    main()