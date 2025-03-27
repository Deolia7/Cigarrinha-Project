from fpdf import FPDF
from io import BytesIO
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório de Monitoramento - Cigarrinha-do-Milho", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def gerar_relatorio_pdf(talhao, cidade, media_adultos, media_ninfas, media_total, clima_data, clima_temps, clima_ums, recomendacoes, fotos, historico):
    pdf = PDF()
    pdf.add_page()

    # Dados Gerais
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Talhão: {talhao}", ln=True)
    pdf.cell(0, 10, f"Cidade/Coordenada: {cidade}", ln=True)
    pdf.cell(0, 10, f"Data da Avaliação: {datetime.today().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)

    # População
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "População Observada:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"- Média de Adultos: {media_adultos:.1f}", ln=True)
    pdf.cell(0, 10, f"- Média de Ninfas: {media_ninfas:.1f}", ln=True)
    pdf.cell(0, 10, f"- Total: {media_total:.1f}", ln=True)
    pdf.ln(5)

    # Clima
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Clima (últimos dias):", ln=True)
    pdf.set_font("Arial", size=12)
    for data, temp, um in zip(clima_data, clima_temps, clima_ums):
        pdf.cell(0, 10, f"- {data}: {temp:.1f}°C / {um:.0f}% UR", ln=True)
    pdf.ln(5)

    # Recomendação Técnica
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recomendações Técnicas:", ln=True)
    pdf.set_font("Arial", size=12)
    for item in recomendacoes:
        pdf.multi_cell(0, 10, f"- {item}")
    pdf.ln(5)

    # Histórico de Avaliações
    if historico is not None and not historico.empty:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Histórico de Avaliações:", ln=True)
        pdf.set_font("Arial", size=12)
        for idx, row in historico.iterrows():
            data = row['Data']
            real = row['População Real (média)']
            prev = row['População Prevista (modelo)']
            pdf.cell(0, 10, f"{data}: Real = {real}, Previsto = {prev}", ln=True)
        pdf.ln(5)

    # Fotos anexadas
    if fotos:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Fotos do Talhão:", ln=True)
        for foto in fotos:
            if os.path.exists(foto):
                pdf.image(foto, w=100)
                pdf.ln(3)

    # Exportar para buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.read()
