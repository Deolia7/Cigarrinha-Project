import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from utils.api_weather import obter_clima
from utils.recomendacoes import gerar_recomendacoes
from models.predicao_populacional import prever_populacao
from components.graficos import plotar_graficos, plotar_historico
from components.relatorio_pdf import gerar_relatorio_pdf

st.set_page_config(layout="wide")
st.title("📊 Monitoramento da Cigarrinha-do-Milho")

# Diretórios para salvar os dados
os.makedirs("avaliacoes_salvas", exist_ok=True)
os.makedirs("imagens", exist_ok=True)

# Funções auxiliares
def carregar_dados(talhao):
    caminho = f"avaliacoes_salvas/{talhao}.json"
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            return json.load(f)
    return []

def salvar_dados(talhao, dados):
    with open(f"avaliacoes_salvas/{talhao}.json", "w") as f:
        json.dump(dados, f, indent=4)

# Entrada de dados
with st.sidebar:
    st.header("🧾 Cadastro da Avaliação")
    fazenda = st.text_input("Nome da Fazenda")
    talhao = st.text_input("Nome do Talhão")
    data = st.date_input("Data da Avaliação", datetime.today())
    pontos = st.number_input("Número de Pontos de Coleta", min_value=3, max_value=10, value=3)

    dados_pontos = []
    for i in range(pontos):
        adultos = st.number_input(f"Ponto {i+1} - Adultos", min_value=0, key=f"a_{i}")
        ninfas = st.number_input(f"Ponto {i+1} - Ninfas", min_value=0, key=f"n_{i}")
        dados_pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

    imagem = st.file_uploader("📷 Foto do Talhão", type=["jpg", "png", "jpeg"])

    localizacao = st.text_input("Cidade ou coordenadas do talhão")
    clima = None
    if localizacao:
        try:
            clima = obter_clima(localizacao)
        except Exception as e:
            st.error(f"Erro ao obter dados climáticos: {e}")
    else:
        st.warning("Digite a cidade ou coordenadas para obter os dados climáticos.")

    if st.button("📈 Gerar Análise"):
        if not fazenda or not talhao:
            st.warning("Preencha os campos de Fazenda e Talhão.")
        else:
            # Previsão e Recomendação
            populacao_prevista = prever_populacao(dados_pontos, clima)
            recomendacoes = gerar_recomendacoes(dados_pontos, populacao_prevista)

            # Salvar imagem
            caminho_imagem = None
            if imagem:
                nome_imagem = f"imagens/{talhao}_{data}.jpg"
                with open(nome_imagem, "wb") as f:
                    f.write(imagem.getbuffer())
                caminho_imagem = nome_imagem

            # Salvar avaliação
            nova_avaliacao = {
                "data": str(data),
                "pontos": dados_pontos,
                "populacao_prevista": populacao_prevista,
                "imagem": caminho_imagem
            }
            historico = carregar_dados(talhao)
            historico.append(nova_avaliacao)
            salvar_dados(talhao, historico)

            st.success("Análise concluída.")
            st.markdown("## 📌 Recomendações Técnicas")
            st.markdown(recomendacoes)

            # Gerar PDF
            pdf_file = gerar_relatorio_pdf(fazenda, talhao, nova_avaliacao, recomendacoes, historico)
            st.download_button("📄 Baixar Relatório PDF", data=pdf_file, file_name="relatorio.pdf")

            # Gráficos
            plotar_graficos(dados_pontos, populacao_prevista)
            plotar_historico(historico)

            # Tabela CSV
            df = pd.DataFrame([{
                "Data": a["data"],
                "População Real (média)": sum(p["adultos"] + p["ninfas"] for p in a["pontos"]) / len(a["pontos"]),
                "População Prevista (modelo)": a["populacao_prevista"][0]
            } for a in historico])
            st.subheader("📋 Histórico de Avaliações")
            st.dataframe(df)
            st.download_button("⬇️ Baixar histórico em CSV", data=df.to_csv(index=False), file_name="historico.csv", mime="text/csv")