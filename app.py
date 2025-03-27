import streamlit as st
from utils.api_weather import obter_dados_climaticos
from models.predicao_populacional import prever_populacao
from utils.recomendacoes import gerar_recomendacoes
from components.graficos import plotar_graficos
from components.relatorio_pdf import gerar_relatorio_pdf
import datetime
import os
import json

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-Milho", layout="wide")
st.title("Monitoramento da Cigarrinha-do-Milho")

def carregar_historico_avaliacoes(fazenda, talhao):
    pasta = "avaliacoes_salvas"
    historico = []
    if os.path.exists(pasta):
        for arquivo in os.listdir(pasta):
            if arquivo.endswith(".json") and f"{fazenda}_{talhao}" in arquivo:
                with open(os.path.join(pasta, arquivo), "r") as f:
                    historico.append(json.load(f))
    return historico

st.sidebar.header("Cadastro da Avaliação")
fazenda = st.sidebar.text_input("Nome da Fazenda")
talhao = st.sidebar.text_input("Nome do Talhão")
cidade = st.sidebar.text_input("Cidade ou Coordenadas (Google Maps format)")
data_avaliacao = st.sidebar.date_input("Data da Avaliação", value=datetime.date.today())

imagem = st.sidebar.file_uploader("Foto do Talhão (opcional)", type=["jpg", "png", "jpeg"])

st.sidebar.subheader("Dados de Campo")
num_pontos = st.sidebar.slider("Número de Pontos de Coleta", min_value=3, max_value=5, value=3)

dados_pontos = []
for i in range(num_pontos):
    st.sidebar.markdown(f"### Ponto {i+1}")
    adultos = st.sidebar.number_input(f"Nº de Adultos - Ponto {i+1}", min_value=0, step=1)
    ninfas = st.sidebar.number_input(f"Nº de Ninfas - Ponto {i+1}", min_value=0, step=1)
    dados_pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

if st.sidebar.button("Gerar Análise"):
    with st.spinner("Analisando dados..."):
        clima = obter_dados_climaticos(cidade)
        if "erro" in clima:
            st.error(f"Erro ao obter dados climáticos: {clima['erro']}")
            st.stop()

        st.expander("🔍 Dados climáticos brutos").write(clima)

        # Carrega histórico e calcula média
        historico = carregar_historico_avaliacoes(fazenda, talhao)
        historico.append({
            "data": str(data_avaliacao),
            "dados_pontos": dados_pontos
        })

        # Calcula médias históricas
        soma_adultos = [0] * num_pontos
        soma_ninfas = [0] * num_pontos
        total_avaliacoes = len(historico)

        for h in historico:
            for i, ponto in enumerate(h["dados_pontos"]):
                soma_adultos[i] += ponto["adultos"]
                soma_ninfas[i] += ponto["ninfas"]

        media_pontos = [{"ponto": i+1,
                         "adultos": round(soma_adultos[i] / total_avaliacoes, 1),
                         "ninfas": round(soma_ninfas[i] / total_avaliacoes, 1)} for i in range(num_pontos)]

        # Previsão e recomendações com base na avaliação atual
        populacao_prevista = prever_populacao(dados_pontos, clima)
        recomendacoes = gerar_recomendacoes(dados_pontos, populacao_prevista)

        # Exibe gráficos com médias históricas e nova avaliação
        st.subheader("📊 Histórico e Previsão Populacional")
        plotar_graficos(media_pontos, populacao_prevista)

        st.subheader("Recomendações Técnicas")
        st.markdown(recomendacoes)
        st.success("Análise concluída.")

        # Salva dados
        pasta = "avaliacoes_salvas"
        os.makedirs(pasta, exist_ok=True)
        nome_base = f"{fazenda}_{talhao}_{data_avaliacao}".replace(" ", "_")
        with open(f"{pasta}/{nome_base}.json", "w") as f:
            json.dump({
                "fazenda": fazenda,
                "talhao": talhao,
                "cidade": cidade,
                "data": str(data_avaliacao),
                "dados_pontos": dados_pontos,
                "populacao_prevista": populacao_prevista,
                "recomendacoes": recomendacoes
            }, f)

        caminho_imagem = None
        if imagem:
            imagem_path = f"{pasta}/{nome_base}.jpg"
            with open(imagem_path, "wb") as img:
                img.write(imagem.read())
            caminho_imagem = imagem_path

        pdf_file = gerar_relatorio_pdf(
            fazenda, talhao, cidade, data_avaliacao,
            dados_pontos, populacao_prevista,
            recomendacoes, caminho_imagem
        )

        st.download_button(
            label="📄 Download do Relatório",
            data=pdf_file,
            file_name="relatorio.pdf",
            mime="application/pdf"
        )
