# Monitoramento da Cigarrinha-do-Milho 🐛🌽

Este é um aplicativo interativo para auxiliar técnicos agrícolas no **monitoramento da população da cigarrinha-do-milho (Dalbulus maidis)** com base em dados coletados no campo e previsão climática.

### 🚀 Funcionalidades

- Cadastro de fazendas e talhões
- Inserção de dados por ponto de coleta (adultos e ninfas)
- Gráficos de população atual, previsão e comparativo com pico futuro
- Recomendações agronômicas automáticas
- Geração de relatório técnico (PDF)
- Suporte a **cidades** ou **coordenadas (Google Maps)**

---

### ▶️ Executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

### ☁️ Deploy no Streamlit Cloud

1. Suba todos os arquivos para um repositório público no GitHub
2. Acesse: [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecte ao repositório e selecione:
   - `app.py` como script principal
   - Adicione o segredo `OPENWEATHER_API_KEY` nas configurações (`Secrets`)
4. Clique em **Deploy**

---

### 🔑 Variáveis de ambiente

No menu `Settings > Secrets`, adicione:

```
OPENWEATHER_API_KEY = "sua_chave_api_openweather"
```

---

### 📦 Estrutura do projeto

```
📁 components/
📁 models/
📁 utils/
📄 app.py
📄 requirements.txt
📄 README.md
```
