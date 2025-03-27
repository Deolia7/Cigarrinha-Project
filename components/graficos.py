#import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plotar_graficos(dados_pontos, populacao_prevista):
    st.markdown("### Gráfico 1 - População Atual por Ponto de Coleta")
    df_atual = pd.DataFrame(dados_pontos)
    df_atual_grouped = df_atual.groupby('ponto').sum()

    fig1, ax1 = plt.subplots()
    df_atual_grouped[['adultos', 'ninfas']].plot(kind='bar', stacked=True, ax=ax1, color=['#1f77b4', '#ff7f0e'])
    ax1.set_ylabel("Número de Insetos")
    ax1.set_title("População Atual da Cigarrinha-do-Milho")
    ax1.legend(["Adultos", "Ninfas"])
    st.pyplot(fig1)

    st.markdown("### Gráfico 2 - Previsão Populacional para os Próximos Dias")
    if isinstance(populacao_prevista, list) and len(populacao_prevista) > 0:
        df_prev = pd.DataFrame(populacao_prevista)
        df_prev['data'] = pd.to_datetime(df_prev['data'])
        fig2, ax2 = plt.subplots()
        ax2.plot(df_prev['data'], df_prev['pop'], color='blue')
        ax2.set_xlabel("Data")
        ax2.set_ylabel("População Estimada")
        ax2.set_title("Previsão da População da Cigarrinha-do-Milho")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

        st.markdown("### Gráfico 3 - Comparativo Atual vs. Pico Previsto")
        pop_atual = df_atual_grouped[['adultos', 'ninfas']].sum().sum()
        pop_pico = df_prev['pop'].max()
        pico_data = df_prev[df_prev['pop'] == pop_pico]['data'].dt.strftime('%d/%m/%Y').values[0]

        fig3, ax3 = plt.subplots()
        ax3.bar(['Atual'], [pop_atual], color='green')
        ax3.bar(['Pico Previsto'], [pop_pico], color='red')
        ax3.set_ylabel("População")
        ax3.set_title("Comparativo da Infestação")
        ax3.text(0.5, pop_pico + 0.5, f"Pico em {pico_data}", ha='center')
        st.pyplot(fig3)
