
from fpdf import FPDF
import tempfile
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório Técnico - Monitoramento da Cigarrinha-do-Milho", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def gerar_relatorio_pdf(fazenda, talhao, cidade, data_avaliacao, dados_pontos, populacao_prevista, recomendacoes, fotos, figuras):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Dados gerais
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fazenda: {fazenda}", ln=True)
    pdf.cell(0, 10, f"Talhão: {talhao}", ln=True)
    pdf.cell(0, 10, f"Localização: {cidade}", ln=True)
    pdf.cell(0, 10, f"Data da Avaliação: {data_avaliacao.strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(5)

    # Dados por ponto
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Dados Coletados por Ponto:", ln=True)
    pdf.set_font("Arial", "", 11)
    for ponto in dados_pontos:
        pdf.cell(0, 8, f"Ponto {ponto['ponto']}: Adultos = {ponto['adultos']} | Ninfas = {ponto['ninfas']}", ln=True)
    pdf.ln(5)

    # Recomendações
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recomendação Técnica:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, recomendacoes)
    pdf.ln(5)

    # Gráficos salvos temporariamente
    for i, fig in enumerate(figuras):
        temp_fig = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig.savefig(temp_fig.name, bbox_inches="tight")
        pdf.add_page()
        pdf.image(temp_fig.name, x=10, w=180)
        os.unlink(temp_fig.name)

    # Fotos reais do talhão
    if fotos:
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Fotos do Talhão:", ln=True)
        pdf.ln(5)
        for foto in fotos[:2]:
            if foto is not None:
                temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                temp_img.write(foto.read())
                temp_img.flush()
                pdf.image(temp_img.name, x=15, w=180)
                os.unlink(temp_img.name)
                pdf.ln(5)

    # Salvar PDF
    nome_arquivo = f"Relatorio_{fazenda}_{talhao}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf".replace(" ", "_")
    caminho = os.path.join("/mnt/data", nome_arquivo)
    pdf.output(caminho)
    return caminho
