def prever_populacao(media_inicial, dias=30):
    crescimento_diario = 0.05
    populacao = media_inicial
    predicao = []

    for i in range(dias):
        populacao *= (1 + crescimento_diario)
        predicao.append({"dia": i, "pop": round(populacao, 2)})

    return predicao