
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def plotar_graficos(dados_pontos, df_prev):
    # Gráfico 1: Evolução atual da população
    pontos = [p["ponto"] for p in dados_pontos]
    adultos = [p["adultos"] for p in dados_pontos]
    ninfas = [p["ninfas"] for p in dados_pontos]

    st.subheader("Gráfico 1 - População Atual por Ponto de Coleta")
    fig1, ax1 = plt.subplots()
    ax1.bar(pontos, adultos, label="Adultos")
    ax1.bar(pontos, ninfas, bottom=adultos, label="Ninfas")
    ax1.set_xlabel("Ponto de Coleta")
    ax1.set_ylabel("Número de Insetos")
    ax1.set_title("População Atual da Cigarrinha-do-Milho")
    ax1.legend()
    st.pyplot(fig1)

    # Gráfico 2: Previsão populacional
    st.subheader("Gráfico 2 - Previsão Populacional (Próximos 30 dias)")
    fig2, ax2 = plt.subplots()
    ax2.plot(df_prev["dia"], df_prev["populacao_prevista"], color="blue")
    ax2.set_xlabel("Data")
    ax2.set_ylabel("População Estimada")
    ax2.set_title("Projeção de População da Cigarrinha")
    st.pyplot(fig2)

    # Gráfico 3: Comparativo atual vs pico previsto
    st.subheader("Gráfico 3 - Comparativo Atual vs. Pico Previsto")
    fig3, ax3 = plt.subplots()
    media_atual = sum(adultos) + sum(ninfas)
    pico = df_prev["populacao_prevista"].max()
    ax3.bar(["Atual", "Pico Previsto"], [media_atual, pico], color=["green", "red"])
    ax3.set_ylabel("População")
    ax3.set_title("Comparativo da Infestação")
    st.pyplot(fig3)
