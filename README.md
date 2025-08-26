# 🛒 Product Recommendation System with Real-Time Inference

---

## 🚀 Features

- ✅ Real-time product recommendation via **Kafka streaming**
- ⚡ Fast retrieval with **FAISS (Facebook AI Similarity Search)**
- 🧠 Collaborative filtering using **KNN with cosine similarity**
- 📦 REST API using **FastAPI + Uvicorn**
- 📊 Experiment tracking using **MLflow**
- 🐳 Fully containerized with **Docker**
- 🧪 Modular code under `src/` directory

---
- docker run -p 8000:8000 -v "${PWD}/models:/app/models" -v "${PWD}/data:/app/data" product-recommender



