import json
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# --- 1. Load Data saat aplikasi nyala ---
# Kita cari path file json-nya
json_path = os.path.join(os.path.dirname(__file__), "recommender.json")

try:
    with open(json_path, "r") as f:
        recommendations = json.load(f)
    print("✅ Data rekomendasi berhasil dimuat!")
except FileNotFoundError:
    recommendations = {}
    print("⚠️ File recommender.json tidak ditemukan, rekomendasi kosong.")

# --- 2. Endpoint Utama (Halaman Depan) ---
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Retail Recommender API siap digunakan!",
        "version": "1.0.0"
    }

# --- 3. Endpoint Rekomendasi (Fitur Inti) ---
@app.get("/recommend/{product_id}")
def get_recommendation(product_id: str):
    # Ubah input jadi huruf besar semua biar cocok sama key di JSON
    clean_id = product_id.upper()
    
    # Cek apakah produk ada di database kita
    if clean_id in recommendations:
        return {
            "product": clean_id,
            "recommendations": recommendations[clean_id]
        }
    else:
        # Kalau produk tidak ditemukan
        return {
            "product": clean_id,
            "recommendations": [],
            "note": "Produk ini belum ada di pola belanja kita."
        }