
import streamlit as st
from utils.api_weather import obter_dados_climaticos
from models.predicao_populacional import prever_populacao
from utils.recomendacoes import gerar_recomendacoes
from components.graficos import plotar_graficos
from components.relatorio_pdf import gerar_relatorio_pdf
import datetime

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-Milho", layout="wide")
st.title("Monitoramento da Cigarrinha-do-Milho")

# Entrada de dados da fazenda e talhão
st.sidebar.header("Cadastro da Avaliação")
fazenda = st.sidebar.text_input("Nome da Fazenda")
talhao = st.sidebar.text_input("Nome do Talhão")
cidade = st.sidebar.text_input("Cidade ou Coordenadas (Google Maps format)")
data_avaliacao = st.sidebar.date_input("Data da Avaliação", value=datetime.date.today())

# Pontos de coleta (mínimo 3)
st.sidebar.subheader("Dados de Campo")
num_pontos = st.sidebar.slider("Número de Pontos de Coleta", min_value=3, max_value=5, value=3)

dados_pontos = []
for i in range(num_pontos):
    st.sidebar.markdown(f"### Ponto {i+1}")
    adultos = st.sidebar.number_input(f"Nº de Adultos - Ponto {i+1}", min_value=0, step=1)
    ninfas = st.sidebar.number_input(f"Nº de Ninfas - Ponto {i+1}", min_value=0, step=1)
    dados_pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

# Botão de processar
if st.sidebar.button("Gerar Análise"):
    with st.spinner("Analisando dados..."):
        clima = obter_dados_climaticos(cidade)

        if "erro" in clima:
            st.error(f"Erro ao obter dados climáticos: {clima['erro']}")
            st.stop()

        # Debug: mostrar dados climáticos brutos
        st.expander("🔍 Dados climáticos brutos").write(clima)

        populacao_prevista = prever_populacao(dados_pontos, clima)
        recomendacoes = gerar_recomendacoes(dados_pontos, populacao_prevista)
        plotar_graficos(dados_pontos, populacao_prevista)

        st.subheader("Recomendações Técnicas")
        st.markdown(recomendacoes)

        st.success("Análise concluída.")

        if st.button("Baixar Relatório PDF"):
            gerar_relatorio_pdf(fazenda, talhao, cidade, data_avaliacao, dados_pontos, populacao_prevista, recomendacoes)
