import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY", "sua_api_key_aqui")  # substitua se necessário

def obter_clima(localizacao):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={localizacao}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Erro na API: " + response.text)
    dados = response.json()
    return {
        "temp": dados["main"]["temp"],
        "umidade": dados["main"]["humidity"]
    }