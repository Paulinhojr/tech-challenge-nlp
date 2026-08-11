import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline


# =========================
# 1. Carregamento dos dados
# =========================

train_path = "data/medical_tc_train.csv"
test_path = "data/medical_tc_test.csv"
labels_path = "data/medical_tc_labels.csv"

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)
labels_df = pd.read_csv(labels_path)


# =========================
# 2. Separação das variáveis
# =========================

X_train = train_df["medical_abstract"]
y_train = train_df["condition_label"]

X_test = test_df["medical_abstract"]
y_test = test_df["condition_label"]


# =========================
# 3. Criação do modelo
# =========================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# =========================
# 4. Treinamento
# =========================

print("Iniciando treinamento...")

model.fit(X_train, y_train)

print("Treinamento concluído.")


# =========================
# 5. Avaliação
# =========================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nRelatório de classificação:")
print(
    classification_report(
        y_test,
        predictions
    )
)


# =========================
# 6. Salvamento do modelo
# =========================

output_path = "models/medical_classifier.pkl"

joblib.dump(model, output_path)

print(f"\nModelo salvo em: {output_path}")
