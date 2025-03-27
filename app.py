import streamlit as st
from components.recomendacoes import gerar_recomendacoes
from components.predicao_populacional import prever_populacao
from components.api_weather import obter_dados_climaticos
from components.graficos import gerar_graficos
from components.relatorio_pdf import gerar_relatorio_pdf
import pandas as pd
from datetime import datetime
import os
from PIL import Image
import uuid

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-Milho", layout="wide")

st.title("🌽 Monitoramento da Cigarrinha-do-Milho")

# 📁 Criar pastas se não existirem
os.makedirs("avaliacoes_salvas", exist_ok=True)
os.makedirs("fotos_salvas", exist_ok=True)

# 📋 Entrada de dados
with st.form("avaliacao_form"):
    st.subheader("Cadastro da Avaliação")
    talhao = st.text_input("Nome do Talhão")
    cidade = st.text_input("Cidade ou Coordenada (ex: 'Rio Verde' ou '-18.91,-50.16')")

    col1, col2 = st.columns(2)
    with col1:
        data_avaliacao = st.date_input("Data da Avaliação", value=datetime.today())
        adultos = st.number_input("Nº médio de Adultos", 0.0, 100.0, 0.0, step=0.1)
        ninfas = st.number_input("Nº médio de Ninfas", 0.0, 100.0, 0.0, step=0.1)
    with col2:
        foto = st.file_uploader("Foto do Talhão (opcional)", type=["jpg", "jpeg", "png"])

    submit = st.form_submit_button("Gerar Análise")

# 🔄 Processamento
if submit:
    if not cidade.strip():
        st.error("⚠️ Por favor, preencha a cidade ou coordenadas corretamente.")
    else:
        try:
            with st.spinner("Analisando..."):

                # 🌡️ Clima
                datas_clima, temps, ums = obter_dados_climaticos(cidade)

                # 🐛 População
                media_total = adultos + ninfas
                previsao = prever_populacao(datas_clima, temps, ums)

                # 💡 Recomendação
                recomendacoes = gerar_recomendacoes(media_total, previsao)

                # 🖼️ Salvar imagem se enviada
                foto_path = None
                if foto:
                    foto_id = str(uuid.uuid4())
                    ext = os.path.splitext(foto.name)[-1]
                    foto_path = f"fotos_salvas/{foto_id}{ext}"
                    with open(foto_path, "wb") as f:
                        f.write(foto.read())

                # 💾 Histórico por talhão
                historico_path = f"avaliacoes_salvas/{talhao}.csv"
                if os.path.exists(historico_path):
                    df_hist = pd.read_csv(historico_path)
                else:
                    df_hist = pd.DataFrame(columns=["Data", "População Real (média)", "População Prevista (modelo)"])

                nova_entrada = {
                    "Data": data_avaliacao.strftime("%Y-%m-%d"),
                    "População Real (média)": media_total,
                    "População Prevista (modelo)": round(previsao, 1)
                }
                df_hist = pd.concat([df_hist, pd.DataFrame([nova_entrada])], ignore_index=True)
                df_hist.drop_duplicates(subset="Data", keep="last", inplace=True)
                df_hist.to_csv(historico_path, index=False)

                # 📈 Gráficos
                st.subheader("📊 Gráficos Populacionais")
                gerar_graficos(df_hist)

                # 📋 Tabela de histórico
                st.subheader("📋 Histórico de Avaliações")
                st.dataframe(df_hist)
                st.download_button("⬇️ Baixar histórico em CSV", df_hist.to_csv(index=False), file_name="historico.csv", mime="text/csv")

                # 📄 Relatório PDF
                pdf_file = gerar_relatorio_pdf(
                    talhao=talhao,
                    cidade=cidade,
                    media_adultos=adultos,
                    media_ninfas=ninfas,
                    media_total=media_total,
                    clima_data=datas_clima,
                    clima_temps=temps,
                    clima_ums=ums,
                    recomendacoes=recomendacoes,
                    fotos=[foto_path] if foto_path else [],
                    historico=df_hist
                )

                st.download_button(
                    label="📥 Baixar Relatório PDF",
                    data=pdf_file,
                    file_name="relatorio_cigarrinha.pdf",
                    mime="application/pdf"
                )

                st.success("Análise concluída.")
        except Exception as e:
            st.error(f"Erro ao processar os dados: {e}")
