from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório de Monitoramento da Cigarrinha-do-Milho", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def gerar_relatorio_pdf(fazenda, talhao, nova_avaliacao, recomendacoes, historico):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fazenda: {fazenda}", ln=True)
    pdf.cell(0, 10, f"Talhão: {talhao}", ln=True)
    pdf.cell(0, 10, f"Data da Avaliação: {nova_avaliacao.get('data', 'N/A')}", ln=True)
    pdf.cell(0, 10, f"Ponto(s) Avaliado(s): {nova_avaliacao.get('pontos', 'N/A')}", ln=True)
    pdf.cell(0, 10, f"Média de Adultos: {nova_avaliacao.get('media_real_adultos', 'N/A')}", ln=True)
    pdf.cell(0, 10, f"Média de Ninfas: {nova_avaliacao.get('media_real_ninfas', 'N/A')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recomendações Técnicas:", ln=True)
    pdf.set_font("Arial", "", 12)
    for linha in recomendacoes.split("\n"):
        pdf.multi_cell(0, 8, linha)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Histórico de Avaliações:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(60, 8, "Data", 1)
    pdf.cell(65, 8, "População Real (média)", 1)
    pdf.cell(65, 8, "População Prevista (modelo)", 1, ln=True)
    for _, row in historico.iterrows():
        pdf.cell(60, 8, str(row["data"]), 1)
        pdf.cell(65, 8, str(row["media_real"]), 1)
        pdf.cell(65, 8, str(row["media_prevista"]), 1, ln=True)

    return pdf.output(dest="S").encode("latin-1", "replace")
