import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def plotar_graficos(dados_pontos, populacao_prevista):
    st.subheader("📊 Gráfico 1 - População Atual por Ponto de Coleta")

    df_atual = pd.DataFrame(dados_pontos)

    # Verifica se os dados estão presentes
    if "ponto" in df_atual.columns and "adultos" in df_atual.columns and "ninfas" in df_atual.columns:
        fig1, ax1 = plt.subplots()
        ax1.plot(df_atual["ponto"], df_atual["adultos"], marker='o', label="Adultos", color='blue')
        ax1.plot(df_atual["ponto"], df_atual["ninfas"], marker='o', label="Ninfas", color='orange')
        ax1.set_title("População Atual da Cigarrinha-do-Milho")
        ax1.set_xlabel("Ponto de Coleta")
        ax1.set_ylabel("Número de Insetos")
        ax1.legend()
        st.pyplot(fig1)
    else:
        st.warning("❗ Dados insuficientes para exibir o gráfico de população atual.")

    st.subheader("📈 Gráfico 2 - Previsão Populacional para os Próximos Dias")

    if populacao_prevista:
        dias = [datetime.today() + timedelta(days=i) for i in range(len(populacao_prevista))]
        fig2, ax2 = plt.subplots()
        ax2.plot(dias, populacao_prevista, color='green')
        ax2.set_title("Previsão Populacional da Cigarrinha-do-Milho")
        ax2.set_xlabel("Data")
        ax2.set_ylabel("População Estimada")
        fig2.autofmt_xdate(rotation=30)
        st.pyplot(fig2)
    else:
        st.warning("❗ Sem dados disponíveis para previsão populacional.")

    st.subheader("📊 Gráfico 3 - Comparativo Atual vs. Pico Previsto")

    try:
        pop_atual = sum(p["adultos"] + p["ninfas"] for p in dados_pontos)
        pico = max(populacao_prevista)
        dias = [datetime.today() + timedelta(days=i) for i in range(len(populacao_prevista))]
        data_pico = dias[populacao_prevista.index(pico)].strftime("%d/%m/%Y")
        fig3, ax3 = plt.subplots()
        ax3.bar(["População Atual", f"Pico Previsto\n({data_pico})"], [pop_atual, pico], color=["red", "green"])
        ax3.set_title("Comparativo da Infestação")
        ax3.set_ylabel("População")
        st.pyplot(fig3)
    except Exception as e:
        st.warning(f"❗ Erro ao gerar gráfico comparativo: {e}")
