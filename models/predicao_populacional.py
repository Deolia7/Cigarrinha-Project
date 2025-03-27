def prever_populacao(dados_pontos, clima):
    base = sum(p["adultos"] + p["ninfas"] for p in dados_pontos) / len(dados_pontos)
    previsao = []
    for i in range(10):
        clima_dia = clima["list"][min(i, len(clima["list"]) - 1)]
        temp = clima_dia["main"]["temp"]
        pop = base * (1 + (temp - 20) * 0.03)
        previsao.append(round(pop, 2))
    return previsao
