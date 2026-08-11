import time
import requests

# URL da API rodando no Docker
URL = "http://127.0.0.1:8000/predict"

# Payload de teste
PAYLOAD = {
    "text": "Does carotid restenosis predict an increased risk of stroke?"
}

NUM_REQUESTS = 50
latencies = []

print(f"🚀 Iniciando benchmark de latência ({NUM_REQUESTS} requisições)...")

# Warm-up (primeira requisição para carregar o modelo na memória)
requests.post(URL, json=PAYLOAD)

for i in range(1, NUM_REQUESTS + 1):
    start_time = time.time()
    response = requests.post(URL, json=PAYLOAD)
    end_time = time.time()
    
    if response.status_code == 200:
        latency_ms = (end_time - start_time) * 1000
        latencies.append(latency_ms)
    else:
        print(f"❌ Requisição {i} falhou com status: {response.status_code}")

if latencies:
    avg_latency = sum(latencies) / len(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)
    
    print("\n📊 RESULTADOS DO BENCHMARK BASELINE:")
    print(f"   • Média de Latência: {avg_latency:.2f} ms")
    print(f"   • Menor Tempo:      {min_latency:.2f} ms")
    print(f"   • Maior Tempo:      {max_latency:.2f} ms")