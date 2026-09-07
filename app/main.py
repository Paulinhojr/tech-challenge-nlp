from pathlib import Path
import time

import joblib
import pandas as pd
from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel


# =========================
# Configuração dos caminhos
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "medical_classifier.pkl"
LABELS_PATH = BASE_DIR / "data" / "medical_tc_labels.csv"


# =========================
# Carregamento do modelo
# =========================

model = joblib.load(MODEL_PATH)

labels_df = pd.read_csv(LABELS_PATH)

label_mapping = dict(
    zip(
        labels_df["condition_label"],
        labels_df["condition_name"],
    )
)


# =========================
# Criação da API
# =========================

app = FastAPI(
    title="Medical Abstract Classification API",
    description="API para classificação de abstracts médicos.",
    version="1.0.0",
)


# =========================
# Modelo da requisição
# =========================

class PredictionRequest(BaseModel):
    text: str


# =========================
# Prometheus metrics
# =========================

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total de requisições recebidas pela API",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "Tempo de resposta das requisições da API",
    ["endpoint"],
)


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.url.path,
    ).observe(duration)

    return response


# =========================
# Métricas Prometheus
# =========================

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


# =========================
# Health check
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================
# Predição
# =========================

@app.post("/predict")
def predict(request: PredictionRequest):
    prediction = model.predict([request.text])[0]

    classification = label_mapping[prediction]

    return {
        "classification": classification
    }