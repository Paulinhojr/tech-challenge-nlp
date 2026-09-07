---

### 🚀 Recomendação de Infraestrutura em Nuvem (AWS / GCP / Azure)

Para este projeto, a provedora recomendada é a **AWS** (ou equivalentemente **GCP/Azure**), utilizando serviços gerenciados e serverless para otimizar custos e manutenção:

#### Opção A: Serverless com AWS Lambda + Amazon ECR (Recomendado para início/baixo custo)

* **Arquitetura:** Empacotar a imagem Docker da API no **Amazon ECR** e executá-la através do **AWS Lambda** integrado ao **Amazon API Gateway**.
* **Vantagens:**
  * Custo zero enquanto não houver requisições (cobrança por milissegundos de execução).
  * Auto-scaling automático conforme a demanda de requisições aumenta.
  * O footprint do modelo (`TF-IDF + Logistic Regression`) é extremamente leve e roda perfeitamente em limites serverless.

#### Opção B: Containers Gerenciados com AWS App Runner / Amazon ECS (Recomendado para tráfego constante)

* **Arquitetura:** Subir a imagem Docker diretamente no **AWS App Runner** ou **Amazon ECS (Fargate)**.
* **Vantagens:**
  * Mantém o container sempre quente (*warm start*), eliminando latências iniciais (*cold start*).
  * Ideal para ambientes hospitalares ou clínicas onde o fluxo de consultas de textos médicos ocorre durante todo o dia útil.

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
│   └── workflows/                 # Pipeline de CI com GitHub Actions
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI (/health, /predict e /metrics)
│   └── model.py
│
├── dags/                          # DAGs do Apache Airflow
│
├── data/                          # Dataset de treino e teste
│
├── models/
│   └── medical_classifier.pkl     # Modelo treinado
│
├── monitoring/
│   ├── grafana/
│   │   └── medical-api-dashboard.json
│   └── prometheus.yml
│
├── scripts/
│   ├── benchmark.py               # Medição de latência
│   ├── inspect_dataset.py
│   └── train_model.py             # Treinamento do modelo baseline
│
├── tests/                         # Testes automatizados
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml             # API + Prometheus + Grafana
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

Acesse:

```text
http://127.0.0.1:8000/docs
```

**Exemplo de Payload (`POST /predict`):**

```json
{
  "text": "Does carotid restenosis predict an increased risk of stroke?"
}
```

### 4. Rodar o Benchmark de Latência

```bash
pip install requests
python scripts/benchmark.py
```

---

### 🚀 Integração Contínua (CI) — Medical Text Classification API

Este repositório utiliza **GitHub Actions** para automatizar o pipeline de **Integração Contínua (CI)**.

O objetivo do pipeline é garantir que as atualizações da API de classificação de textos médicos e os modelos de Machine Learning sejam testados e validados automaticamente antes de integrarem a versão final.

Por padrão, o workflow é acionado automaticamente a cada alteração enviada (`push`) para a branch `main`.

---

### 🛠️ Como Forçar a Execução do Pipeline Manualmente

Caso seja necessário testar a esteira de Integração Contínua (CI) para validar as configurações, sem realizar alterações no código da aplicação, é possível utilizar um **commit vazio (`empty commit`)**.

#### 1. Clonar o repositório

```bash
git clone https://github.com/Paulinhojr/tech-challenge-nlp.git
```

#### 2. Acessar o diretório do projeto

```bash
cd tech-challenge-nlp
```

#### 3. Adicionar os arquivos ao staging

```bash
git add .
```

#### 4. Criar o commit de acionamento

O parâmetro `--allow-empty` permite criar um commit sem modificar nenhum arquivo do projeto.

```bash
git commit --allow-empty -m "ci: forca execucao do pipeline"
```

#### 5. Enviar para a branch principal

```bash
git push origin main
```

---

### 📊 Acompanhamento

Após executar o comando `git push`, acesse a aba **Actions** do repositório no GitHub.

Uma nova execução do workflow será iniciada com o commit:

```text
ci: forca execucao do pipeline
```

Durante a execução, o pipeline realizará as validações configuradas no projeto, incluindo a configuração do ambiente, instalação das dependências, análise estática do código e execução dos testes automatizados.

Uma execução concluída com sucesso será apresentada com o indicador verde de aprovação no GitHub Actions.

---

### ⚙️ Pipeline de Treinamento (Airflow DAG)

O fluxo de treinamento e atualização do modelo de Machine Learning é orquestrado utilizando o **Apache Airflow**.

A DAG principal do projeto foi desenvolvida para automatizar e monitorar o processo de criação do modelo preditivo.

A tarefa central do pipeline executa o script Python responsável pelo treinamento:

```bash
python scripts/train_model.py
```

#### 🔄 Comportamento Esperado

Ao acionar a DAG, o Airflow executará o processo de treinamento utilizando o dataset disponível no projeto.

