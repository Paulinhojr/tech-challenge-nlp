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

# 📊 Grafana

O Grafana é utilizado para visualizar graficamente as métricas coletadas pelo Prometheus.

Acesse:

```text
http://localhost:3000
```

No primeiro acesso, utilize as credenciais padrão:

```text
Usuário: admin
Senha: admin
```

O Grafana poderá solicitar a alteração da senha no primeiro login.

---

## 🔌 Configurando o Prometheus como Data Source

Dentro do Grafana:

1. Acesse **Connections**.
2. Entre em **Data Sources**.
3. Selecione **Prometheus**.
4. Configure o endereço:

```text
http://prometheus:9090
```

5. Clique em:

```text
Save & Test
```

O resultado esperado é uma mensagem semelhante a:

```text
Successfully queried the Prometheus API.
```

> Importante: dentro do Docker Compose deve ser utilizado `prometheus:9090` e não `localhost:9090`, pois Grafana e Prometheus estão sendo executados em containers diferentes.

---

# 📊 Dashboard de Monitoramento

O dashboard criado para o projeto contém cinco painéis principais:

### 1. Taxa de Requisições da API

Mostra a quantidade de requisições recebidas ao longo do tempo.

```promql
rate(api_requests_total[$__rate_interval])
```

---

### 2. Latência Média da API

Mostra o tempo médio gasto no processamento das requisições.

```promql
rate(api_request_duration_seconds_sum[1m])
/
rate(api_request_duration_seconds_count[1m])
```

---

### 3. Erros da API — Últimos 5 Minutos

Monitora respostas HTTP de erro das categorias:

```text
4xx
5xx
```

Consulta utilizada:

```promql
sum(increase(api_requests_total{status_code=~"4..|5.."}[5m]))
```

Para gerar um erro de teste é possível acessar uma rota inexistente:

```text
http://localhost:8000/teste
```

A FastAPI deverá retornar:

```json
{
  "detail": "Not Found"
}
```

com status HTTP:

```text
404
```

Após alguns segundos o erro será coletado pelo Prometheus e poderá ser visualizado no Grafana.

---

### 4. Uso de Memória da API

Monitora aproximadamente a memória RAM residente utilizada pelo processo Python da FastAPI.

```promql
process_resident_memory_bytes{job="medical-api"}
```

A unidade utilizada no Grafana é:

```text
Data / bytes (IEC)
```

permitindo a exibição automática em **MiB**.

---

### 5. Uso de CPU da API

Monitora o consumo de CPU do processo da aplicação.

```promql
rate(process_cpu_seconds_total{job="medical-api"}[1m]) * 100
```

A unidade configurada no Grafana é:

```text
Percent (0-100)
```

---

# 💾 Dashboard Versionado

O dashboard do Grafana também foi exportado em formato JSON para permitir o versionamento da configuração junto ao código do projeto.

O arquivo está localizado em:

```text
monitoring/grafana/medical-api-dashboard.json
```

Isso permite preservar as configurações e consultas utilizadas no dashboard mesmo que o ambiente Docker seja recriado.

---

# ✅ Validação Completa da Stack de Observabilidade

Após executar:

```bash
docker compose up --build
```

realize as seguintes verificações.

### 1. API

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

### 2. Métricas

Acesse:

```text
http://localhost:8000/metrics
```

Devem aparecer métricas como:

```text
api_requests_total
api_request_duration_seconds
```

---

### 3. Prometheus

Acesse:

```text
http://localhost:9090
```

Execute:

```promql
up
```

Resultado esperado:

```text
up{instance="api:8000", job="medical-api"} 1
```

---

### 4. Grafana

Acesse:

```text
http://localhost:3000
```

Configure o Prometheus como Data Source utilizando:

```text
http://prometheus:9090
```

Após a configuração, o dashboard poderá visualizar as métricas coletadas pela aplicação.

---

# 🔄 Fluxo Completo de Observabilidade

```text
Usuário
   │
   ▼
FastAPI
   │
   ├── /health
   ├── /predict
   └── /metrics
          │
          ▼
     Prometheus
          │
          ▼
       Grafana
          │
          ▼
     Dashboard
```

A stack permite acompanhar o comportamento da aplicação através de métricas de **requisições, latência, erros, memória e CPU**, oferecendo uma camada básica de observabilidade para o serviço de inferência.