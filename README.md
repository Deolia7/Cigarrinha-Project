
# 📊 Monitoramento da Cigarrinha-do-Milho

Este é um aplicativo completo em Streamlit para monitoramento, previsão populacional e recomendações técnicas para controle da **Cigarrinha-do-Milho (Dalbulus maidis)**.

---

## 🚀 Funcionalidades

- Cadastro de fazendas e talhões
- Entrada de dados de campo (adultos e ninfas)
- Integração com API do clima (OpenWeather)
- Previsão populacional para os próximos 30 dias
- Geração de gráficos técnicos (atual, previsão e comparativo)
- Recomendações agronômicas automáticas
- Geração de relatório técnico em PDF

---

## 🛠️ Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/monitoramento_cigarrinha.git
cd monitoramento_cigarrinha
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração da API (OpenWeather)

O app utiliza a API da OpenWeather para previsão do tempo. Crie um arquivo `secrets.toml` na pasta `.streamlit/` com o seguinte conteúdo:

```
OPENWEATHER_API_KEY = "sua_chave_aqui"
```

Você pode obter uma chave gratuita em: https://openweathermap.org/api

---

## ▶️ Executando o App

```bash
streamlit run app.py
```

---

## 🌐 Deploy no Streamlit Cloud

1. Crie um repositório no GitHub e suba os arquivos.
2. Acesse: https://streamlit.io/cloud e conecte sua conta ao GitHub.
3. Escolha o repositório e o arquivo `app.py`.
4. Vá em `Settings > Secrets` e adicione:

```
OPENWEATHER_API_KEY = sua_chave
```

Pronto! Seu app estará disponível publicamente.

---

## 📄 Licença

Este projeto está sob a licença MIT.
