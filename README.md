### 🚀 Recomendação de Infraestrutura em Nuvem (AWS / GCP / Azure)

Para este projeto, a provedora recomendada é a **AWS** (ou equivalentemente **GCP/Azure**), utilizando serviços gerenciados e serverless para otimizar custos e manutenção.

#### Opção A: Serverless com AWS Lambda + Amazon ECR

Recomendado para início do projeto ou cenários de baixo volume de requisições.

* **Arquitetura:** Empacotar a imagem Docker da API no **Amazon ECR** e executá-la através do **AWS Lambda**, integrado ao **Amazon API Gateway**.
* **Vantagens:**
  * Cobrança baseada no tempo de execução.
  * Escalabilidade automática de acordo com a demanda.
  * O modelo `TF-IDF + Logistic Regression` possui baixo consumo computacional e é adequado para ambientes serverless.

#### Opção B: Containers Gerenciados com AWS App Runner / Amazon ECS

Recomendado para cenários com tráfego constante.

* **Arquitetura:** Executar a imagem Docker diretamente através do **AWS App Runner** ou **Amazon ECS (Fargate)**.
* **Vantagens:**
  * Mantém o container disponível continuamente.
  * Reduz problemas relacionados a *cold start*.
  * Adequado para ambientes hospitalares ou clínicas com fluxo contínuo de consultas.

---

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
tech-challenge-nlp/
├── .github/
│   └── workflows/                     # Pipeline de CI com GitHub Actions
│
├── app/
│   ├── __init__.py
│   ├── main.py                        # FastAPI (/health, /predict e /metrics)
│   └── model.py
│
├── dags/                              # DAGs do Apache Airflow
│
├── data/                              # Dataset de treino e teste
│
├── models/
│   └── medical_classifier.pkl         # Modelo treinado
│
├── monitoring/
│   ├── grafana/
│   │   ├── medical-api-dashboard.json # Dashboard exportado do Grafana
│   │   └── provisioning/
│   │       └── datasources/
│   │           └── prometheus.yml     # Data Source automático do Grafana
│   │
│   └── prometheus.yml                 # Configuração do Prometheus
│
├── scripts/
│   ├── benchmark.py                   # Medição de latência
│   ├── inspect_dataset.py
│   └── train_model.py                 # Treinamento do modelo baseline
│
├── tests/                             # Testes automatizados
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml                 # API + Prometheus + Grafana
├── README.md
└── requirements.txt
```

---

## 📊 Métricas do Modelo Baseline

* **Dataset:** 14.438 resumos médicos (*abstracts*)
* **Modelo:** TF-IDF Vectorizer + Logistic Regression
* **Acurácia:** `55,57%`
* **F1-Score (Weighted):** `0,55`

---

## ⚡ Benchmark de Latência

| Métrica | Tempo (ms) |
| :--- | :--- |
| **Média de Latência** | **8.87 ms** |
| **Menor Tempo** | 2.18 ms |
| **Maior Tempo** | 14.48 ms |

---

# 🛠️ Executando somente a API

Caso seja necessário executar apenas a aplicação FastAPI sem a stack de monitoramento:

### 1. Construir a imagem Docker

```bash
docker build -t medical-classifier-api .
```

### 2. Subir o container

```bash
docker run -d -p 8000:8000 --name medical_api_container medical-classifier-api
```

### 3. Acessar a documentação

Acesse:

```text
http://127.0.0.1:8000/docs
```

### Exemplo de Payload

Endpoint:

```text
POST /predict
```

Payload:

```json
{
  "text": "Does carotid restenosis predict an increased risk of stroke?"
}
```

### 4. Rodar o benchmark de latência

```bash
pip install requests
python scripts/benchmark.py
```

---

# 🚀 Integração Contínua (CI)

Este repositório utiliza **GitHub Actions** para automatizar o pipeline de **Integração Contínua (CI)**.

O objetivo do pipeline é garantir que atualizações da API e do projeto de Machine Learning sejam testadas e validadas automaticamente antes de integrarem a versão final.

Por padrão, o workflow é acionado automaticamente a cada alteração enviada (`push`) para a branch:

```text
main
```

---

## 🛠️ Forçando a Execução do Pipeline Manualmente

Caso seja necessário executar novamente a esteira de CI sem realizar alterações no código, é possível criar um **commit vazio**.

### 1. Clonar o repositório

```bash
git clone https://github.com/Paulinhojr/tech-challenge-nlp.git
```

### 2. Acessar o diretório

```bash
cd tech-challenge-nlp
```

### 3. Criar um commit vazio

```bash
git commit --allow-empty -m "ci: forca execucao do pipeline"
```

### 4. Enviar para a branch principal

```bash
git push origin main
```

---

## 📊 Acompanhamento do CI

Após executar o `git push`, acesse a aba:

```text
Actions
```

do repositório no GitHub.

Uma nova execução do workflow será iniciada.

Durante a execução, o pipeline realizará as validações configuradas no projeto, incluindo:

* configuração do ambiente;
* instalação das dependências;
* análise estática do código;
* execução dos testes automatizados.

Uma execução concluída com sucesso será apresentada com o indicador verde de aprovação no GitHub Actions.

---

# ⚙️ Pipeline de Treinamento — Apache Airflow

O fluxo de treinamento e atualização do modelo de Machine Learning é orquestrado utilizando o **Apache Airflow**.

A DAG principal do projeto automatiza e monitora o processo de criação do modelo preditivo.

A tarefa central executa:

```bash
python scripts/train_model.py
```

## 🔄 Comportamento Esperado

Ao acionar a DAG, o Airflow executará o processo de treinamento utilizando o dataset disponível no projeto.

Após a conclusão da tarefa:

```text
treinar_modelo
```

o modelo final será salvo em:

```text
models/medical_classifier.pkl
```

Esse modelo ficará disponível para ser consumido pela **FastAPI**.

---

# 📈 Monitoramento e Observabilidade

A solução utiliza:

* **FastAPI** para disponibilizar a aplicação;
* **prometheus-client** para instrumentação;
* **Prometheus** para coleta e armazenamento das métricas;
* **Grafana** para visualização.

A arquitetura utilizada é:

```text
FastAPI
   │
   │ /metrics
   ▼
