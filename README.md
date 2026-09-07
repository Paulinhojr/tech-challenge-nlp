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

# 📊 Grafana — Dashboard de Monitoramento

O **Grafana** é utilizado para visualizar de forma gráfica as métricas coletadas pelo Prometheus.

Neste projeto, o Grafana é iniciado automaticamente pelo Docker Compose e o **Prometheus já é configurado como Data Source automaticamente** através do mecanismo de provisioning.

Portanto, não é necessário cadastrar manualmente o Prometheus dentro do Grafana.

---

## 🚀 1. Iniciar o ambiente

Na raiz do projeto, execute:

```bash
docker compose up --build
```

Esse comando inicia os três serviços utilizados no monitoramento:

```text
FastAPI      → http://localhost:8000
Prometheus   → http://localhost:9090
Grafana      → http://localhost:3000
```

Aguarde alguns segundos até que todos os containers estejam inicializados.

---

## 🔐 2. Acessar o Grafana

Abra no navegador:

```text
http://localhost:3000
```

No primeiro acesso, utilize:

```text
Usuário: admin
Senha: admin
```

O Grafana poderá solicitar a criação de uma nova senha.

Caso apareça a opção de pular essa etapa, ela também pode ser utilizada.

---

## 🔌 3. Prometheus configurado automaticamente

O projeto já contém o arquivo responsável por cadastrar automaticamente o Prometheus no Grafana:

```text
monitoring/grafana/provisioning/datasources/prometheus.yml
```

O Data Source criado automaticamente possui o nome:

```text
prometheus
```

e utiliza internamente o endereço:

```text
http://prometheus:9090
```

Caso queira confirmar a configuração dentro do Grafana, acesse:

```text
Connections
→ Data sources
→ prometheus
```

O Prometheus deverá aparecer automaticamente.

Não é necessário criar um novo Data Source manualmente.

---

# 📥 4. Importar o Dashboard

O dashboard utilizado no projeto está salvo e versionado no arquivo:

```text
monitoring/grafana/medical-api-dashboard.json
```

Para importar:

1. No menu lateral do Grafana, clique em **Dashboards**.
2. Clique em **New**.
3. Selecione **Import**.
4. Clique em **Upload dashboard JSON file**.
5. Navegue até:

```text
monitoring/grafana/medical-api-dashboard.json
```

6. Selecione o arquivo.
7. O Grafana deverá identificar automaticamente o dashboard:

```text
Medical API - Monitoring
```

8. Clique em:

```text
Import
```

Após a importação, os painéis aparecerão automaticamente no dashboard.

---

# 📈 5. Painéis do Dashboard

O dashboard possui cinco painéis principais.

### Taxa de Requisições da API

Mostra a taxa de requisições recebidas pela aplicação ao longo do tempo.

```promql
rate(api_requests_total[$__rate_interval])
```

---

### Latência Média da API

Mostra o tempo médio necessário para a API processar as requisições.

```promql
rate(api_request_duration_seconds_sum[1m])
/
rate(api_request_duration_seconds_count[1m])
```

---

### Uso de CPU da API

Mostra aproximadamente o consumo de CPU do processo responsável pela API.

```promql
rate(process_cpu_seconds_total{job="medical-api"}[1m]) * 100
```

A unidade utilizada no Grafana é:

```text
Percent (0-100)
```

---

### Uso de Memória da API

Mostra a quantidade de memória RAM residente utilizada pelo processo Python da aplicação.

```promql
process_resident_memory_bytes{job="medical-api"}
```

A unidade configurada é:

```text
Data / bytes (IEC)
```

permitindo ao Grafana converter automaticamente os valores para KiB, MiB ou GiB.

---

### Erros da API — Últimos 5 Minutos

Esse painel mostra a quantidade de respostas HTTP com status:

```text
4xx
5xx
```

registradas nos últimos cinco minutos.

A consulta utilizada é:

```promql
sum(increase(api_requests_total{status_code=~"4..|5.."}[5m]))
```

Em uma execução nova do projeto, esse painel pode aparecer inicialmente como:

```text
No data
```

Isso é normal.

Significa apenas que ainda não ocorreu nenhuma requisição com erro.

---

# 🧪 6. Testar o Painel de Erros

Para verificar se o monitoramento de erros está funcionando, podemos gerar propositalmente uma requisição HTTP `404`.

Abra no navegador:

```text
http://localhost:8000/teste
```

Como a rota `/teste` não existe na aplicação, a FastAPI deverá retornar:

```json
{
  "detail": "Not Found"
}
```

com o código HTTP:

```text
404 Not Found
```

Acesse essa URL algumas vezes ou pressione `F5` algumas vezes para gerar múltiplos erros.

Exemplo:

```text
http://localhost:8000/teste
http://localhost:8000/teste
http://localhost:8000/teste
```

Depois aguarde aproximadamente **10 a 15 segundos**, pois o Prometheus realiza a coleta das métricas periodicamente.

Volte ao dashboard do Grafana e clique em:

```text
Refresh
```

O painel:

```text
Erros da API - Últimos 5 Minutos
```

deverá começar a apresentar a quantidade de erros registrados.

---

# 🔎 7. Confirmar os erros diretamente no Prometheus

Também é possível verificar diretamente no Prometheus se os erros `404` foram registrados.

Acesse:

```text
http://localhost:9090
```

Execute a consulta:

```promql
api_requests_total{status_code="404"}
```

O Prometheus deverá apresentar algo semelhante a:

```text
api_requests_total{
    endpoint="/teste",
    method="GET",
    status_code="404"
} 5
```

O número final representa a quantidade de requisições `404` registradas para aquela rota.

---

# ✅ 8. Validação final do Dashboard

Após iniciar a aplicação e importar o dashboard, o comportamento esperado é:

```text
Taxa de Requisições da API       → apresenta dados
Latência Média da API            → apresenta dados
Uso de CPU da API                → apresenta dados
Uso de Memória da API            → apresenta dados
Erros da API - Últimos 5 Minutos → apresenta dados após gerar erros 404
```

Caso algum gráfico ainda esteja vazio, aguarde alguns segundos e clique em:

```text
Refresh
```

no canto superior direito do dashboard.

---

# 🔄 Fluxo completo do monitoramento

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
Medical API - Monitoring
```

Com isso, o processo de reprodução do monitoramento é:

```text
1. docker compose up --build

2. Abrir:
   http://localhost:3000

3. Login:
   admin / admin

4. Dashboards
   → New
   → Import

5. Selecionar:
   monitoring/grafana/medical-api-dashboard.json

6. Importar o dashboard

7. Para testar erros:
   http://localhost:8000/teste

8. Aguardar alguns segundos e clicar em Refresh
```

O Prometheus já é configurado automaticamente pelo projeto, portanto não é necessário realizar nenhuma configuração manual adicional de Data Source no Grafana.
