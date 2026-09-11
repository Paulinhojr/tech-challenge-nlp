from pathlib import Path

import joblib

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "medical_classifier.pkl"
ONNX_PATH = BASE_DIR / "models" / "medical_classifier.onnx"


print("Carregando modelo original...")

model = joblib.load(MODEL_PATH)

print("Modelo carregado.")
print("Convertendo para ONNX...")


initial_type = [
    ("input", StringTensorType([None, 1]))
]


onnx_model = convert_sklearn(
    model,
    initial_types=initial_type,
)


with open(ONNX_PATH, "wb") as file:
    file.write(onnx_model.SerializeToString())


print("Conversão concluída.")
print(f"Modelo ONNX salvo em: {ONNX_PATH}")