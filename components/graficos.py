import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def plotar_graficos(dados_pontos, populacao_prevista):
    # Gráfico 1: População atual por ponto de coleta (linha)
    st.subheader("Gráfico 1 - População Atual por Ponto de Coleta")
    df_atual = pd.DataFrame(dados_pontos)
    fig1, ax1 = plt.subplots()
    ax1.plot(df_atual["ponto"], df_atual["adultos"], marker='o', label="Adultos")
    ax1.plot(df_atual["ponto"], df_atual["ninfas"], marker='o', label="Ninfas")
    ax1.set_title("População Atual da Cigarrinha-do-Milho")
    ax1.set_xlabel("Ponto de Coleta")
    ax1.set_ylabel("Número de Insetos")
    ax1.legend()
    st.pyplot(fig1)

    # Gráfico 2: Previsão Populacional
    st.subheader("Gráfico 2 - Previsão Populacional para os Próximos Dias")
    dias = [datetime.today() + timedelta(days=i) for i in range(len(populacao_prevista))]
    fig2, ax2 = plt.subplots()
    ax2.plot(dias, populacao_prevista, color='blue')
    ax2.set_title("Previsão Populacional da Cigarrinha-do-Milho")
    ax2.set_xlabel("Data")
    ax2.set_ylabel("População Estimada")
    fig2.autofmt_xdate(rotation=30)
    st.pyplot(fig2)

    # Gráfico 3: Comparativo atual vs. pico previsto
    st.subheader("Gráfico 3 - Comparativo Atual vs. Pico Previsto")
    pop_atual = sum([p["adultos"] + p["ninfas"] for p in dados_pontos])
    pico = max(populacao_prevista)
    data_pico = dias[populacao_prevista.index(pico)].strftime("%d/%m/%Y")
    fig3, ax3 = plt.subplots()
    ax3.bar(["População Atual", f"Pico Previsto
({data_pico})"], [pop_atual, pico], color=["red", "green"])
    ax3.set_title("Comparativo da Infestação")
    ax3.set_ylabel("População")
    st.pyplot(fig3)
