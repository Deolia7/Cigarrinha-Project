from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os
import io

def gerar_relatorio_pdf(fazenda, talhao, cidade, data, dados_pontos, populacao_prevista, recomendacoes, caminho_imagem=None, buffer=None):
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

    fig, ax = plt.subplots()
    dias = list(range(len(populacao_prevista)))
    ax.plot(dias, populacao_prevista, marker='o')
    ax.set_title("Previsão Populacional (30 dias)")
    ax.set_xlabel("Dias")
    ax.set_ylabel("População Estimada")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.savefig(tmpfile.name)
        plt.close(fig)
        pdf.image(tmpfile.name, w=180)
        os.unlink(tmpfile.name)

    if caminho_imagem and os.path.exists(caminho_imagem):
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Imagem do Talhão:", ln=True)
        pdf.image(caminho_imagem, w=180)

    if buffer:
        pdf.output(buffer)
        buffer.seek(0)
    else:
        pdf.output("relatorio.pdf")
