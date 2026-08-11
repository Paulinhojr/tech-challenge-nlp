from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
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
        labels_df["condition_name"]
    )
)


# =========================
# Criação da API
# =========================

app = FastAPI(
    title="Medical Abstract Classification API",
    description="API para classificação de abstracts médicos.",
    version="1.0.0"
)


# =========================
# Modelo da requisição
# =========================

class PredictionRequest(BaseModel):
    text: str


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