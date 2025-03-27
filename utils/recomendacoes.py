def gerar_recomendacoes(dados_pontos, populacao_prevista):
    media_atual = sum(p["adultos"] + p["ninfas"] for p in dados_pontos) / len(dados_pontos)
    pico = max(populacao_prevista)
    indice_pico = populacao_prevista.index(pico)
    
    recomendacao = ""
    if pico > media_atual * 2:
        recomendacao += "🔴 **Alerta de Infestação:** Aplicação imediata de inseticida é recomendada.\n\n"
    elif pico > media_atual * 1.2:
        recomendacao += "🟠 **Tendência de aumento:** Monitore frequentemente e considere aplicação preventiva.\n\n"
    else:
        recomendacao += "🟢 **População sob controle:** Continue monitorando regularmente.\n\n"

    recomendacao += f"📅 **Pico previsto em {indice_pico} dias**. Ideal aplicar inseticida até esse período.\n\n"
    recomendacao += "**Produto recomendado:** Efficon\n"
    recomendacao += "- Dose: 800 a 1000 mL p.c./ha\n"
    recomendacao += "- Volume de calda: 150 L/ha (terrestre) ou 30-50 L/ha (aéreo)\n"
    recomendacao += "- Repetir aplicação até 3 vezes, com intervalo de 7 dias entre aplicações.\n"
    
    return recomendacao