Prometheus
   │
   │ Data Source
   ▼
Grafana
```

---

# 🐳 Executando a Stack Completa

Para executar API, Prometheus e Grafana em conjunto, é necessário possuir **Docker** e **Docker Compose** instalados.

Na raiz do projeto execute:

```bash
docker compose up --build
```

O Docker Compose iniciará automaticamente os três serviços:

```text
FastAPI
Prometheus
Grafana
```

Após a inicialização:

| Serviço | Endereço |
| :--- | :--- |
| FastAPI | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Métricas | http://localhost:8000/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

---

# 🩺 1. Verificando a FastAPI

## Health Check

Acesse:

```text
http://localhost:8000/health
```

Resultado esperado:

```json
{
  "status": "ok"
}
```

---

## Endpoint de Métricas

Acesse:

```text
http://localhost:8000/metrics
```

Entre as métricas disponibilizadas estão:

```text
api_requests_total
api_request_duration_seconds
process_resident_memory_bytes
process_cpu_seconds_total
```

### `api_requests_total`

Registra a quantidade de requisições recebidas pela API, incluindo:

* método HTTP;
* endpoint;
* status HTTP.

### `api_request_duration_seconds`

Registra o tempo gasto pela aplicação para processar as requisições.

As métricas de processo também permitem acompanhar informações como:

* consumo de memória;
* utilização de CPU.

---

# 🔎 2. Verificando o Prometheus

O Prometheus está configurado através do arquivo:

```text
monitoring/prometheus.yml
```

O intervalo de coleta utilizado é de aproximadamente:

```text
5 segundos
```

Acesse:

```text
http://localhost:9090
```

No campo de consulta do Prometheus execute:

```promql
up
```

O resultado esperado é:

```text
up{instance="api:8000", job="medical-api"} 1
```

O valor:

```text
1
```

indica que o Prometheus está conseguindo acessar a FastAPI e coletar as métricas corretamente.

Caso seja exibido:

```text
0
```

o Prometheus reconhece o serviço, porém não está conseguindo acessar a API.

---

# 📊 3. Grafana

Acesse:

```text
http://localhost:3000
```

No primeiro acesso utilize:

```text
Usuário: admin
Senha: admin
```

O Grafana poderá solicitar a criação de uma nova senha.

---

## 🔌 Data Source do Prometheus

O Prometheus **não precisa ser configurado manualmente no Grafana**.

O projeto utiliza o mecanismo de **Provisioning do Grafana** através do arquivo:

```text
monitoring/grafana/provisioning/datasources/prometheus.yml
```

Esse arquivo cria automaticamente o Data Source:

```text
prometheus
```

utilizando internamente:

```text
http://prometheus:9090
```

Caso seja necessário verificar a configuração:

```text
Connections
→ Data sources
→ prometheus
```

---

# 📥 4. Importando o Dashboard

O dashboard utilizado pelo projeto está salvo em:

```text
monitoring/grafana/medical-api-dashboard.json
```

Para importar:

1. Acesse **Dashboards** no Grafana.
2. Clique em **New**.
3. Selecione **Import**.
4. Clique em **Upload dashboard JSON file**.
5. Selecione:

```text
monitoring/grafana/medical-api-dashboard.json
```

6. Clique em **Import**.

O dashboard será criado com o nome:

```text
Medical API - Monitoring
```

Os painéis já estarão configurados para utilizar o Prometheus provisionado pelo projeto.

---

# 📈 5. Painéis do Dashboard

O dashboard possui cinco painéis principais.

## Taxa de Requisições da API

Mostra a taxa de requisições recebidas pela aplicação.

```promql
rate(api_requests_total[$__rate_interval])
```

---

## Latência Média da API

Mostra o tempo médio utilizado para processar as requisições.

```promql
rate(api_request_duration_seconds_sum[1m])
/
rate(api_request_duration_seconds_count[1m])
```

---

## Uso de CPU da API

Mostra o consumo de CPU do processo da aplicação.

```promql
rate(process_cpu_seconds_total{job="medical-api"}[1m]) * 100
```

---

## Uso de Memória da API

Mostra a quantidade de memória RAM residente utilizada pelo processo da aplicação.

```promql
process_resident_memory_bytes{job="medical-api"}
```

---

## Erros da API — Últimos 5 Minutos

Mostra respostas HTTP com status:

```text
4xx
5xx
```

registradas nos últimos cinco minutos.

```promql
sum(increase(api_requests_total{status_code=~"4..|5.."}[5m]))
```

Em uma execução nova, o painel pode inicialmente apresentar:

```text
No data
```

Isso é normal caso nenhuma requisição com erro tenha ocorrido.

---

# 🧪 6. Testando o Painel de Erros

Para validar o monitoramento de erros, é possível gerar propositalmente uma requisição HTTP `404`.

Acesse:

```text
http://localhost:8000/teste
```

A rota `/teste` não existe na aplicação. Portanto, a FastAPI deverá retornar:

```json
{
  "detail": "Not Found"
}
```

com status:

```text
404 Not Found
```

Atualize essa página algumas vezes para gerar múltiplas requisições.

Depois aguarde aproximadamente:

```text
10 a 15 segundos
```

para que o Prometheus realize a coleta.

Volte ao dashboard do Grafana e clique em:

```text
Refresh
```

O painel:

```text
Erros da API - Últimos 5 Minutos
```

deverá começar a apresentar os erros registrados.

---

## Confirmando o erro diretamente no Prometheus

Também é possível consultar diretamente:

```promql
api_requests_total{status_code="404"}
```

Um resultado esperado é semelhante a:

```text
api_requests_total{
    endpoint="/teste",
    method="GET",
    status_code="404"
} 5
```

O número apresentado representa a quantidade de requisições registradas para aquela série.

---

# ✅ Validação Final

Para confirmar o funcionamento completo do ambiente:

```text
FastAPI /health       → status "ok"

FastAPI /metrics      → métricas disponíveis

Prometheus
up                    → valor 1

Grafana
Taxa de Requisições   → apresenta dados
Latência Média        → apresenta dados
Uso de CPU            → apresenta dados
Uso de Memória        → apresenta dados

/teste
Erro HTTP 404         → registrado no painel de erros
```

Com esses testes concluídos, a comunicação entre:

```text
FastAPI → Prometheus → Grafana
```

está funcionando corretamente.
