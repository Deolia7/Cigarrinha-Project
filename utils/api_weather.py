import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def obter_dados_climaticos(localizacao):
    url_base = "http://api.openweathermap.org/data/2.5/forecast"

    if "," in localizacao:
        try:
            lat, lon = localizacao.split(",")
            params = {
                "lat": lat.strip(),
                "lon": lon.strip(),
                "appid": API_KEY,
                "units": "metric",
                "cnt": 10
            }
        except:
            return {"erro": "Formato de coordenadas inválido. Use: -17.830784, -51.764033"}
    else:
        params = {
            "q": localizacao.strip(),
            "appid": API_KEY,
            "units": "metric",
            "cnt": 10
        }

    try:
        resposta = requests.get(url_base, params=params)
        dados = resposta.json()
        if resposta.status_code == 200 and "list" in dados:
            return dados
        else:
            return {"erro": f"Erro na API: {dados.get('message', 'desconhecido')}"}
    except Exception as e:
        return {"erro": str(e)}
