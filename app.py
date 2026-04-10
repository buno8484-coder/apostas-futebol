import streamlit as st
import pandas as pd
import requests
from datetime import date

st.set_page_config(page_title="Scanner de Apostas", layout="wide")

st.title("⚽ Scanner de Apostas (Dados Reais)")

# 🔑 SUA API KEY (cole a sua aqui)
API_KEY = "a210552d9ca862c4801da1d9a589ceb7"

headers = {
    "x-apisports-key": API_KEY
}

# 📅 Seleção de data
data_escolhida = st.date_input("Selecione a data", date.today())
data_formatada = data_escolhida.strftime("%Y-%m-%d")

st.subheader(f"Jogos em {data_formatada}")

# 🌍 Buscar jogos do dia
url = f"https://v3.football.api-sports.io/fixtures?date={data_formatada}"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    
    jogos = []

    for jogo in dados["response"]:
        liga = jogo["league"]["name"]
        time_casa = jogo["teams"]["home"]["name"]
        time_fora = jogo["teams"]["away"]["name"]
        horario = jogo["fixture"]["date"]

        jogos.append({
            "Liga": liga,
            "Jogo": f"{time_casa} x {time_fora}",
            "Horário": horario
        })

    df_jogos = pd.DataFrame(jogos)

    st.dataframe(df_jogos)

else:
    st.error("Erro ao buscar dados da API")

st.info("Próximo passo: integrar estatísticas dos jogadores + cálculo de EV")
