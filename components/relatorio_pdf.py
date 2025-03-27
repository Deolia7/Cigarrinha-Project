from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os
from io import BytesIO

def gerar_relatorio_pdf(fazenda, talhao, cidade, data, dados_pontos, populacao_prevista, recomendacoes, caminho_imagem=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Relatório Técnico - Monitoramento da Cigarrinha-do-Milho", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fazenda: {fazenda} | Talhão: {talhao}", ln=True)
    pdf.cell(0, 10, f"Cidade: {cidade} | Data: {data}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Dados de Campo:", ln=True)
    pdf.set_font("Arial", "", 11)
    for p in dados_pontos:
        pdf.cell(0, 8, f"Ponto {p['ponto']}: Adultos = {p['adultos']} | Ninfas = {p['ninfas']}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recomendações:", ln=True)
    pdf.set_font("Arial", "", 11)
    for linha in recomendacoes.split("\n"):
        pdf.multi_cell(0, 7, linha)

    # Gráfico de previsão populacional
    dias = list(range(len(populacao_prevista)))
    fig, ax = plt.subplots()
    ax.plot(dias, populacao_prevista, marker='o')
    ax.set_title("Previsão Populacional (30 dias)")
    ax.set_xlabel("Dias")
    ax.set_ylabel("População Estimada")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.savefig(tmpfile.name)
        pdf.image(tmpfile.name, w=180)
        os.unlink(tmpfile.name)

    if caminho_imagem and os.path.exists(caminho_imagem):
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Imagem do Talhão:", ln=True)
        pdf.image(caminho_imagem, w=180)

    # Gerar PDF em memória
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    import streamlit as st
    st.download_button("📄 Download do Relatório", data=pdf_buffer, file_name="relatorio.pdf", mime="application/pdf")
