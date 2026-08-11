# 🩺 Medical Abstract Classifier API

```text
                  ABSTRACT (Texto Médico)
                             │
                             ▼
                 ┌───────────────────────┐
                 │    Docker Container   │
                 │                       │
                 │   FastAPI (Uvicorn)   │
                 │    POST /predict      │
                 └───────────┬───────────┘
                             │
                             ▼
                   medical_classifier.pkl
                             │
                             ▼
                         TF-IDF +
                    Logistic Regression
                             │
                             ▼
                  Classificação Prevista
```

---

## 📁 Estrutura do Projeto

```text
Tech-Challenge nlp/
├── app/
│   ├── __init__.py
│   ├── main.py          # Endpoints FastAPI (/health, /predict)
│   └── model.py         # Lógica de carregamento e predição do modelo
├── data/                # Dataset de treino e teste
├── models/              # Artefatos salvos (.pkl)
├── scripts/
│   ├── benchmark.py     # Script para medição de latência
│   ├── inspect_dataset.py
│   └── train_model.py   # Treinamento do modelo baseline
├── tests/               # Testes automatizados
├── .dockerignore
├── .gitignore
├── Dockerfile           # Configuração da imagem da aplicação
├── README.md            # Documentação da solução
└── requirements.txt     # Dependências do projeto
```

---

## 📊 Métricas do Modelo Baseline

* **Dataset:** 14.438 resumos médicos (*abstracts*)
* **Modelo:** TF-IDF Vectorizer + Logistic Regression
* **Acurácia:** `55,57%`
* **F1-Score (Weighted):** `0,55`

---

## ⚡ Benchmark de Latência (no Docker)

| Métrica | Tempo (ms) |
| :--- | :--- |
| **Média de Latência** | **8.87 ms** |
| **Menor Tempo** | 2.18 ms |
| **Maior Tempo** | 14.48 ms |

---

## 🛠️ Como Executar a Aplicação

### 1. Construir a Imagem Docker
```bash
docker build -t medical-classifier-api .
```

### 2. Subir o Container
```bash
docker run -d -p 8000:8000 --name medical_api_container medical-classifier-api
```

### 3. Acessar a Documentação
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Exemplo de Payload (`POST /predict`):**
```json
{
  "text": "Does carotid restenosis predict an increased risk of stroke?"
}
```

### 4. Rodar o Benchmark de Latência
```bash
python scripts/benchmark.py
```