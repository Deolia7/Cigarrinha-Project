import streamlit as st
from datetime import datetime
import os
import json
from components.graficos import (
    plotar_graficos,
    plotar_grafico_historico,
)
from components.relatorio_pdf import gerar_relatorio_pdf
from utils.api_weather import obter_dados_climaticos
from utils.recomendacoes import gerar_recomendacoes
from models.predicao_populacional import prever_populacao

# Título
st.title("🛰️ Monitoramento da Cigarrinha-do-Milho")

# Inicializa pastas
os.makedirs("avaliacoes_salvas", exist_ok=True)
os.makedirs("relatorios", exist_ok=True)

# Dados do usuário
with st.sidebar:
    st.subheader("📍 Identificação da Avaliação")
    fazenda = st.text_input("Nome da Fazenda")
    talhao = st.text_input("Talhão")
    localizacao = st.text_input("Cidade ou Coordenadas (Ex: Uberaba ou 18°23'26.8\"S 52°38'08.3\"W)")
    data_avaliacao = st.date_input("Data da Avaliação", value=datetime.today())
    arquivo_imagem = st.file_uploader("📷 Enviar imagem do talhão (opcional)", type=["png", "jpg", "jpeg"])
    pontos = st.slider("Número de pontos de coleta", 3, 5, 3)

# Botão para iniciar preenchimento dos dados
st.markdown("## 👇 Preencha os dados de campo:")
dados_pontos = []
for i in range(pontos):
    with st.expander(f"Ponto {i+1}", expanded=i == 0):
        adultos = st.number_input(f"Adultos no ponto {i+1}", min_value=0, step=1, key=f"adultos_{i}")
        ninfas = st.number_input(f"Ninfas no ponto {i+1}", min_value=0, step=1, key=f"ninfas_{i}")
        dados_pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

if st.button("🔍 Gerar Análise"):
    if not fazenda or not talhao or not localizacao:
        st.error("Por favor, preencha todos os campos de identificação (fazenda, talhão e localização).")
    else:
        try:
            clima = obter_dados_climaticos(localizacao)
            st.success("Análise concluída.")

            populacao_prevista = prever_populacao(clima, dados_pontos)
            recomendacoes = gerar_recomendacoes(dados_pontos, populacao_prevista)
            st.markdown("### 📋 Recomendações Técnicas")
            st.markdown(recomendacoes)

            # Salvar dados no histórico
            nome_arquivo = f"avaliacoes_salvas/{fazenda}_{talhao}.json"
            if os.path.exists(nome_arquivo):
                with open(nome_arquivo, "r") as f:
                    historico = json.load(f)
            else:
                historico = []

            nova_avaliacao = {
                "data": str(data_avaliacao),
                "dados": dados_pontos,
                "populacao_prevista": populacao_prevista,
                "imagem": arquivo_imagem.name if arquivo_imagem else None
            }

            if arquivo_imagem:
                img_path = f"avaliacoes_salvas/{fazenda}_{talhao}_{data_avaliacao}.jpg"
                with open(img_path, "wb") as f:
                    f.write(arquivo_imagem.getbuffer())
                nova_avaliacao["imagem_path"] = img_path

            historico.append(nova_avaliacao)

            with open(nome_arquivo, "w") as f:
                json.dump(historico, f, indent=4)

            # Gráficos
            plotar_graficos(dados_pontos, populacao_prevista)
            plotar_grafico_historico(historico)

            # Tabela
            st.markdown("### 📑 Histórico de Avaliações")
            import pandas as pd
            df = pd.DataFrame([
                {
                    "Data": h["data"],
                    "População Real (média)": round(sum(p["adultos"] + p["ninfas"] for p in h["dados"]) / len(h["dados"]), 1),
                    "População Prevista (modelo)": round(h["populacao_prevista"][0], 1)
                } for h in historico
            ])
            st.dataframe(df)

            # Exportar CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Baixar histórico em CSV", csv, "historico.csv", "text/csv")

            # Relatório PDF
            st.markdown("### 📄 Baixar Relatório Completo")
            pdf_file = gerar_relatorio_pdf(fazenda, talhao, historico, recomendacoes)
            st.download_button("⬇️ Baixar PDF", data=pdf_file, file_name="relatorio_cigarrinha.pdf")

        except Exception as e:
            st.error(f"Erro ao obter dados climáticos: {e}")
