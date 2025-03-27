from fpdf import FPDF
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório de Monitoramento - Cigarrinha-do-Milho", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def gerar_relatorio_pdf(fazenda, talhao, cidade, data_avaliacao, dados_pontos, populacao_prevista, recomendacoes, caminho_imagem=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Dados da fazenda
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, f"Fazenda: {fazenda}", ln=True)
    pdf.cell(0, 10, f"Talhão: {talhao}", ln=True)
    pdf.cell(0, 10, f"Cidade/Coordenadas: {cidade}", ln=True)
    pdf.cell(0, 10, f"Data da Avaliação: {data_avaliacao}", ln=True)
    pdf.ln(5)

    # Tabela de dados de campo
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "Dados de Campo:", ln=True)
    pdf.set_font("Arial", "", 11)
    for ponto in dados_pontos:
        pdf.cell(0, 10, f"Ponto {ponto['ponto']}: Adultos = {ponto['adultos']} | Ninfas = {ponto['ninfas']}", ln=True)

    pdf.ln(5)

    # Previsão
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "Previsão Populacional (Próximos 30 dias):", ln=True)
    pdf.set_font("Arial", "", 11)
    for dia, valor in enumerate(populacao_prevista, start=1):
        pdf.cell(0, 10, f"Dia {dia}: {round(valor, 2)}", ln=True)

    pdf.ln(5)

    # Recomendação
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "Recomendações Técnicas:", ln=True)
    pdf.set_font("Arial", "", 11)
    for linha in recomendacoes.strip().split("\n"):
        pdf.multi_cell(0, 10, linha.strip())

    pdf.ln(5)

    # Inserir imagem (caso exista)
    if caminho_imagem and os.path.exists(caminho_imagem):
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "Imagem do Talhão:", ln=True)
        pdf.image(caminho_imagem, w=150)
        pdf.ln(5)

    # Retorno do PDF corrigido para utf-8
    return pdf.output(dest="S").encode("utf-8")
