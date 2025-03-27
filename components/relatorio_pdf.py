
from fpdf import FPDF
import tempfile
import streamlit as st
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório Técnico - Monitoramento da Cigarrinha-do-Milho', ln=True, align='C')
        self.ln(10)

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, title, ln=True)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 8, content)
        self.ln(4)

def gerar_relatorio_pdf(fazenda, talhao, cidade, data, dados_pontos, df_prev, recomendacoes):
    pdf = PDF()
    pdf.add_page()

    pdf.add_section("Informações da Avaliação", f"Fazenda: {fazenda}\nTalhão: {talhao}\nCidade: {cidade}\nData: {data}")

    texto_pontos = "\n".join([f"Ponto {p['ponto']}: {p['adultos']} adultos, {p['ninfas']} ninfas" for p in dados_pontos])
    pdf.add_section("Dados de Campo", texto_pontos)

    pico = df_prev['populacao_prevista'].max()
    previsao_resumo = f"Pico previsto de população: {pico:.2f} indivíduos nos próximos 30 dias."
    pdf.add_section("Resumo da Previsão", previsao_resumo)

    pdf.add_section("Recomendações Técnicas", recomendacoes)

    # Salvar o PDF temporariamente e criar botão para download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        with open(tmp_file.name, "rb") as f:
            st.download_button("📄 Baixar Relatório PDF", f, file_name="relatorio_cigarrinha.pdf")
        os.unlink(tmp_file.name)
