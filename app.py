
import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from components.graficos import plotar_graficos
from components.relatorio_pdf import gerar_relatorio_pdf
from models.predicao_populacional import prever_populacao
from utils.api_weather import obter_clima
from utils.recomendacoes import gerar_recomendacoes

# Criar diretório para armazenar histórico
if not os.path.exists("avaliacoes_salvas"):
    os.makedirs("avaliacoes_salvas")

st.set_page_config(layout="wide")
st.title("📊 Monitoramento da Cigarrinha-do-Milho")

# Entrada de dados
st.sidebar.header("📍 Identificação da Avaliação")
fazenda = st.sidebar.text_input("Nome da Fazenda")
talhao = st.sidebar.text_input("Nome do Talhão")
data_avaliacao = st.sidebar.date_input("Data da Avaliação", value=datetime.today())
localizacao = st.sidebar.text_input("Cidade ou Coordenadas")

st.sidebar.header("📷 Foto do Talhão")
foto_talhao = st.sidebar.file_uploader("Envie uma foto do talhão", type=["jpg", "jpeg", "png"])

st.sidebar.header("🦟 Pontos de Coleta")
num_pontos = st.sidebar.slider("Número de pontos", 3, 5, 3)

dados_pontos = []
for i in range(num_pontos):
    st.sidebar.markdown(f"### Ponto {i+1}")
    adultos = st.sidebar.number_input(f"Adultos no ponto {i+1}", 0, 100, 0, key=f"adultos_{i}")
    ninfas = st.sidebar.number_input(f"Ninfas no ponto {i+1}", 0, 100, 0, key=f"ninfas_{i}")
    dados_pontos.append({"ponto": f"P{i+1}", "adultos": adultos, "ninfas": ninfas})

if st.button("🚀 Gerar Análise"):
    if not localizacao.strip():
        st.error("Por favor, preencha a cidade ou coordenadas.")
    else:
        try:
            clima = obter_clima(localizacao)
        except Exception as e:
            st.error(f"Erro ao obter dados climáticos: {e}")
            clima = None

        pop_prevista = prever_populacao(clima)
        plotar_graficos(dados_pontos, pop_prevista)

        recomendacoes = gerar_recomendacoes(dados_pontos, pop_prevista)
        st.success("Análise concluída.")
        st.markdown("### 🧪 Recomendações Técnicas")
        st.markdown(recomendacoes)

        # Calcular média real
        media_real = sum(p["adultos"] + p["ninfas"] for p in dados_pontos) / len(dados_pontos)

        # Salvar histórico
        chave_talhao = f"{fazenda}_{talhao}".replace(" ", "_")
        historico_path = f"avaliacoes_salvas/{chave_talhao}.json"
        historico = []

        if os.path.exists(historico_path):
            with open(historico_path, "r") as f:
                historico = json.load(f)

        historico.append({
            "data": data_avaliacao.strftime("%Y-%m-%d"),
            "pop_real": round(media_real, 1),
            "pop_prevista": round(pop_prevista[0], 1)
        })

        with open(historico_path, "w") as f:
            json.dump(historico, f, indent=2)

        # Exibir histórico
        st.markdown("### 🗂️ Histórico de Avaliações")
        df_hist = pd.DataFrame(historico)
        st.dataframe(df_hist)

        # Baixar CSV
        csv = df_hist.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar histórico em CSV", csv, "historico.csv", "text/csv")

        # Gerar relatório em PDF
        pdf_file = gerar_relatorio_pdf(dados_pontos, pop_prevista, recomendacoes, foto_talhao, historico)
        st.download_button("📄 Baixar Relatório em PDF", pdf_file, file_name="relatorio_cigarrinha.pdf")
