from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Relatório Técnico - Monitoramento da Cigarrinha-do-Milho', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_image(self, path, date_label):
        self.add_page()
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Foto registrada em: {date_label}', 0, 1)
        self.image(path, x=15, w=180)
        self.ln(5)

def gerar_relatorio_pdf(fazenda, talhao, cidade, data_avaliacao, dados_pontos, populacao_prevista, recomendacoes, imagem_path):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Arial', '', 12)

    pdf.chapter_title("Informações Gerais")
    info = f"Fazenda: {fazenda}\nTalhão: {talhao}\nCidade: {cidade}\nData da Avaliação: {data_avaliacao}"
    pdf.chapter_body(info)

    pdf.chapter_title("Dados da Avaliação")
    for ponto in dados_pontos:
        linha = f"Ponto {ponto['ponto']}: Adultos = {ponto['adultos']} | Ninfas = {ponto['ninfas']}"
        pdf.chapter_body(linha)

    pdf.chapter_title("Previsão Populacional (30 dias)")
    previsao_texto = ", ".join([f"{round(p, 2)}" for p in populacao_prevista])
    pdf.chapter_body(previsao_texto)

    pdf.chapter_title("Recomendações Técnicas")
    pdf.chapter_body(recomendacoes.replace("•", "-"))

    # Adicionar todas as imagens históricas do talhão
    if fazenda and talhao:
        pasta = "avaliacoes_salvas"
        prefixo = f"{fazenda}_{talhao}_"
        imagens = sorted([f for f in os.listdir(pasta) if f.endswith(".jpg") and prefixo in f])
        for img in imagens:
            data_str = img.replace(f"{prefixo}", "").replace(".jpg", "")
            img_path = os.path.join(pasta, img)
            pdf.add_image(img_path, data_str)

    # Retorna binário
    return pdf.output(dest='S').encode('latin1')
