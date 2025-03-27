from datetime import datetime, timedelta

def prever_populacao(dados, clima):
    """
    Modelo preditivo simples baseado em crescimento linear ajustado
    com dados climáticos e número de insetos observados.

    Parâmetros:
        dados (dict): dicionário com a média de adultos e ninfas.
        clima (dict): dicionário com dados de temperatura e umidade.

    Retorna:
        list: lista de dicionários com datas e população prevista.
    """
    media_adultos = dados.get("media_adultos", 0)
    media_ninfas = dados.get("media_ninfas", 0)

    # Parâmetro de risco inicial
    populacao_base = media_adultos + (media_ninfas * 0.6)

    # Fator climático (poderia vir de regressão futura, mas aqui simplificado)
    temp = clima.get("temp", 28)
    umid = clima.get("umid", 70)

    fator_clima = 1.0
    if temp > 30:
        fator_clima += 0.1
    elif temp < 20:
        fator_clima -= 0.1

    if umid > 80:
        fator_clima += 0.05
    elif umid < 50:
        fator_clima -= 0.05

    dias = 30  # previsão para os próximos 30 dias
    previsao = []
    for i in range(dias):
        dia = datetime.now() + timedelta(days=i)
        crescimento = 1 + (i / 20)  # crescimento progressivo
        populacao = populacao_base * crescimento * fator_clima
        previsao.append({
            "data": dia.strftime("%d/%m/%Y"),
            "pop": round(populacao, 2)
        })

    return previsao
