import streamlit as st
import os
import json
from datetime import datetime
from components.graficos import plotar_graficos, plotar_comparativo_historico
from components.relatorio_pdf import gerar_relatorio_pdf
from models.predicao_populacional import prever_populacao
from utils.api_weather import obter_clima
from utils.recomendacoes import gerar_recomendacoes

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-Milho", page_icon="📊", layout="wide")

st.title("📊 Monitoramento da Cigarrinha-do-Milho")

# Pastas
PASTA_AVALIACOES = "avaliacoes_salvas"
PASTA_IMAGENS = "imagens"

os.makedirs(PASTA_AVALIACOES, exist_ok=True)
os.makedirs(PASTA_IMAGENS, exist_ok=True)

# Entradas
st.sidebar.header("📍 Identificação do Talhão")
fazenda = st.sidebar.text_input("Nome da Fazenda")
talhao = st.sidebar.text_input("Nome do Talhão")

num_pontos = st.sidebar.slider("Número de Pontos de Amostragem", 3, 5, 3)

st.sidebar.markdown("---")
st.sidebar.header("📅 Data e Local")
data_avaliacao = st.sidebar.date_input("Data da Avaliação", value=datetime.today())
localizacao = st.sidebar.text_input("Cidade ou Coordenadas")

# Dados de campo
st.header("📋 Dados de Campo")
dados_pontos = []
for i in range(num_pontos):
    col1, col2 = st.columns(2)
    with col1:
        adultos = st.number_input(f"Ponto {i+1} - Adultos", min_value=0, key=f"adultos_{i}")
    with col2:
        ninfas = st.number_input(f"Ponto {i+1} - Ninfas", min_value=0, key=f"ninfas_{i}")
    dados_pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

# Foto
st.subheader("📸 Foto do Talhão (opcional)")
foto = st.file_uploader("Envie uma imagem do talhão", type=["png", "jpg", "jpeg"])

# Botão de análise
gerar = st.button("📈 Gerar Análise")

if gerar:
    try:
        with st.spinner("🔍 Processando dados..."):
            clima = obter_clima(localizacao)
            st.success("📡 Dados climáticos brutos")
            st.json(clima)

            populacao_prevista = prever_populacao(clima)
            plotar_graficos(dados_pontos, populacao_prevista)

            recomendacoes = gerar_recomendacoes(dados_pontos, populacao_prevista)
            st.subheader("📢 Recomendações Técnicas")
            st.markdown(recomendacoes)

            # Salvar avaliação
            historico_path = os.path.join(PASTA_AVALIACOES, f"{fazenda}_{talhao}.json")
            if os.path.exists(historico_path):
                with open(historico_path, "r") as f:
                    historico = json.load(f)
                    if isinstance(historico, list) and isinstance(historico[0], str):
                        historico = [json.loads(h) for h in historico]
            else:
                historico = []

            media_real = sum(p["adultos"] + p["ninfas"] for p in dados_pontos) / len(dados_pontos)

            nova_avaliacao = {
                "data": data_avaliacao.strftime("%Y-%m-%d"),
                "media_real_adultos": media_real,
                "media_adultos": sum(p["adultos"] for p in dados_pontos) / len(dados_pontos),
                "media_ninfas": sum(p["ninfas"] for p in dados_pontos) / len(dados_pontos),
                "populacao_prevista": populacao_prevista
            }

            if foto:
                nome_arquivo = f"{fazenda}_{talhao}_{data_avaliacao.strftime('%Y%m%d')}.jpg"
                caminho_foto = os.path.join(PASTA_IMAGENS, nome_arquivo)
                with open(caminho_foto, "wb") as f:
                    f.write(foto.read())
                nova_avaliacao["imagem"] = caminho_foto

            historico.append(nova_avaliacao)

            with open(historico_path, "w") as f:
                json.dump(historico, f, indent=2)

            # Gráfico comparativo real vs previsto
            plotar_comparativo_historico(historico)

            # Tabela de histórico
            st.subheader("📑 Histórico de Avaliações")
            df_hist = json.loads(json.dumps([
                {
                    "Data": a["data"],
                    "População Real (média)": a["media_real_adultos"],
                    "População Prevista (modelo)": max(a["populacao_prevista"])
                }
                for a in historico
            ]))
            st.dataframe(df_hist)

            # Download do CSV
            csv_path = os.path.join(PASTA_AVALIACOES, f"{fazenda}_{talhao}_historico.csv")
            df_export = json.loads(json.dumps([
                {
                    "Data": a["data"],
                    "População Real (média)": a["media_real_adultos"],
                    "População Prevista (modelo)": max(a["populacao_prevista"])
                }
                for a in historico
            ]))
            df_csv = df_export if isinstance(df_export, list) else []
            if df_csv:
                import pandas as pd
                df = pd.DataFrame(df_csv)
                df.to_csv(csv_path, index=False)
                with open(csv_path, "rb") as f:
                    st.download_button("📥 Baixar histórico em CSV", f, file_name=os.path.basename(csv_path))

            # PDF
            pdf_file = gerar_relatorio_pdf(fazenda, talhao, nova_avaliacao, recomendacoes, historico)
            st.download_button(label="📄 Baixar Relatório em PDF", data=pdf_file, file_name="relatorio_cigarrinha.pdf")

    except Exception as e:
        st.error(f"Erro ao processar a análise: {e}")
