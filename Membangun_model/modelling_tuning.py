import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import mlflow.sklearn
import dagshub
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix

# 1. Hubungkan kode ke DagsHub (Syarat Advance)
dagshub.init(repo_owner='M-Rafif-Musyaffa', repo_name='Eksperimen_ML_Rafif', mlflow=True)

# 2. Persiapan Data
df = pd.read_csv("heart-disease-dataset_preprocessing/heart_ready.csv")
X = df.drop("target", axis=1)
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("Eksperimen_Jantung_Advance")

with mlflow.start_run(run_name="Tuning_Manual_Log"):
    print("Mencari parameter terbaik (Tuning)...")
    
    # 3. Hyperparameter Tuning (Syarat Skilled)
    param_grid = {'n_estimators': [50, 100], 'max_depth': [10, 20]}
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(rf, param_grid, cv=3)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # 4. MANUAL LOGGING (Syarat Skilled/Advance: Tidak pakai autolog)
    mlflow.log_params(grid_search.best_params_)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(
        sk_model=best_model, 
        artifact_path="Model_Jantung_Terbaik",
        skops_trusted_types=["sklearn.tree._tree.Tree"]
    )

    # 5. BUAT 2 ARTEFAK TAMBAHAN GAMBAR (Syarat Advance)
    os.makedirs("artifacts", exist_ok=True)

    # Gambar 1: Confusion Matrix
    plt.figure(figsize=(5,4))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, cmap='Blues')
    plt.title("Confusion Matrix")
    plt.savefig("artifacts/confusion_matrix.png")
    plt.close()

    # Gambar 2: Feature Importance
    plt.figure(figsize=(6,4))
    sns.barplot(x=best_model.feature_importances_, y=X.columns)
    plt.title("Feature Importance")
    plt.savefig("artifacts/feature_importance.png")
    plt.close()

    # Mengirim gambar ke DagsHub
    mlflow.log_artifact("artifacts/confusion_matrix.png")
    mlflow.log_artifact("artifacts/feature_importance.png")

    print("Berhasil! Cek website DagsHub Anda sekarang.")