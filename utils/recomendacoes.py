
def gerar_recomendacoes(dados_pontos, df_prev):
    media_adultos = sum(p["adultos"] for p in dados_pontos) / len(dados_pontos)
    media_ninfas = sum(p["ninfas"] for p in dados_pontos) / len(dados_pontos)

    pico_previsto = df_prev["populacao_prevista"].max()
    texto = []

    if media_adultos + media_ninfas > 20:
        texto.append("- Alto nível atual de infestação. Aplicação de inseticida recomendada imediatamente.")
    elif pico_previsto > 25:
        texto.append("- Infestação tende a aumentar. Monitorar de perto e considerar aplicação nos próximos 7 dias.")
    else:
        texto.append("- População controlada. Reavaliar em 7 dias.")

    if media_ninfas > 5:
        texto.append("- Alta presença de ninfas. Possível surto futuro. Priorize o monitoramento contínuo.")

    return "\n".join(texto)
