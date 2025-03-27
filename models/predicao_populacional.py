
def prever_populacao(dados, clima):
    """
    dados: list de dicionários de pontos com 'adultos' e 'ninfas'
    clima: dicionário com dados climáticos
    """
    import datetime

    # Cálculo da média geral com segurança
    total_adultos = sum([p.get("adultos", 0) for p in dados])
    total_ninfas = sum([p.get("ninfas", 0) for p in dados])
    n = len(dados) if len(dados) > 0 else 1

    media_adultos = total_adultos / n
    media_ninfas = total_ninfas / n

    # Simples modelo preditivo (placeholder)
    dias = 30
    populacao = []
    for i in range(dias):
        crescimento = (media_adultos + media_ninfas) * (1 + 0.05 * i)
        populacao.append({
            "dia": (datetime.date.today() + datetime.timedelta(days=i)).isoformat(),
            "pop": crescimento
        })

    return populacao
