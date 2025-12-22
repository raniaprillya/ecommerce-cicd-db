from fastapi.testclient import TestClient
from app.main import app

# Kita bikin 'klien palsu' untuk ngetes API tanpa perlu nyalain server beneran
client = TestClient(app)

# Skenario 1: Cek halaman Home
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "online",
        "message": "Retail Recommender API siap digunakan!",
        "version": "1.0.0"
    }

# Skenario 2: Cek Rekomendasi yang ADA datanya (Kopi)
def test_recommend_kopi():
    response = client.get("/recommend/kopi")
    assert response.status_code == 200
    data = response.json()
    assert data["product"] == "KOPI"
    # Pastikan rekomendasinya mengandung GULA
    assert "GULA" in data["recommendations"]

# Skenario 3: Cek Rekomendasi barang GAIB (Gak ada di data)
def test_recommend_unknown():
    response = client.get("/recommend/mobil_balap")
    assert response.status_code == 200
    data = response.json()
    assert data["recommendations"] == []
    assert data["note"] == "Produk ini belum ada di pola belanja kita."