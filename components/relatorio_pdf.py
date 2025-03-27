from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório de Monitoramento da Cigarrinha-do-Milho", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def gerar_relatorio_pdf(dados_pontos, populacao_prevista, caminho, fotos=None, recomendacoes=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "", 12)

    # Dados coletados
    pdf.cell(0, 10, "Dados Coletados:", ln=True)
    for ponto in dados_pontos:
        texto = f"Ponto {ponto['ponto']} - Adultos: {ponto['adultos']}, Ninfas: {ponto['ninfas']}"
        pdf.cell(0, 10, texto, ln=True)

    pdf.ln(5)

    # Recomendações
    if recomendacoes:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Recomendações Técnicas:", ln=True)
        pdf.set_font("Arial", "", 12)
        for linha in recomendacoes.split("\n"):
            pdf.multi_cell(0, 10, linha)

    pdf.ln(5)

    # Previsão Populacional
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Previsão Populacional:", ln=True)
    pdf.set_font("Arial", "", 12)
    for p in populacao_prevista[:5]:
        data = p["data"]
        pop = p["pop"]
        pdf.cell(0, 10, f"{data}: {pop:.2f}", ln=True)

    # Fotos
    if fotos:
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Fotos do Talhão:", ln=True)
        for foto in fotos:
            pdf.image(foto, w=100)
            pdf.ln(10)

    # Salvar PDF
    nome_pdf = f"{caminho}/relatorio_cigarrinha_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(nome_pdf)
    return nome_pdf
