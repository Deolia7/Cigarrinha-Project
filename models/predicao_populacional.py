def prever_populacao(dados_pontos, clima):
    base = sum(p["adultos"] + p["ninfas"] for p in dados_pontos) / len(dados_pontos)
    fator = 1.15 + (clima["temp"] / 100) + (clima["umidade"] / 200)
    return [round(base * (fator ** i), 1) for i in range(30)]