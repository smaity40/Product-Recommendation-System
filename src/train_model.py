import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib
import mlflow
import os
import faiss

# Load the processed ratings
df = pd.read_csv("data/processed/ratings.csv")

# Create user-item matrix
pivot = df.pivot_table(index='user_id', columns='product_id', values='rating', fill_value=0)
matrix = pivot.values.astype('float32')

# -----------------------------
# 1️⃣ Train NearestNeighbors model (backup)
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(pivot)

# -----------------------------
# 2️⃣ Train Faiss index for fast vector search
index = faiss.IndexFlatL2(matrix.shape[1])  # L2 norm
index.add(matrix)  # Add all user vectors

# -----------------------------
# 3️⃣ Save models
os.makedirs("models", exist_ok=True)
joblib.dump(pivot, "models/user_item_matrix.pkl")
joblib.dump(model, "models/recommender_model.pkl")
faiss.write_index(index, "models/faiss_index.idx")

# -----------------------------
# 4️⃣ Log with MLflow
mlflow.set_experiment("Amazon_Recommendation")
with mlflow.start_run():
    mlflow.log_param("num_users", pivot.shape[0])
    mlflow.log_param("num_products", pivot.shape[1])
    mlflow.log_param("faiss_index", "IndexFlatL2")
    mlflow.sklearn.log_model(model, artifact_path="sklearn_model")
    mlflow.log_artifact("models/faiss_index.idx")

print("✅ Model training complete. Files saved in models/")
