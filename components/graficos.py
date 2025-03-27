import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def plotar_graficos(dados_pontos, populacao_prevista):
    st.subheader("📊 Gráfico 1 - População Atual por Ponto de Coleta")
    df_atual = pd.DataFrame(dados_pontos)
    fig1, ax1 = plt.subplots()
    ax1.plot(df_atual["ponto"], df_atual["adultos"], marker='o', label="Adultos")
    ax1.plot(df_atual["ponto"], df_atual["ninfas"], marker='o', label="Ninfas")
    ax1.set_title("População Atual da Cigarrinha-do-Milho")
    ax1.set_xlabel("Ponto de Coleta")
    ax1.set_ylabel("Número de Insetos")
    ax1.legend()
    st.pyplot(fig1)

    st.subheader("📈 Gráfico 2 - Previsão Populacional para os Próximos Dias")
    dias = [datetime.today() + timedelta(days=i) for i in range(len(populacao_prevista))]
    fig2, ax2 = plt.subplots()
    ax2.plot(dias, populacao_prevista, color='blue')
    ax2.set_title("Previsão Populacional da Cigarrinha-do-Milho")
    ax2.set_xlabel("Data")
    ax2.set_ylabel("População Estimada")
    fig2.autofmt_xdate(rotation=30)
    st.pyplot(fig2)

    st.subheader("📉 Gráfico 3 - Comparativo Atual vs. Pico Previsto")
    pop_atual = sum(p["adultos"] + p["ninfas"] for p in dados_pontos)
    pico = max(populacao_prevista)
    data_pico = dias[populacao_prevista.index(pico)].strftime("%d/%m/%Y")
    fig3, ax3 = plt.subplots()
    ax3.bar(["População Atual", f"Pico Previsto\n({data_pico})"], [pop_atual, pico], color=["red", "green"])
    ax3.set_title("Comparativo da Infestação")
    ax3.set_ylabel("População")
    st.pyplot(fig3)


def plotar_comparativo_historico(historico):
    st.subheader("📊 Gráfico 4 - Comparativo Histórico (População Real x Prevista)")
    if not historico:
        st.warning("Nenhuma avaliação anterior para comparar.")
        return

    try:
        datas = [datetime.strptime(a["data"], "%Y-%m-%d") for a in historico]
        reais = [a["media_real_adultos"] for a in historico]
        previstos = [max(a["populacao_prevista"]) for a in historico]

        fig, ax = plt.subplots()
        ax.plot(datas, reais, label="População Real", marker="o")
        ax.plot(datas, previstos, label="População Prevista", marker="x")
        ax.set_title("Comparativo População Real x Prevista")
        ax.set_xlabel("Data")
        ax.set_ylabel("População")
        ax.legend()
        fig.autofmt_xdate(rotation=30)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao gerar gráfico comparativo: {e}")
