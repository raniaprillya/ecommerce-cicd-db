# 1. Ambil base image Python yang ringan
FROM python:3.9-slim

# 2. Set folder kerja di dalam server
WORKDIR /code

# 3. Copy file requirements dulu (biar cache-nya efisien)
COPY ./requirements.txt /code/requirements.txt

# 4. Install library
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copy semua kode aplikasi kita
COPY ./app /code/app

# 6. Perintah untuk menyalakan server saat container jalan
# Host 0.0.0.0 artinya bisa diakses dari luar container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]