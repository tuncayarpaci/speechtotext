FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Sistem paketlerini kur
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pip'i güncelle (Kurulum hatalarını önlemek için)
RUN pip3 install --upgrade pip

# Sadece gerekli ana kütüphaneleri kur
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY main_api.py .
COPY templates/ ./templates/

RUN mkdir -p kayitlar

EXPOSE 3333

CMD ["python3", "main_api.py"]
