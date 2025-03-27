
from datetime import datetime, timedelta
import numpy as np

def gerar_recomendacoes(dados_pontos, populacao_prevista):
    media_adultos = np.mean([p["adultos"] for p in dados_pontos])
    media_ninfas = np.mean([p["ninfas"] for p in dados_pontos])
    pico_populacional = max([p["pop"] for p in populacao_prevista])
    data_pico = max(populacao_prevista, key=lambda p: p["pop"])["data"]

    janela_inicio = (datetime.strptime(data_pico, "%Y-%m-%d") - timedelta(days=7)).strftime("%d/%m/%Y")
    janela_fim = (datetime.strptime(data_pico, "%Y-%m-%d") - timedelta(days=2)).strftime("%d/%m/%Y")
    data_pico_formatada = datetime.strptime(data_pico, "%Y-%m-%d").strftime("%d/%m/%Y")

    texto = f"""
📊 **Média de Insetos por Ponto**  
Adultos: {media_adultos:.1f} | Ninfas: {media_ninfas:.1f}

🧪 **Produto recomendado: Efficon**  
• Dose: 800 a 1000 mL p.c./ha  
• Calda Terrestre: 150 L/ha  
• Calda Aérea: 10 a 50 L/ha  
• Intervalo de aplicação: Máximo de 3 aplicações com 7 dias de intervalo  
• Intervalo de segurança: 35 dias

📅 **Época ideal de aplicação:**  
Início da infestação, preferencialmente **antes do pico populacional previsto**.

🗓️ **Pico estimado:** {data_pico_formatada}  
🔍 **Janela ideal de controle:** entre **{janela_inicio}** e **{janela_fim}**

⚠️ Repetir a aplicação em caso de reinfestações. Para pulverização aérea, utilizar bicos centrífugos (atomizadores rotativos) com volume entre 10 e 30 L/ha.

💡 Ajustar a estratégia conforme condições climáticas e monitoramento contínuo.
    """

    return texto.strip()
