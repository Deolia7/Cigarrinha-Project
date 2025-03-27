def gerar_recomendacoes(dados_pontos, populacao_prevista):
    media_atual = sum(p["adultos"] + p["ninfas"] for p in dados_pontos) / len(dados_pontos)
    pico = max(populacao_prevista)

    if pico > media_atual * 2:
        return "🔴 Recomenda-se aplicação imediata de inseticida. Pico populacional previsto nos próximos dias."
    elif pico > media_atual * 1.2:
        return "🟠 Atenção: tendência de aumento populacional. Monitore frequentemente e considere aplicação preventiva."
    else:
        return "🟢 Níveis sob controle. Continue monitorando."
