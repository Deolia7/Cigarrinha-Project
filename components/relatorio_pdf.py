from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório Técnico - Monitoramento da Cigarrinha-do-Milho", ln=True, align="C")
        self.ln(5)

def gerar_relatorio_pdf(fazenda, talhao, avaliacao, recomendacoes, historico):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 11)

    pdf.cell(0, 10, f"Fazenda: {fazenda}", ln=True)
    pdf.cell(0, 10, f"Talhão: {talhao}", ln=True)
    pdf.cell(0, 10, f"Data da Avaliação: {avaliacao['data']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "Resumo da Avaliação", ln=True)
    pdf.set_font("Arial", "", 11)

    for i, ponto in enumerate(avaliacao["pontos"]):
        pdf.cell(0, 10, f"Ponto {i+1} - Adultos: {ponto['adultos']}, Ninfas: {ponto['ninfas']}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "Previsão Populacional (30 dias)", ln=True)
    pdf.set_font("Arial", "", 11)
    previsao_str = ", ".join(str(v) for v in avaliacao["populacao_prevista"])
    pdf.multi_cell(0, 10, previsao_str)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "Recomendações Técnicas", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, recomendacoes)

    if avaliacao.get("imagem") and os.path.exists(avaliacao["imagem"]):
        pdf.add_page()
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "Foto da Avaliação", ln=True)
        pdf.image(avaliacao["imagem"], w=150)

    return pdf.output(dest="S").encode("latin1")