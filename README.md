# 🩺 Medical Abstract Classification API (Tech-Challenge NLP)

API desenvolvida com FastAPI para classificação e triagem automática de laudos/resumos médicos (*abstracts*) utilizando técnicas de Processamento de Linguagem Natural (NLP) e Machine Learning.

---

## ☁️ Decisão Arquitetural: Estratégia de Deploy em Nuvem

### Análise de Cenário: Real-Time vs. Batch
Para o contexto hospitalar de **triagem automática de laudos médicos**, a arquitetura escolhida foi o **Processamento em Tempo Real (Real-Time Ingestion)** via API REST.
* **Justificativa**: Casos de urgência médica exigem classificação imediata para priorização na fila de atendimento. Um modelo *Batch* (processamento em lote) geraria um atraso inaceitável na detecção de laudos críticos.

### Proposta de Provedor de Nuvem (AWS)
Para suportar o serviço em produção com alta disponibilidade, escalabilidade e conformidade, recomenda-se a infraestrutura da **AWS**:
1. **Compute**: **AWS ECS (Elastic Container Service)** com **Fargate** para rodar o container Docker da API FastAPI de forma serverless.
2. **Gateway**: **Amazon API Gateway** para controle de tráfego, autenticação, rate limiting e roteamento das requisições.
3. **Monitoramento/Logs**: **Amazon CloudWatch** integrado com o container para coleta de logs operacionais.
4. **CI/CD**: Integração nativa com **GitHub Actions** via *OIDC* para deploy automatizado na AWS a cada *push* no repositório.

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

## 📊 Métricas do Modelo Baseline

- **Dataset**: 14.438 resumos médicos (*abstracts*)
- **Modelo**: TF-IDF Vectorizer + Logistic Regression
- **Acurácia**: `55,57%`
- **F1-Score (Weighted)**: `0,55`

---

## ⚡ Benchmark de Latência (no Docker)

Teste de latência realizado através do script `scripts/benchmark.py` enviando **50 requisições sequenciais** para o container Docker:

| Métrica | Tempo (ms) |
| :--- | :--- |
| **Média de Latência** | **8.87 ms** |
| **Menor Tempo** | 2.18 ms |
| **Maior Tempo** | 14.48 ms |

🛠️ Como Executar a Aplicação
Pré-requisitos
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

