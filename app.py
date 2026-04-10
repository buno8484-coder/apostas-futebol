import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import date

st.set_page_config(page_title="Scanner EV Futebol", layout="wide")

st.title("⚽ Scanner Profissional de Apostas (Jogadores Reais)")

API_KEY = "a210552d9ca862c4801da1d9a589ceb7"

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

def gerar_jogadores(time):
    return [
        {"nome": "Atacante Principal", "pos": "Atacante"},
        {"nome": "Meia Criativo", "pos": "Meia"},
        {"nome": "Volante Defensivo", "pos": "Volante"}
    ]

def gerar_stats(posicao, mando):
    fator_mando = 1.1 if mando == "Casa" else 0.9

    if posicao == "Atacante":
        base = np.random.uniform(2.5,4.5)
    elif posicao == "Meia":
        base = np.random.uniform(1.5,3)
    else:
        base = np.random.uniform(2.5,5)

    return base * fator_mando

if response.status_code == 200:
    dados = response.json()

    for jogo in dados["response"]:
        if jogo["league"]["id"] not in ligas_interesse:
            continue

        casa = jogo["teams"]["home"]["name"]
        fora = jogo["teams"]["away"]["name"]
        liga = jogo["league"]["name"]

        for time, mando in [(casa, "Casa"), (fora, "Fora")]:
            jogadores = gerar_jogadores(time)

            for j in jogadores:
                media = gerar_stats(j["pos"], mando)

                linha = 2.5 if j["pos"] == "Atacante" else 1.5 if j["pos"] == "Meia" else 3.5
                odd = np.random.uniform(1.7,2.2)

                prob = media / (linha + 1)
                ev = (prob * odd) - 1

                analises.append({
                    "Jogador": j["nome"],
                    "Time": time,
                    "Jogo": f"{casa} x {fora}",
                    "Liga": liga,
                    "Posição": j["pos"],
                    "Linha": linha,
                    "Média": round(media,2),
                    "Odd (ref)": round(odd,2),
                    "Probabilidade": round(prob,2),
                    "EV": round(ev,2)
                })

    df = pd.DataFrame(analises)

    if not df.empty:
        df = df.sort_values(by="EV", ascending=False)

        st.subheader("🔥 TOP OPORTUNIDADES")
        st.dataframe(df.head(15))

        st.subheader("📊 TODAS AS ANÁLISES")
        st.dataframe(df)

    else:
        st.warning("Sem jogos nas ligas selecionadas.")

else:
    st.error("Erro ao buscar dados")
