import pandas as pd
import numpy as np
import os

# Load raw dataset
df = df = pd.read_csv(r"D:\Ailab_Task\product-recommender\product-recommender\Data\raw\amazon.csv")

df = df.rename(columns=str.lower)

# Step 1: Split user_ids and ratings
df['user_ids'] = df['user_id'].astype(str).str.split(',')
df['ratings'] = df['rating'].astype(str).str.split(',')
df['product_ids'] = df['product_id']

# Step 2: Flatten to individual user-product-rating records
rows = []
for idx, row in df.iterrows():
    for uid, r in zip(row['user_ids'], row['ratings']):
        try:
            rating = float(r)
        except:
            continue
        rows.append({'user_id': uid.strip(), 'product_id': row['product_ids'], 'rating': rating})

flat_df = pd.DataFrame(rows)

# Drop invalid rows
flat_df = flat_df.dropna(subset=['user_id', 'product_id', 'rating'])
flat_df['rating'] = pd.to_numeric(flat_df['rating'], errors='coerce')
flat_df = flat_df.dropna()

# Ensure output directory exists
os.makedirs("data/processed", exist_ok=True)

# Save flattened ratings data
flat_df.to_csv("data/processed/ratings.csv", index=False)

# Save product_id → product_name mapping
product_info = df[['product_id', 'product_name']].drop_duplicates()
product_info.to_csv("data/processed/product_info.csv", index=False)

print("✅ Preprocessing complete: ratings.csv and product_info.csv saved.")
