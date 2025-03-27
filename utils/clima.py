import requests

def obter_dados_climaticos(latitude, longitude, api_key):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/forecast?"
            f"lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=pt_br"
        )
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as e:
        raise ValueError(f"Erro ao obter dados climáticos: {str(e)}")
