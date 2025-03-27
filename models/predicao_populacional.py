
import numpy as np
import pandas as pd
from datetime import timedelta, datetime

def prever_populacao(dados_pontos, clima):
    media_adultos = np.mean([p["adultos"] for p in dados_pontos])
    media_ninfas = np.mean([p["ninfas"] for p in dados_pontos])
    taxa_transicao = 0.75  # porcentagem de ninfas que viram adultos
    dias = 30

    datas = [datetime.today() + timedelta(days=i) for i in range(dias)]
    adultos_previstos = []
    for i in range(dias):
        clima_dia = clima['list'][min(i, len(clima['list']) - 1)]
        temperatura = clima_dia['main']['temp']
        umidade = clima_dia['main']['humidity']

        fator_climatico = 1 + (temperatura - 25) * 0.03 + (umidade - 60) * 0.01
        fator_climatico = max(0.5, min(1.5, fator_climatico))  # Limita o impacto climático

        adultos = (media_adultos + media_ninfas * taxa_transicao) * (1 + 0.1*i/10) * fator_climatico
        adultos_previstos.append(adultos)

    df_prev = pd.DataFrame({
        "dia": datas,
        "populacao_prevista": adultos_previstos
    })

    return df_prev