Após a conclusão bem-sucedida da tarefa `treinar_modelo`, o modelo final:

```text
models/medical_classifier.pkl
```

será gerado e ficará disponível para ser consumido pela **FastAPI**.

O fluxo permite integrar o processo de treinamento do modelo à camada de orquestração do projeto, mantendo o processo organizado e automatizado.

---

# 📈 Monitoramento e Observabilidade — Prometheus + Grafana

A API foi instrumentada utilizando a biblioteca **prometheus-client**, permitindo coletar métricas relacionadas ao funcionamento e ao desempenho da aplicação.

As métricas são disponibilizadas através do endpoint:

```text
http://localhost:8000/metrics
```

O **Prometheus** coleta periodicamente essas informações e o **Grafana** utiliza o Prometheus como fonte de dados para disponibilizar as métricas através de dashboards.

A arquitetura de observabilidade utilizada no projeto é:

```text
                 ┌──────────────────┐
                 │     FastAPI      │
                 │                  │
                 │     /metrics     │
                 └────────┬─────────┘
                          │
                          │ coleta de métricas
                          ▼
                 ┌──────────────────┐
                 │    Prometheus    │
                 │    Porta 9090    │
                 └────────┬─────────┘
                          │
                          │ Data Source
                          ▼
                 ┌──────────────────┐
                 │     Grafana      │
                 │    Porta 3000    │
                 └──────────────────┘
```

---

## 🐳 Executando a Stack Completa de Monitoramento

Para executar a stack é necessário possuir **Docker** e **Docker Compose** instalados e em execução.

Na raiz do projeto execute:

```bash
docker compose up --build
```

O Docker Compose irá iniciar automaticamente os três serviços:

* **FastAPI**
* **Prometheus**
* **Grafana**

Após a inicialização, os serviços estarão disponíveis nos seguintes endereços:

| Serviço | Endereço |
| :--- | :--- |
| FastAPI | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Métricas da API | http://localhost:8000/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

Para finalizar toda a stack:

```bash
docker compose down
```

---

## 🩺 Health Check

Para verificar se a API está funcionando corretamente, acesse:

```text
http://localhost:8000/health
```

O resultado esperado é:

```json
{
  "status": "ok"
}
```

---

## 📡 Endpoint de Métricas

As métricas da aplicação podem ser visualizadas diretamente através de:

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

A métrica:

```text
api_requests_total
```

registra a quantidade de requisições recebidas pela API, incluindo:

* método HTTP;
* endpoint;
* status HTTP.

A métrica:

```text
api_request_duration_seconds
```

registra o tempo gasto para processar as requisições.

---

# 🔎 Prometheus

O Prometheus está configurado para coletar automaticamente as métricas da FastAPI.

O arquivo responsável pela configuração está disponível em:

```text
monitoring/prometheus.yml
```

O intervalo de coleta configurado é de aproximadamente **5 segundos**.

---

## ✅ Verificando a Comunicação Prometheus → API

Acesse:

```text
http://localhost:9090
```

No campo de consulta do Prometheus execute:

```promql
up
```

O resultado esperado é semelhante a:

```text
up{instance="api:8000", job="medical-api"} 1
```

O valor:

```text
1
```

indica que o Prometheus consegue acessar a FastAPI e coletar as métricas corretamente.

Caso o valor seja:

```text
0
```

significa que o Prometheus reconhece o serviço, porém não está conseguindo acessá-lo.

---

# 📈 Monitoramento e Observabilidade — Prometheus + Grafana

A API foi instrumentada com a biblioteca **prometheus-client** para disponibilizar métricas de funcionamento e desempenho.

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

O **Prometheus** coleta as métricas expostas pela FastAPI e o **Grafana** utiliza essas informações para apresentar os dados em um dashboard.

---

## 🐳 Executando a Stack de Monitoramento

É necessário possuir **Docker** e **Docker Compose** instalados e em execução.

Na raiz do projeto, execute:

```bash
docker compose up --build
```

O Docker Compose iniciará automaticamente:

- **FastAPI**
- **Prometheus**
- **Grafana**

Os serviços estarão disponíveis em:

| Serviço | Endereço |
| :--- | :--- |
| FastAPI | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Métricas | http://localhost:8000/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

Para encerrar a stack:

```bash
docker compose down
```

---

## 🩺 1. Verificando a API

### Health Check

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

### Endpoint de Métricas

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

A métrica `api_requests_total` registra a quantidade de requisições recebidas pela API, incluindo método HTTP, endpoint e status da resposta.

A métrica `api_request_duration_seconds` registra o tempo utilizado para processar as requisições.

---

## 🔎 2. Verificando o Prometheus

O Prometheus está configurado através do arquivo:

```text
monitoring/prometheus.yml
```

O intervalo de coleta configurado é de aproximadamente **5 segundos**.

