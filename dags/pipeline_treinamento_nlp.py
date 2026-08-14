import os
import subprocess
from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.operators.python import PythonOperator

# Caminho da raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# -----------------------------
# 1. Verificação dos dados
# -----------------------------
def preparar_dados():
    print("Verificando arquivos de dados...")

    arquivos = [
        "medical_tc_train.csv",
        "medical_tc_test.csv",
        "medical_tc_labels.csv",
    ]

    for arquivo in arquivos:
        caminho = os.path.join(BASE_DIR, "data", arquivo)

        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        print(f"OK: {arquivo}")

    print("Todos os arquivos de dados foram encontrados.")


# -----------------------------
# 2. Treinamento do modelo
# -----------------------------
def treinar_modelo():
    print("Executando scripts/train_model.py ...")

    script = os.path.join(BASE_DIR, "scripts", "train_model.py")

    subprocess.run(
        ["python", script],
        cwd=BASE_DIR,
        check=True,
    )

    print("Treinamento finalizado.")


# -----------------------------
# 3. Validação do modelo salvo
# -----------------------------
def salvar_modelo():
    modelo = os.path.join(BASE_DIR, "models", "medical_classifier.pkl")

    if os.path.exists(modelo):
        tamanho = os.path.getsize(modelo)

        print(f"Modelo salvo com sucesso em: {modelo}")
        print(f"Tamanho do arquivo: {tamanho} bytes")
    else:
        raise FileNotFoundError(
            "O arquivo medical_classifier.pkl não foi gerado."
        )


# -----------------------------
# Configurações da DAG
# -----------------------------
default_args = {
    "owner": "engenharia_dados",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1, tzinfo=timezone.utc),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="pipeline_treinamento_nlp",
    default_args=default_args,
    description="Pipeline automatizado de treinamento do modelo NLP",
    schedule=timedelta(days=1),
    catchup=False,
    tags=["mlops", "nlp", "tech-challenge"],
) as dag:

    task_preparar = PythonOperator(
        task_id="preparar_dados",
        python_callable=preparar_dados,
    )

    task_treinar = PythonOperator(
        task_id="treinar_modelo",
        python_callable=treinar_modelo,
    )

    task_salvar = PythonOperator(
        task_id="salvar_modelo",
        python_callable=salvar_modelo,
    )

    task_preparar >> task_treinar >> task_salvar

