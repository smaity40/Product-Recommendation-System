from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# -----------------------------
# Load pre-trained artifacts
# -----------------------------
pivot = joblib.load("models/user_item_matrix.pkl")
model = joblib.load("models/recommender_model.pkl")
product_info = pd.read_csv("data/processed/product_info.csv").set_index("product_id")

# -----------------------------
# Initialize FastAPI app
# -----------------------------
app = FastAPI(
    title="Product Recommendation API",
    description="Returns product recommendations for a given user ID.",
    version="1.0.0"
)

# -----------------------------
# Define Request Schema
# -----------------------------
class UserRequest(BaseModel):
    user_id: str
    top_k: int = 5  # Default = 5

# -----------------------------
# Optional root endpoint
# -----------------------------
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Product Recommendation API!",
        "usage": "POST /recommend with a user_id and optional top_k value"
    }

# -----------------------------
# Recommendation Endpoint
# -----------------------------
@app.post("/recommend")
def recommend_products(request: UserRequest):
    user_id = request.user_id
    k = request.top_k

    if user_id not in pivot.index:
        return {"error": f"User ID '{user_id}' not found."}

    # Get recommendations using KNN
    user_vector = pivot.loc[user_id].values.reshape(1, -1)
    distances, indices = model.kneighbors(user_vector, n_neighbors=k)

    product_ids = pivot.columns[indices[0]]
    recommendations = []
    for pid in product_ids:
        name = product_info.loc[pid]['product_name'] if pid in product_info.index else "Unknown"
        recommendations.append({
            "product_id": pid,
            "product_name": name
        })

    return {
        "user_id": user_id,
        "recommendations": recommendations
    }
