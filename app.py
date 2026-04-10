import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(page_title="Análise de Apostas - Futebol", layout="wide")

st.title("⚽ Scanner de Apostas de Valor (EV+)")

# Seleção de data
data_escolhida = st.date_input("Selecione a data", date.today())

st.subheader(f"Jogos do dia: {data_escolhida}")

# Dados simulados (vamos conectar API depois)
data = {
    "Jogador": ["João Silva", "Pedro Santos", "Lucas Lima", "Carlos Souza"],
    "Time": ["Flamengo", "Palmeiras", "Santos", "Grêmio"],
    "Adversário": ["Vasco", "Corinthians", "SPFC", "Inter"],
    "Mercado": ["Chutes", "Chutes no Gol", "Faltas Sofridas", "Desarmes"],
    "Linha": [2.5, 1.5, 2.5, 3.5],
    "Media": [3.2, 2.1, 3.0, 4.2],
    "Odd": [2.20, 1.80, 2.00, 1.90],
    "Mando": ["Casa", "Fora", "Casa", "Fora"]
}

df = pd.DataFrame(data)

# Ajuste simples de mando de campo
def ajuste_mando(row):
    if row["Mando"] == "Casa":
        return row["Media"] * 1.1
    else:
        return row["Media"] * 0.9

df["Media_Ajustada"] = df.apply(ajuste_mando, axis=1)

# Probabilidade simples (simulação)
df["Prob_Modelo"] = df["Media_Ajustada"] / (df["Linha"] + 1)

# Probabilidade implícita
df["Prob_Implicita"] = 1 / df["Odd"]

# EV (valor esperado)
df["EV"] = (df["Prob_Modelo"] * df["Odd"]) - 1

# Ranking
df = df.sort_values(by="EV", ascending=False)

# Destaques
st.subheader("🔥 Melhores oportunidades do dia")
top = df.head(5)

st.dataframe(top)

st.subheader("📊 Todas as análises")
st.dataframe(df)
