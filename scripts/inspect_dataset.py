import pandas as pd


train_path = "data/medical_tc_train.csv"
test_path = "data/medical_tc_test.csv"
labels_path = "data/medical_tc_labels.csv"


train = pd.read_csv(train_path)
test = pd.read_csv(test_path)
labels = pd.read_csv(labels_path)


print("\n===== TRAIN =====")
print(train.head())
print("\nColunas:")
print(train.columns.tolist())
print("\nShape:")
print(train.shape)


print("\n===== TEST =====")
print(test.head())
print("\nColunas:")
print(test.columns.tolist())
print("\nShape:")
print(test.shape)


print("\n===== LABELS =====")
print(labels.head())
print("\nColunas:")
print(labels.columns.tolist())
print("\nShape:")
print(labels.shape)