Acesse:

```text
http://localhost:9090
```

No campo de consulta, execute:

```promql
up
```

O resultado esperado é semelhante a:

```text
up{instance="api:8000", job="medical-api"} 1
```

O valor `1` indica que o Prometheus está conseguindo acessar a FastAPI e coletar suas métricas corretamente.

---

## 📊 3. Acessando o Grafana

Acesse:

```text
http://localhost:3000
```

No primeiro acesso, utilize:

```text
Usuário: admin
Senha: admin
```

O Grafana poderá solicitar a criação de uma nova senha.

---

### 🔌 Data Source do Prometheus

Não é necessário configurar o Prometheus manualmente.

O projeto utiliza o mecanismo de **Provisioning do Grafana**, através do arquivo:

```text
monitoring/grafana/provisioning/datasources/prometheus.yml
```

Esse arquivo cadastra automaticamente o Data Source:

```text
prometheus
```

utilizando o endereço interno:

```text
http://prometheus:9090
```

Caso queira verificar a configuração no Grafana:

```text
Connections
→ Data sources
→ prometheus
```

---

## 📥 4. Importando o Dashboard

O dashboard está disponível em:

```text
monitoring/grafana/medical-api-dashboard.json
```

Para importar:

1. Acesse **Dashboards**.
2. Clique em **New**.
3. Selecione **Import**.
4. Clique em **Upload dashboard JSON file**.
5. Selecione:

```text
monitoring/grafana/medical-api-dashboard.json
```

6. Clique em **Import**.

O dashboard:

```text
Medical API - Monitoring
```

será criado com os painéis já configurados.

---

## 📈 5. Métricas do Dashboard

O dashboard possui cinco painéis.

### Taxa de Requisições da API

```promql
rate(api_requests_total[$__rate_interval])
```

Apresenta a taxa de requisições recebidas pela aplicação.

### Latência Média da API

```promql
rate(api_request_duration_seconds_sum[1m])
/
rate(api_request_duration_seconds_count[1m])
```

Apresenta o tempo médio utilizado pela API para processar as requisições.

### Uso de CPU da API

```promql
rate(process_cpu_seconds_total{job="medical-api"}[1m]) * 100
```

Apresenta o consumo de CPU do processo da aplicação.

### Uso de Memória da API

```promql
process_resident_memory_bytes{job="medical-api"}
```

Apresenta a quantidade de memória RAM utilizada pelo processo da API.

### Erros da API — Últimos 5 Minutos

```promql
sum(increase(api_requests_total{status_code=~"4..|5.."}[5m]))
```

Apresenta a quantidade de respostas HTTP `4xx` e `5xx` registradas nos últimos cinco minutos.

Em uma execução nova, esse painel pode inicialmente apresentar:

```text
No data
```

Isso é esperado caso nenhum erro tenha ocorrido.

---

## 🧪 6. Testando o Monitoramento de Erros

Para testar o painel de erros, gere propositalmente uma requisição `404`.

Acesse:

```text
http://localhost:8000/teste
```

Como a rota `/teste` não existe, a FastAPI deverá retornar:

```json
{
  "detail": "Not Found"
}
```

com status:

```text
404 Not Found
```

Atualize a página algumas vezes para gerar múltiplas requisições com erro.

Depois aguarde aproximadamente **10 a 15 segundos** para que o Prometheus realize a coleta.

Volte ao Grafana e clique em:

```text
Refresh
```

O painel:

```text
Erros da API - Últimos 5 Minutos
```

deverá apresentar os erros registrados.

Também é possível confirmar diretamente no Prometheus com:

```promql
api_requests_total{status_code="404"}
```

Exemplo de resultado:

```text
api_requests_total{
    endpoint="/teste",
    method="GET",
    status_code="404"
} 5
```

---

## ✅ 7. Validação Final

Ao final, o comportamento esperado é:

```text
FastAPI /health                      → funcionando
FastAPI /metrics                     → funcionando
Prometheus up                        → valor 1
Taxa de Requisições                  → apresenta dados
Latência Média                       → apresenta dados
Uso de CPU                           → apresenta dados
Uso de Memória                       → apresenta dados
Erros da API                         → apresenta dados após gerar erros 404
```

### Resumo para reprodução

```text
1. docker compose up --build

2. Testar:
   http://localhost:8000/health
   http://localhost:8000/metrics

3. Acessar:
   http://localhost:9090

   Executar:
   up

4. Acessar:
   http://localhost:3000

5. Login:
   admin / admin

6. Dashboards
   → New
   → Import

7. Selecionar:
   monitoring/grafana/medical-api-dashboard.json

8. Para testar erros:
   http://localhost:8000/teste

9. Aguardar alguns segundos e atualizar o Grafana.
```

O Data Source do Prometheus é configurado automaticamente pelo projeto, portanto nenhuma configuração manual adicional é necessária.
