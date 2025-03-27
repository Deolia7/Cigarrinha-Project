def gerar_recomendacoes(dados_pontos, populacao_prevista):
    recomendacoes = []

    pico_populacional = max([p["pop"] for p in populacao_prevista])
    data_pico = next((p["data"] for p in populacao_prevista if p["pop"] == pico_populacional), None)

    dose = "800 a 1000 mL p.c./ha"
    calda_terrestre = "150 L/ha"
    calda_aerea = "10 a 50 L/ha"
    intervalo_aplicacao = "Máximo de 3 aplicações com intervalo de 7 dias"
    intervalo_seguranca = "35 dias"

    if pico_populacional > 7:
        mensagem = (
            f"⚠️ População prevista em alta! Recomendado iniciar aplicações antes de {data_pico}. "
            "Use Efficon na dose recomendada e siga os intervalos indicados."
        )
    elif pico_populacional > 5:
        mensagem = (
            f"⚠️ População em crescimento! Observe os talhões e esteja pronto para aplicar antes de {data_pico}."
        )
    else:
        mensagem = "✅ Níveis populacionais controlados. Manter monitoramento regular."

    recomendacoes.append({
        "pico_populacional": round(pico_populacional, 2),
        "data_pico": data_pico,
        "mensagem": mensagem,
        "produto": {
            "nome": "Efficon",
            "dose": dose,
            "calda_terrestre": calda_terrestre,
            "calda_aerea": calda_aerea,
            "intervalo_aplicacao": intervalo_aplicacao,
            "intervalo_seguranca": intervalo_seguranca
        }
    })

    return recomendacoes
