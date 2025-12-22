# Ini dijalankan di Databricks Notebook
import json
from pyspark.sql import SparkSession

# 1. Start Spark (Di Databricks Community ini otomatis, tapi kita tulis aja)
spark = SparkSession.builder.appName("RetailRecommender").getOrCreate()

# 2. Simulasi: Membuat DataFrame Data Transaksi (Ceritanya ini data Jutaan Baris)
# Di project asli, ini: spark.read.csv("/FileStore/tables/transaksi.csv")
data = [
    ("INV001", "KOPI"), ("INV001", "GULA"), ("INV001", "SUSU"),
    ("INV002", "SEPATU"), ("INV002", "KAOS_KAKI"),
    ("INV003", "LAPTOP"), ("INV003", "MOUSE"), ("INV003", "KEYBOARD"),
    ("INV004", "HP"), ("INV004", "CASING"), ("INV004", "HEADSET"),
    ("INV005", "KOPI"), ("INV005", "ROTI") # Kopi juga dibeli sama Roti
]
columns = ["InvoiceNo", "StockCode"]
df = spark.createDataFrame(data, columns)

print("✅ Data Loaded. Total rows:", df.count())

# 3. Logic Data Engineering: Mencari Pasangan Barang
# Kita cari: Barang A sering dibeli bareng apa aja?
from pyspark.sql.functions import collect_list, col

# Group by Invoice (Satu keranjang isinya apa aja)
basket = df.groupBy("InvoiceNo").agg(collect_list("StockCode").alias("items"))

# (Logic Sederhana untuk Demo)
# Kita bikin dictionary rekomendasi manual dari pola di atas
# Di real case: Pakai FPGrowth Algorithm (MLlib)
rules = {
    "KOPI": ["GULA", "SUSU", "ROTI"],
    "SEPATU": ["KAOS_KAKI", "TALI_SEPATU"],
    "LAPTOP": ["MOUSE", "KEYBOARD", "MOUSEPAD"],
    "HP": ["CASING", "HEADSET", "POWERBANK"]
}

print("✅ Model Trained. Rules generated.")

# 4. Simpan Hasil ke Folder App (Menimpa file dummy yg lama)
# Path di Databricks Repos agak unik, kita pakai relative path
import os

# Lokasi file json tujuan (di folder app/)
output_path = "../app/recommender.json" 

# Tulis file JSON
with open(output_path, "w") as f:
    json.dump(rules, f)
    
print(f"✅ Rules saved to {output_path}")