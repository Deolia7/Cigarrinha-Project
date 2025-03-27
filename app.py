import streamlit as st
import os
import json
from datetime import datetime
from components.graficos import plotar_graficos
from components.relatorio_pdf import gerar_relatorio_pdf
from utils.api_weather import obter_clima
from utils.recomendacoes import gerar_recomendacoes
from models.predicao_populacional import prever_populacao

# Diretório para salvar avaliações
DIRETORIO_AVALIACOES = "avaliacoes_salvas"
os.makedirs(DIRETORIO_AVALIACOES, exist_ok=True)

st.set_page_config(layout="wide")
st.title("📊 Monitoramento da Cigarrinha-do-Milho")

# Seções de entrada
with st.sidebar:
    st.header("🧭 Dados de Entrada")
    fazenda = st.text_input("Nome da Fazenda")
    talhao = st.text_input("Nome do Talhão")

    localizacao = st.text_input("Cidade ou Coordenadas (ex: '18°23'26.8\"S 52°38'08.3\"W')")
    data_avaliacao = st.date_input("Data da Avaliação", datetime.today())
    pontos = st.number_input("Número de Pontos de Coleta", min_value=3, max_value=10, value=3)

    dados_pontos = []
    for i in range(pontos):
        st.subheader(f"Ponto {i+1}")
        adultos = st.number_input(f"Adultos (Ponto {i+1})", min_value=0, key=f"a{i}")
        ninfas = st.number_input(f"Ninfas (Ponto {i+1})", min_value=0, key=f"n{i}")
        dados_pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

    imagem = st.file_uploader("📷 Foto do Talhão (opcional)", type=["png", "jpg", "jpeg"])
    gerar = st.button("🚀 Gerar Análises")

if gerar:
    if not fazenda or not talhao or not localizacao:
        st.error("❌ Por favor, preencha todos os campos obrigatórios (fazenda, talhão, localização).")
    else:
        try:
            clima = obter_clima(localizacao)
            populacao_prevista = prever_populacao(clima, dados_pontos)
            recomendacoes = gerar_recomendacoes(dados_pontos, populacao_prevista)

            # Calcular médias reais
            media_real_adultos = sum([p["adultos"] for p in dados_pontos]) / len(dados_pontos)
            media_real_ninfas = sum([p["ninfas"] for p in dados_pontos]) / len(dados_pontos)

            nova_avaliacao = {
                "data": str(data_avaliacao),
                "pontos": dados_pontos,
                "media_real_adultos": round(media_real_adultos, 2),
                "media_real_ninfas": round(media_real_ninfas, 2),
                "populacao_prevista": populacao_prevista
            }

            # Caminho do arquivo do talhão
            nome_arquivo = f"{fazenda}_{talhao}.json".replace(" ", "_").lower()
            caminho_arquivo = os.path.join(DIRETORIO_AVALIACOES, nome_arquivo)

            historico = []
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r") as f:
                    historico = json.load(f)

            historico.append(nova_avaliacao)

            with open(caminho_arquivo, "w") as f:
                json.dump(historico, f, indent=4)

            # Gerar relatórios
            st.success("✅ Análise concluída.")
            plotar_graficos(dados_pontos, populacao_prevista, historico)

            st.subheader("📋 Histórico de Avaliações")
            import pandas as pd
            df_hist = pd.DataFrame([
                {
                    "Data": a["data"],
                    "População Real (média)": a["media_real_adultos"],
                    "População Prevista (modelo)": max(a["populacao_prevista"])
                }
                for a in historico
            ])
            st.dataframe(df_hist)

            st.download_button("📥 Baixar histórico em CSV", data=df_hist.to_csv(index=False), file_name="historico.csv")

            st.subheader("🧠 Recomendação Técnica")
            st.markdown(recomendacoes)

            # Gerar relatório final em PDF
            pdf_file = gerar_relatorio_pdf(fazenda, talhao, nova_avaliacao, recomendacoes, historico, imagem)
            st.download_button("📄 Baixar Relatório em PDF", data=pdf_file, file_name="relatorio.pdf")

        except Exception as e:
            st.error(f"Erro ao processar a análise: {e}")
