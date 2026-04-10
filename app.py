import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import date

st.set_page_config(page_title="Scanner de Apostas", layout="wide")

st.title("⚽ Scanner de Apostas com EV+")

API_KEY = "a210552d9ca862c4801da1d9a589ceb7"

headers = {
    "x-apisports-key": API_KEY
}

# 📅 Data
data_escolhida = st.date_input("Selecione a data", date.today())
data_formatada = data_escolhida.strftime("%Y-%m-%d")

st.subheader(f"Jogos em {data_formatada}")

# 🔎 Buscar jogos
url = f"https://v3.football.api-sports.io/fixtures?date={data_formatada}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    
    analises = []

    for jogo in dados["response"][:5]:  # limita pra não estourar API
        time_casa = jogo["teams"]["home"]["name"]
        time_fora = jogo["teams"]["away"]["name"]

        # 👇 SIMULAÇÃO (depois vamos trocar por real)
        jogadores = [
            {"nome": "Atacante A", "media": np.random.uniform(2,4), "linha": 2.5, "odd": 2.10, "tipo": "Chutes"},
            {"nome": "Meia B", "media": np.random.uniform(1,3), "linha": 1.5, "odd": 1.80, "tipo": "Chutes no Gol"},
            {"nome": "Volante C", "media": np.random.uniform(2,5), "linha": 3.5, "odd": 2.00, "tipo": "Desarmes"},
        ]

        for j in jogadores:
            media = j["media"]
            linha = j["linha"]
            odd = j["odd"]

            # 📊 Probabilidade simples (ajustada)
            prob = media / (linha + 1)

            # 💰 EV
            ev = (prob * odd) - 1

            analises.append({
                "Jogo": f"{time_casa} x {time_fora}",
                "Jogador": j["nome"],
                "Mercado": j["tipo"],
                "Linha": linha,
                "Média": round(media,2),
                "Probabilidade": round(prob,2),
                "Odd": odd,
                "EV": round(ev,2)
            })

    df = pd.DataFrame(analises)

    # Ranking
    df = df.sort_values(by="EV", ascending=False)

    st.subheader("🔥 Melhores oportunidades")
    st.dataframe(df.head(10))

    st.subheader("📊 Todas análises")
    st.dataframe(df)

else:
    st.error("Erro ao buscar jogos")
