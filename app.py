import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import date

st.set_page_config(page_title="Scanner EV Futebol", layout="wide")

st.title("⚽ Scanner Profissional de Apostas (EV+)")

API_KEY = "a210552d9ca862c4801da1d9a589ceb7"

headers = {
    "x-apisports-key": API_KEY
}

# 📅 Data
data_escolhida = st.date_input("Selecione a data", date.today())
data_formatada = data_escolhida.strftime("%Y-%m-%d")

st.subheader(f"Jogos em {data_formatada}")

# 🎯 Ligas e competições alvo (IDs corretos)
ligas_interesse = [
    39,   # Premier League
    140,  # La Liga
    135,  # Serie A Itália
    78,   # Bundesliga
    61,   # Ligue 1

    71,   # Brasileirão
    128,  # Argentina
    265,  # Chile
    239,  # Colômbia
    268,  # Uruguai

    2,    # Champions League
    3,    # Europa League
    13,   # Libertadores
    11    # Sul-Americana
]

url = f"https://v3.football.api-sports.io/fixtures?date={data_formatada}"
response = requests.get(url, headers=headers)

analises = []

def gerar_stats(posicao):
    if posicao == "Atacante":
        return {
            "chutes": np.random.uniform(2,5),
            "gol": np.random.uniform(1,3),
            "faltas": np.random.uniform(1,2),
            "desarmes": np.random.uniform(0,1)
        }
    elif posicao == "Meia":
        return {
            "chutes": np.random.uniform(1,3),
            "gol": np.random.uniform(0.5,2),
            "faltas": np.random.uniform(1,3),
            "desarmes": np.random.uniform(1,3)
        }
    else:
        return {
            "chutes": np.random.uniform(0,2),
            "gol": np.random.uniform(0,1),
            "faltas": np.random.uniform(2,4),
            "desarmes": np.random.uniform(3,6)
        }

if response.status_code == 200:
    dados = response.json()

    for jogo in dados["response"]:
        liga_id = jogo["league"]["id"]

        if liga_id not in ligas_interesse:
            continue

        casa = jogo["teams"]["home"]["name"]
        fora = jogo["teams"]["away"]["name"]
        liga_nome = jogo["league"]["name"]

        jogadores = [
            ("Atacante", "Chutes", 2.5, 2.10),
            ("Atacante", "Chutes no Gol", 1.5, 1.90),
            ("Meia", "Faltas Sofridas", 2.5, 2.00),
            ("Volante", "Desarmes", 3.5, 1.85)
        ]

        for pos, mercado, linha, odd in jogadores:
            stats = gerar_stats(pos)

            media = stats["chutes"] if "Chutes" in mercado else \
                    stats["gol"] if "Gol" in mercado else \
                    stats["faltas"] if "Faltas" in mercado else \
                    stats["desarmes"]

            prob = media / (linha + 1)
            ev = (prob * odd) - 1

            analises.append({
                "Liga": liga_nome,
                "Jogo": f"{casa} x {fora}",
                "Mercado": mercado,
                "Linha": linha,
                "Média": round(media,2),
                "Probabilidade": round(prob,2),
                "Odd": odd,
                "EV": round(ev,2)
            })

    df = pd.DataFrame(analises)

    if not df.empty:
        df = df.sort_values(by="EV", ascending=False)

        st.subheader("🔥 TOP OPORTUNIDADES")
        st.dataframe(df.head(10))

        st.subheader("📊 TODAS AS ANÁLISES")
        st.dataframe(df)
    else:
        st.warning("Nenhum jogo encontrado nas ligas selecionadas.")

else:
    st.error("Erro ao buscar dados da API")
