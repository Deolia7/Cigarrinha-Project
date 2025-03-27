import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image

from utils.api_weather import obter_dados_climaticos
from utils.recomendacoes import gerar_recomendacoes
from models.predicao_populacional import prever_populacao
from components.graficos import (
    plotar_grafico_populacional,
    plotar_grafico_predicao,
    plotar_grafico_comparativo
)
from components.relatorio_pdf import gerar_relatorio_pdf

# Garantir que a pasta de avaliações esteja criada
os.makedirs("avaliacoes_salvas", exist_ok=True)

# Configuração da página
st.set_page_config(page_title="Monitoramento da Cigarrinha-do-Milho", layout="wide")
st.title("🌽 Monitoramento da Cigarrinha-do-Milho")

# Entrada de localização
st.subheader("🌎 Local da Avaliação")
local = st.text_input("Digite o nome da cidade ou coordenadas (ex: 18°23'26.8\"S 52°38'08.3\"W)", "")

# Obter dados climáticos
clima = {}
if local:
    try:
        clima = obter_dados_climaticos(local)
        with st.expander("📉 Dados climáticos brutos"):
            st.json(clima)
    except Exception as e:
        st.error(f"Erro ao obter dados climáticos: {e}")
else:
    st.warning("Por favor, preencha o campo de localização.")

# Cadastro da fazenda e talhão
st.subheader("🏡 Identificação")
fazenda = st.text_input("Nome da Fazenda")
talhao = st.text_input("Nome do Talhão")

# Data da avaliação
data_avaliacao = st.date_input("Data da Avaliação", value=datetime.today())

# Pontos de avaliação
st.subheader("📍 Avaliação da População")
dados_pontos = []
for i in range(1, 6):
    col1, col2 = st.columns(2)
    with col1:
        adultos = st.number_input(f"Nº de Adultos - Ponto {i}", min_value=0, step=1)
    with col2:
        ninfas = st.number_input(f"Nº de Ninfas - Ponto {i}", min_value=0, step=1)
    dados_pontos.append({"adultos": adultos, "ninfas": ninfas})

# Upload de imagem (opcional)
st.subheader("📷 Foto do Talhão (opcional)")
imagem = st.file_uploader("Envie uma imagem do talhão", type=["jpg", "jpeg", "png"])

# Botão de análise
if st.button("Gerar Análise"):
    try:
        # Previsão
        populacao_prevista = prever_populacao(clima, len(dados_pontos))

        # Recomendação
        recomendacoes = gerar_recomendacoes(dados_pontos, populacao_prevista)

        # População real média
        media_real = sum(p["adultos"] + p["ninfas"] for p in dados_pontos) / len(dados_pontos)

        # Nome do arquivo por talhão
        nome_talhao = f"{fazenda}_{talhao}".replace(" ", "_")
        caminho = f"avaliacoes_salvas/{nome_talhao}.csv"
        nova_linha = {
            "Data": str(data_avaliacao),
            "População Real (média)": round(media_real, 1),
            "População Prevista (modelo)": round(populacao_prevista[0], 1)
        }

        # Salvar histórico
        if os.path.exists(caminho):
            df_antigo = pd.read_csv(caminho)
            df_novo = pd.concat([df_antigo, pd.DataFrame([nova_linha])], ignore_index=True)
        else:
            df_novo = pd.DataFrame([nova_linha])
        df_novo.to_csv(caminho, index=False)

        # Exibir recomendação
        st.success("Análise concluída.")
        st.subheader("📌 Recomendações Técnicas")
        st.markdown(recomendacoes)

        # Gráficos
        st.subheader("📊 Evolução Populacional")
        st.pyplot(plotar_grafico_populacional(dados_pontos))

        st.subheader("📈 Previsão Populacional (30 dias)")
        st.pyplot(plotar_grafico_predicao(populacao_prevista))

        # Histórico
        st.subheader("📋 Histórico de Avaliações")
        st.dataframe(df_novo)
        st.download_button("📥 Baixar histórico em CSV", data=df_novo.to_csv(index=False), file_name="historico.csv")

        # Comparativo real vs previsto
        st.subheader("📉 Comparativo Real vs Modelo")
        st.pyplot(plotar_grafico_comparativo(df_novo))

        # Geração de PDF
        if st.button("📄 Baixar Relatório PDF"):
            pdf_file = gerar_relatorio_pdf(
                nome_fazenda=fazenda,
                nome_talhao=talhao,
                data=str(data_avaliacao),
                dados_pontos=dados_pontos,
                populacao_prevista=populacao_prevista,
                recomendacoes=recomendacoes,
                imagem=imagem,
                historico=df_novo
            )
            st.download_button("📄 Clique aqui para baixar o PDF", data=pdf_file, file_name="relatorio.pdf")

    except Exception as e:
        st.error(f"Ocorreu um erro durante a análise: {e}")
