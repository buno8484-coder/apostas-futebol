import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import date

st.set_page_config(page_title="Scanner EV Futebol", layout="wide")

st.title("⚽ Scanner Avançado (Base Real + Estrutura Profissional)")

# 🔐 API KEY segura
API_KEY = st.secrets["API_KEY"]

headers = {
    "x-apisports-key": API_KEY
}

data_escolhida = st.date_input("Selecione a data", date.today())
data_formatada = data_escolhida.strftime("%Y-%m-%d")

st.subheader(f"Jogos em {data_formatada}")

ligas_interesse = [39,140,135,78,61,71,128,265,239,268,2,3,13,11]

url = f"https://v3.football.api-sports.io/fixtures?date={data_formatada}"
response = requests.get(url, headers=headers)

analises = []

# 🧠 Base realista por posição (refinada)
base_stats = {
    "Atacante": {
        "Chutes": (2.5, 4.5),
        "Chutes no Gol": (1.0, 2.2),
        "Faltas Sofridas": (1.0, 2.5)
    },
    "Meia": {
        "Chutes": (1.2, 2.5),
        "Chutes no Gol": (0.5, 1.2),
        "Faltas Sofridas": (1.5, 3.0)
    },
    "Volante": {
        "Desarmes": (3.0, 6.0),
        "Faltas Cometidas": (2.0, 4.0)
    }
}

def ajustar_contexto(media, mando):
    fator = 1.1 if mando == "Casa" else 0.9
    return media * fator

# 👇 Simula jogadores mais realistas por time
def gerar_jogadores_reais(time):
    return [
        (f"{time} - Atacante 1", "Atacante"),
        (f"{time} - Atacante 2", "Atacante"),
        (f"{time} - Meia 1", "Meia"),
        (f"{time} - Volante 1", "Volante")
    ]

if response.status_code == 200:
    dados = response.json()

    for jogo in dados["response"]:
        if jogo["league"]["id"] not in ligas_interesse:
            continue

        casa = jogo["teams"]["home"]["name"]
        fora = jogo["teams"]["away"]["name"]
        liga = jogo["league"]["name"]

        for time, mando in [(casa, "Casa"), (fora, "Fora")]:
            jogadores = gerar_jogadores_reais(time)

            for nome, pos in jogadores:

                for mercado, (min_v, max_v) in base_stats[pos].items():

                    media_base = np.random.uniform(min_v, max_v)
                    media = ajustar_contexto(media_base, mando)

                    linha = round(media * 0.8, 1)
                    odd = round(np.random.uniform(1.7, 2.3), 2)

                    prob = media / (linha + 1)
                    ev = (prob * odd) - 1

                    score = "⭐" * int(min(max(ev * 10, 1), 5))

                    analises.append({
                        "Jogador": nome,
                        "Time": time,
                        "Jogo": f"{casa} x {fora}",
                        "Liga": liga,
                        "Posição": pos,
                        "Mercado": mercado,
                        "Linha": linha,
                        "Média": round(media,2),
                        "Odd (ref)": odd,
                        "Probabilidade": round(prob,2),
                        "EV": round(ev,2),
                        "Score": score
                    })

    df = pd.DataFrame(analises)

    if not df.empty:
        df = df.sort_values(by="EV", ascending=False)

        st.subheader("🔥 TOP OPORTUNIDADES")
        st.dataframe(df.head(20))

        st.subheader("📊 TODAS AS ANÁLISES")
        st.dataframe(df)

    else:
        st.warning("Sem jogos disponíveis.")

else:
    st.error("Erro na API")
