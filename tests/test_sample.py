from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict():
    payload = {
        "text": "Does carotid restenosis predict an increased risk of stroke?"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert "classification" in response.json()