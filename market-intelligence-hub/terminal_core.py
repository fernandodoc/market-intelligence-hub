import feedparser
import pandas as pd
from datetime import datetime
from textblob import TextBlob
import requests

class FinanceTerminal:
    def __init__(self):
        self.sources = {
            "InfoMoney": "https://www.infomoney.com.br/feed/",
            "Investing.com": "https://br.investing.com/rss/news.rss",
            "CNBC": "https://search.cnbc.com/rs/search/combinedfeed.view?articlePubDate=0&output=rss&searchterm=markets",
            "Valor Econômico": "https://valor.globo.com/rss/valor/",
            "Reuters": "https://news.google.com/rss/search?q=site:reuters.com+finance&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        }
        
        self.categories = {
            "Política Monetária": ["selic", "copom", "fed", "juros", "inflação", "ipca"],
            "Ações": ["ibovespa", "ações", "balanço", "dividendos", "petr4", "vale3"],
            "Câmbio": ["dólar", "cambio", "moeda"],
            "Macro": ["pib", "fiscal", "economia", "tesouro"]
        }

    def _categorize(self, title):
        title_lower = title.lower()
        for cat, keywords in self.categories.items():
            if any(kw in title_lower for kw in keywords):
                return cat
        return "Geral"

    def _analyze_sentiment(self, text):
        analysis = TextBlob(text)
        score = analysis.sentiment.polarity
        bull = ['alta', 'lucro', 'sobe', 'cresce', 'compra', 'supera']
        bear = ['queda', 'prejuízo', 'cai', 'recessão', 'venda', 'crise']
        t = text.lower()
        for w in bull: 
            if w in t: score += 0.25
        for w in bear: 
            if w in t: score -= 0.25
        if score > 0.05: return "BULLISH 🟢"
        if score < -0.05: return "BEARISH 🔴"
        return "NEUTRAL ⚪"

    def fetch_news(self):
        all_data = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        for name, url in self.sources.items():
            try:
                # Timeout curto para não travar o terminal se um site cair
                response = requests.get(url, headers=headers, timeout=5)
                feed = feedparser.parse(response.content)
                
                # Pegamos apenas as 5 mais recentes de CADA fonte para processar
                for entry in feed.entries[:5]:
                    all_data.append({
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", datetime.now().strftime("%H:%M")),
                        "source": name,
                        "category": self._categorize(entry.title),
                        "sentiment": self._analyze_sentiment(entry.title)
                    })
            except:
                continue
        
        if not all_data:
            return pd.DataFrame()

        df = pd.DataFrame(all_data).drop_duplicates(subset=['title'])

        # --- LÓGICA DE DIVERSIDADE (1 de cada site) ---
        # Agrupamos por fonte e pegamos a primeira notícia de cada uma
        diverse_df = df.groupby('source').first().reset_index()
        
        # Se ainda sobrarem vagas para chegar a 7, preenchemos com as restantes
        if len(diverse_df) < 7:
            remaining = df[~df['title'].isin(diverse_df['title'])]
            diverse_df = pd.concat([diverse_df, remaining.head(7 - len(diverse_df))])

        return diverse_df.head(7)