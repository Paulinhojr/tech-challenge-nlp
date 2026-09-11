from pathlib import Path

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

PKL_PATH = BASE_DIR / "models" / "medical_classifier.pkl"
ONNX_PATH = BASE_DIR / "models" / "medical_classifier.onnx"
TEST_PATH = BASE_DIR / "data" / "medical_tc_test.csv"


# =========================
# Carregar modelo original
# =========================

print("Carregando modelo original...")

sklearn_model = joblib.load(PKL_PATH)


# =========================
# Carregar modelo ONNX
# =========================

print("Carregando modelo ONNX...")

onnx_session = ort.InferenceSession(
    str(ONNX_PATH),
    providers=["CPUExecutionProvider"],
)

input_name = onnx_session.get_inputs()[0].name

print(f"Entrada ONNX: {input_name}")

print("Saídas ONNX:")
for output in onnx_session.get_outputs():
    print(f"- {output.name}")


# =========================
# Carregar dados de teste
# =========================

test_df = pd.read_csv(TEST_PATH)

# Vamos começar com 100 exemplos
texts = test_df["medical_abstract"]
y_true = test_df["condition_label"]


# =========================
# Predição Scikit-learn
# =========================

sklearn_predictions = sklearn_model.predict(texts)


# =========================
# Predição ONNX
# =========================

onnx_input = np.array(
    texts.tolist(),
    dtype=object,
).reshape(-1, 1)

onnx_outputs = onnx_session.run(
    None,
    {input_name: onnx_input},
)

onnx_predictions = np.array(onnx_outputs[0])


# =========================
# Comparação
# =========================

matches = sklearn_predictions == onnx_predictions

agreement = matches.mean() * 100


print("\n=========================")
print("COMPARAÇÃO DOS MODELOS")
print("=========================")

print(f"Predições comparadas: {len(texts)}")
print(f"Predições iguais: {matches.sum()}")
print(f"Concordância: {agreement:.2f}%")

print("\nPrimeiras 10 previsões:")

for i in range(10):
    print(
        f"{i + 1}: "
        f"PKL={sklearn_predictions[i]} | "
        f"ONNX={onnx_predictions[i]}"
    )

print("\nRESULTADO FINAL")
print(f"Predições comparadas: {len(texts)}")
print(f"Predições iguais: {matches.sum()}")
print(f"Concordância: {agreement:.2f}%")

print("\nDIVERGÊNCIAS")

for i, match in enumerate(matches):
    if not match:
        print(f"\nÍndice: {i}")
        print(f"PKL: {sklearn_predictions[i]}")
        print(f"ONNX: {onnx_predictions[i]}")
        print(f"Texto: {texts.iloc[i]}")

sklearn_accuracy = (
    sklearn_predictions == y_true.to_numpy()
).mean() * 100

onnx_accuracy = (
    onnx_predictions == y_true.to_numpy()
).mean() * 100

print("\nACURÁCIA NO CONJUNTO DE TESTE")
print(f"PKL:  {sklearn_accuracy:.2f}%")
print(f"ONNX: {onnx_accuracy:.2f}%")