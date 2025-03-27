
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório de Monitoramento - Cigarrinha-do-Milho", ln=True, align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 10, text)

def gerar_relatorio_pdf(dados_pontos, populacao_prevista, recomendacoes, imagem, historico):
    pdf = PDF()
    pdf.add_page()

    # Dados da avaliação
    pdf.chapter_title("Dados da Avaliação")
    hoje = datetime.today().strftime("%d/%m/%Y")
    texto = f"Data do Relatório: {hoje}\n\n"
    for i, ponto in enumerate(dados_pontos):
        texto += f"Ponto {i+1}: Adultos = {ponto['adultos']}, Ninfas = {ponto['ninfas']}\n"
    pdf.chapter_body(texto)

    # Gráfico de previsão
    pdf.chapter_title("Previsão Populacional")
    previsao_txt = ", ".join([str(round(p, 1)) for p in populacao_prevista])
    pdf.chapter_body("Próximos dias (população prevista):\n" + previsao_txt)

    # Recomendação
    pdf.chapter_title("Recomendações Técnicas")
    pdf.chapter_body(recomendacoes.replace("**", "").replace("\n", "\n"))

    # Histórico
    if historico:
        pdf.chapter_title("Histórico de Avaliações")
        for h in historico:
            linha = f"Data: {h['data']} | População Real: {h['pop_real']} | Prevista: {h['pop_prevista']}"
            pdf.chapter_body(linha)

    # Foto
    if imagem:
        try:
            image = Image.open(imagem)
            image = image.convert("RGB")
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)
            pdf.chapter_title("Foto do Talhão")
            pdf.image(buffer, x=10, y=None, w=100)
        except Exception as e:
            pdf.chapter_body(f"Erro ao carregar imagem: {e}")

    return pdf.output(dest="S").encode("latin1")
