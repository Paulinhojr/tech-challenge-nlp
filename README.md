

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
pip install requests
python scripts/benchmark.py
```
### 🚀 Integração Contínua (CI) — Medical Text Classification API

Este repositório utiliza **GitHub Actions** para automatizar o pipeline de **Integração Contínua (CI)**. O objetivo do pipeline é garantir que as atualizações da nossa API de classificação de textos médicos e os modelos de Machine Learning sejam testados e validados automaticamente antes de integrarem a versão final.

Por padrão, o workflow é acionado automaticamente a cada alteração enviada (`push`) para a branch `main`.

---

### 🛠️ Como Forçar a Execução do Pipeline Manualmente

Caso seja necessário testar a esteira de CI/CD para validar as configurações, sem realizar alterações no código da aplicação, é possível utilizar um **commit vazio (`empty commit`)**.

#### 1. Clonar o repositório

Caso o projeto ainda não esteja disponível localmente, execute:

```bash
git clone https://github.com/Paulinhojr/tech-challenge-nlp.git
```

#### 2. Acessar o diretório do projeto

No terminal integrado do VS Code:

```bash
cd tech-challenge-nlp
```

#### 3. Adicionar os arquivos ao staging

```bash
git add .
```

#### 4. Criar o commit de acionamento

O parâmetro `--allow-empty` permite criar um commit sem modificar nenhum arquivo do projeto. Esse commit será utilizado para disparar o workflow do GitHub Actions:

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
