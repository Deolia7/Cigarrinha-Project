from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os

def remover_acentos(texto):
    import unicodedata
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

def gerar_relatorio_pdf(fazenda, talhao, cidade, data, dados_pontos, populacao_prevista, recomendacoes, caminho_imagem=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, remover_acentos("Relatório Técnico - Monitoramento da Cigarrinha-do-Milho"), ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fazenda: {remover_acentos(fazenda)} | Talhao: {remover_acentos(talhao)}", ln=True)
    pdf.cell(0, 10, f"Cidade: {remover_acentos(cidade)} | Data: {data}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Dados de Campo:", ln=True)
    pdf.set_font("Arial", "", 11)
    for p in dados_pontos:
        linha = f"Ponto {p['ponto']}: Adultos = {p['adultos']} | Ninfas = {p['ninfas']}"
        pdf.cell(0, 8, remover_acentos(linha), ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recomendacoes:", ln=True)
    pdf.set_font("Arial", "", 11)
    for linha in recomendacoes.split("\n"):
        pdf.multi_cell(0, 7, remover_acentos(linha))

    dias = list(range(len(populacao_prevista)))
    fig, ax = plt.subplots(figsize=(6, 4), dpi=80)
    ax.plot(dias, populacao_prevista, marker='o')
    ax.set_title("Previsao Populacional (30 dias)")
    ax.set_xlabel("Dias")
    ax.set_ylabel("Populacao Estimada")
    plt.tight_layout()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.savefig(tmpfile.name)
        pdf.image(tmpfile.name, w=180)
        os.unlink(tmpfile.name)
    plt.close(fig)

    if caminho_imagem and os.path.exists(caminho_imagem):
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Imagem do Talhao:", ln=True)
        pdf.image(caminho_imagem, w=180)

    # ✅ Gera o conteúdo do PDF em bytes compatível com Streamlit
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return pdf_bytes
