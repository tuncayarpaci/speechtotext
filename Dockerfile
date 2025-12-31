FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Sistem bağımlılıklarını ve FFmpeg'i kur
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pip'i güncelle ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Uygulama kodlarını ve klasörleri kopyala
COPY main_api.py database.py .
COPY templates/ ./templates/

# Kayıtlar ve Veritabanı için gerekli izinler
RUN mkdir -p kayitlar

# Portu aç
EXPOSE 3333

CMD ["python3", "main_api.py"]
