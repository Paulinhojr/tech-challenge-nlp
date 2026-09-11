from pathlib import Path
import time

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

PKL_PATH = BASE_DIR / "models" / "medical_classifier.pkl"
ONNX_PATH = BASE_DIR / "models" / "medical_classifier.onnx"
TEST_PATH = BASE_DIR / "data" / "medical_tc_test.csv"


# =========================
# Carregamento dos modelos
# =========================

print("Carregando modelos...")

sklearn_model = joblib.load(PKL_PATH)

onnx_session = ort.InferenceSession(
    str(ONNX_PATH),
    providers=["CPUExecutionProvider"],
)

input_name = onnx_session.get_inputs()[0].name


# =========================
# Dados de teste
# =========================

test_df = pd.read_csv(TEST_PATH)

# 500 textos para o benchmark
texts = test_df["medical_abstract"].head(500).tolist()


# =========================
# Warm-up
# =========================

print("Executando warm-up...")

for text in texts[:20]:
    sklearn_model.predict([text])

    onnx_input = np.array(
        [[text]],
        dtype=object,
    )

    onnx_session.run(
        None,
        {input_name: onnx_input},
    )


# =========================
# Benchmark PKL
# =========================

print("Testando modelo PKL...")

pkl_times = []

for text in texts:

    start = time.perf_counter()

    sklearn_model.predict([text])

    end = time.perf_counter()

    pkl_times.append(
        (end - start) * 1000
    )


# =========================
# Benchmark ONNX
# =========================

print("Testando modelo ONNX...")

onnx_times = []

for text in texts:

    onnx_input = np.array(
        [[text]],
        dtype=object,
    )

    start = time.perf_counter()

    onnx_session.run(
        None,
        {input_name: onnx_input},
    )

    end = time.perf_counter()

    onnx_times.append(
        (end - start) * 1000
    )


# =========================
# Estatísticas
# =========================

pkl_times = np.array(pkl_times)
onnx_times = np.array(onnx_times)


pkl_mean = pkl_times.mean()
onnx_mean = onnx_times.mean()

gain = (
    (pkl_mean - onnx_mean)
    / pkl_mean
) * 100


# =========================
# Tamanho dos arquivos
# =========================

pkl_size = PKL_PATH.stat().st_size / (1024 * 1024)
onnx_size = ONNX_PATH.stat().st_size / (1024 * 1024)


# =========================
# Resultado
# =========================

print("\n=========================")
print("BENCHMARK PKL VS ONNX")
print("=========================")

print("\nPKL")
print(f"Média:   {pkl_mean:.3f} ms")
print(f"Mediana: {np.median(pkl_times):.3f} ms")
print(f"Mínimo:  {pkl_times.min():.3f} ms")
print(f"Máximo:  {pkl_times.max():.3f} ms")
print(f"P95:     {np.percentile(pkl_times, 95):.3f} ms")

print("\nONNX")
print(f"Média:   {onnx_mean:.3f} ms")
print(f"Mediana: {np.median(onnx_times):.3f} ms")
print(f"Mínimo:  {onnx_times.min():.3f} ms")
print(f"Máximo:  {onnx_times.max():.3f} ms")
print(f"P95:     {np.percentile(onnx_times, 95):.3f} ms")

print("\nGANHO DE DESEMPENHO")
print(f"{gain:.2f}%")

print("\nTAMANHO DOS MODELOS")
print(f"PKL:  {pkl_size:.2f} MB")
print(f"ONNX: {onnx_size:.2f} MB")