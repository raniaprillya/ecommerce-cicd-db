import json
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# --- 1. Load Data ---
json_path = os.path.join(os.path.dirname(__file__), "recommender.json")

try:
    with open(json_path, "r") as f:
        recommendations = json.load(f)
    print("Recommendation Data Loaded!")
except FileNotFoundError:
    recommendations = {}
    print("Recommender.json file not found, recommendation empty.")

# --- 2. Main Endpoint ---
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Retail Recommender API ready to use!",
        "version": "1.0.0"
    }

# --- 3. Recommendation Endpoint ---
@app.get("/recommend/{product_id}")
def get_recommendation(product_id: str):
    clean_id = product_id.upper()
    
    # Check product in json files
    if clean_id in recommendations:
        return {
            "product": clean_id,
            "recommendations": recommendations[clean_id]
        }
    else:
        return {
            "product": clean_id,
            "recommendations": [],
            "note": "This product not found in our database."
        }