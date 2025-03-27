import streamlit as st
from components.graficos import plotar_graficos
from components.relatorio_pdf import gerar_relatorio_pdf
from utils.clima import obter_dados_climaticos
from utils.previsao_modelo import prever_populacao
from utils.recomendacoes import gerar_recomendacoes
import pandas as pd
from PIL import Image
import datetime

st.title("Monitoramento da Cigarrinha-do-Milho")

st.markdown("### Localização")
local_input = st.text_input("Digite a cidade ou coordenadas (ex: -17.83, -51.76):")

if local_input:
    try:
        clima = obter_dados_climaticos(local_input)
    except Exception as e:
        st.error(f"Erro ao obter dados climáticos: {e}")
        st.stop()

    st.markdown("### Avaliação por Ponto de Coleta")
    dados_pontos = []
    for i in range(1, 4):
        adultos = st.number_input(f"Nº de Adultos - Ponto {i}", min_value=0, step=1)
        ninfas = st.number_input(f"Nº de Ninfas - Ponto {i}", min_value=0, step=1)
        dados_pontos.append({"ponto": f"Ponto {i}", "adultos": adultos, "ninfas": ninfas})

    st.markdown("### 📸 Enviar Fotos do Talhão")
    fotos = st.file_uploader("Envie até 2 fotos do talhão", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

    if st.button("Gerar Análise"):
        populacao_prevista = prever_populacao(dados_pontos, clima)
        recomendacoes = gerar_recomendacoes(dados_pontos, populacao_prevista)

        st.markdown("### 📊 Gráficos")
        fig1, fig2, fig3 = plotar_graficos(dados_pontos, populacao_prevista)
        st.pyplot(fig1)
        st.pyplot(fig2)
        st.pyplot(fig3)

        st.markdown("### ✅ Recomendações Técnicas")
        for r in recomendacoes:
            st.markdown(f"- {r}")

        st.markdown("### 📄 Relatório Final")
        buffer = gerar_relatorio_pdf(dados_pontos, populacao_prevista, recomendacoes, fotos)
        st.download_button(label="📥 Baixar Relatório em PDF", data=buffer, file_name="relatorio.pdf")