# NVIDIA'nın CUDA destekli resmi imajını kullanıyoruz
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Sistem paketlerini ve Python'ı kur
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kütüphaneleri kopyala ve kur
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Uygulama kodlarını ve klasörleri kopyala
COPY main_api.py .
COPY templates/ ./templates/

# Kayıtlar için klasör oluştur
RUN mkdir -p kayitlar

# Portu dış dünyaya aç
EXPOSE 3333

# Uygulamayı başlat
CMD ["python3", "main_api.py"]
