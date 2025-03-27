from datetime import datetime, timedelta
import numpy as np

def prever_populacao(dados_pontos, clima):
    populacao_atual = sum(p['adultos'] + p['ninfas'] for p in dados_pontos) / len(dados_pontos)

    dias = 30
    populacao_prevista = []
    for i in range(dias):
        data = datetime.now() + timedelta(days=i)
        fator_climatico = 1.0

        if 'list' in clima:
            clima_dia = clima['list'][min(i, len(clima['list']) - 1)]
            temperatura = clima_dia['main']['temp']
            umidade = clima_dia['main'].get('humidity', 50)

            if 20 <= temperatura <= 32 and umidade >= 60:
                fator_climatico = 1.05
            else:
                fator_climatico = 0.98

        nova_populacao = populacao_atual * (fator_climatico ** i)
        populacao_prevista.append({'data': data.strftime('%Y-%m-%d'), 'pop': round(nova_populacao, 2)})

    return populacao_prevista
