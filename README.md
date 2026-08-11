# 🩺 Medical Abstract Classification API (Tech-Challenge NLP)

API desenvolvida com FastAPI para classificação de resumos médicos (*abstracts*) utilizando técnicas de Processamento de Linguagem Natural (NLP) e Machine Learning.

---

## 📐 Arquitetura da Solução

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

📊 Métricas do Modelo Baseline
Dataset: 14.438 resumos médicos (abstracts)

Modelo: TF-IDF Vectorizer + Logistic Regression

Acurácia: 55,57%

F1-Score (Weighted): 0,55

⚡ Benchmark de Latência (no Docker)
Teste de latência realizado através do script scripts/benchmark.py enviando 50 requisições sequenciais para o container Docker:
MétricaTempo (ms)Média de Latência8.87 msMenor Tempo2.18 msMaior Tempo14.48 ms

🛠️ Como Executar a Aplicação
Pró-requisitos
Docker instalado e em execução.

Python 3.10+ (para rodar scripts locais como o benchmark).

1. Construir a Imagem Docker
Na raiz do projeto, execute:
Bash
docker build -t medical-classifier-api .


2. Subir o Container
Bash
docker run -d -p 8000:8000 --name medical_api_container medical-classifier-api

3. Acessar a Documentação Interativa (Swagger)
Abra no seu navegador:

👉 http://127.0.0.1:8000/docs

Endpoints Disponíveis:
GET /health: Retorna {"status": "ok"} para verificação da saúde do serviço.

POST /predict: Recebe o texto e retorna a doença/condição prevista.

Exemplo de Payload (POST /predict):
JSON
{
  "text": "Does carotid restenosis predict an increased risk of stroke?"
}


4. Rodar o Benchmark de Latência
Com a API ativa no Docker, execute:
Bash
python scripts/benchmark.py