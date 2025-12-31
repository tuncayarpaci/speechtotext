Markdown

# 🎙️ Whisper Enterprise Pro API Service

Bu proje, NVIDIA GPU (RTX 4000) destekli, dinamik API anahtarı yönetimi ve işlem kuyruğu özelliklerine sahip profesyonel bir ses-metin dönüşümü (Transcription) servisidir.

## 🚀 Öne Çıkan Özellikler

* **Dinamik API Key Yönetimi**: Kullanıcılar kendi anahtarlarını `/generate-key` endpoint'i üzerinden oluşturur; anahtarlar SQLite veritabanında güvenle saklanır.
* **GPU İşlem Kuyruğu (Task Queue)**: `asyncio.Lock` mekanizması sayesinde aynı anda gelen çoklu istekler sıraya alınır ve GPU'nun aşırı yüklenmesi/çökmesi engellenir.
* [cite_start]**Gelişmiş JSON Çıktısı**: Yanıtlar sadece tam metni değil, kelime bazlı zaman damgalarını (start/end) ve modelin doğruluk skorlarını (probability) içerir. [cite: 1-8]
* **Lazy Loading Model Desteği**: `tiny`, `medium` ve `large` modelleri sadece ilk talep edildiklerinde GPU belleğine yüklenerek kaynak tasarrufu sağlar.
* **WebSocket Desteği**: `/ws/{api_key}` üzerinden gerçek zamanlı, düşük gecikmeli canlı deşifre imkanı sunar.

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Sistem Bağımlılıkları
Ubuntu üzerinde NVIDIA sürücülerinin ve FFmpeg'in yüklü olması gerekir:
```bash
sudo apt update && sudo apt install ffmpeg python3-pip -y
2. Bağımlılıkların Yüklenmesi
Bash

python3 -m venv my_model_env
source my_model_env/bin/activate
pip install fastapi uvicorn faster-whisper jinja2 python-multipart websockets
3. Servisi Başlatma
Bash

python main_api.py
🖥️ Kullanım Rehberi
API Anahtarı Alın: POST http://localhost:3333/generate-key?username=tuncay

Dosya Gönderin: Header'a x-api-key bilginizi ekleyerek /transcribe endpoint'ine ses dosyası yükleyin.

Performans İzleme: Yanıt içerisindeki queue_wait_time ile isteğinizin kuyrukta ne kadar beklediğini görebilirsiniz.

📂 Proje Yapısı
main_api.py: API logic ve GPU kilit yönetimi.

database.py: SQLite veritabanı ve kullanıcı yetkilendirme işlemleri.

users.db: API anahtarlarının saklandığı veritabanı (Otomatik oluşturulur).

🛡️ Güvenlik
users.db dosyası hassas veriler içerdiği için .gitignore dosyasına eklenmiştir. Üretim ortamında API anahtarlarınızı kimseyle paylaşmayın.




---

### 2. GitHub Commit ve Push Komutları

Şimdi hazırladığımız tüm dosyaları (özellikle `database.py` ve yeni `README.md`) GitHub repona göndermek için terminalde şu komutları sırasıyla çalıştır:

```bash
cd /home/tuncay/Projects

# 1. Önce veritabanı dosyasının git'e gitmesini engelleyelim
echo "users.db" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "my_model_env/" >> .gitignore

# 2. Tüm yeni ve güncellenmiş dosyaları ekle
git add main_api.py database.py README.md .gitignore templates/index.html

# 3. Commit mesajını oluştur
git commit -m "Final: Dinamik API Key, SQLite veritabanı ve GPU işlem kuyruğu eklendi"

# 4. GitHub'a gönder
git push
