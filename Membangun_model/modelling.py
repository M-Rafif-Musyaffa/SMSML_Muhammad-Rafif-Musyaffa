import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Membaca data yang sudah bersih dari tugas preprocessing
df = pd.read_csv("heart-disease-dataset_preprocessing/heart_ready.csv")
X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fitur AUTOLOG (Syarat Utama Kriteria Basic)
mlflow.sklearn.autolog()

# Memulai training model
with mlflow.start_run(run_name="Basic_RandomForest"):
    print("Melatih model kriteria Basic...")
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    print("Selesai! Log tersimpan secara lokal.")