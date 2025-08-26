import pandas as pd
import joblib
import faiss

# Load data and models
pivot = joblib.load("models/user_item_matrix.pkl")
product_info = pd.read_csv("data/processed/product_info.csv").set_index("product_id")
index = faiss.read_index("models/faiss_index.idx")

def recommend(user_id, top_k=5):
    if user_id not in pivot.index:
        return {"error": f"User ID '{user_id}' not found."}

    # Get user vector and search using FAISS
    user_vector = pivot.loc[user_id].values.astype('float32').reshape(1, -1)
    distances, indices = index.search(user_vector, top_k)

    # Map indices to product IDs
    product_ids = pivot.columns[indices[0]]
    results = []

    for pid in product_ids:
        name = product_info.loc[pid]['product_name'] if pid in product_info.index else "Unknown"
        results.append({
            "product_id": pid,
            "product_name": name
        })

    return {
        "user_id": user_id,
        "recommendations": results
    }

