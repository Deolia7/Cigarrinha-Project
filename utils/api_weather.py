
import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def obter_dados_climaticos(localizacao):
    url_base = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": localizacao,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 10  # previsão dos próximos dias
    }

    try:
        resposta = requests.get(url_base, params=params)
        dados = resposta.json()
        if resposta.status_code == 200:
            return dados
        else:
            return {"erro": f"Erro na API: {dados.get('message', 'Erro desconhecido')}"}
    except Exception as e:
        return {"erro": str(e)}
