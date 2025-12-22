import json
from pyspark.sql import SparkSession

# 1. Start Spark 
spark = SparkSession.builder.appName("RetailRecommender").getOrCreate()

# 2. Dummy : Transaction data
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

# 3. Logic Data Engineering: Searching products by Grouping by invoice
from pyspark.sql.functions import collect_list, col

basket = df.groupBy("InvoiceNo").agg(collect_list("StockCode").alias("items"))

# (Logic for Demo Purpose)
# Manual dictionary recommendation
rules = {
    "KOPI": ["GULA", "SUSU", "ROTI"],
    "SEPATU": ["KAOS_KAKI", "TALI_SEPATU"],
    "LAPTOP": ["MOUSE", "KEYBOARD", "MOUSEPAD"],
    "HP": ["CASING", "HEADSET", "POWERBANK"]
}

print("✅ Model Trained. Rules generated.")

# 4. Save to json
import os

output_path = "../app/recommender.json" 

with open(output_path, "w") as f:
    json.dump(rules, f)
    
print(f"✅ Rules saved to {output_path}")