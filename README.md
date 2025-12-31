# 🎙️ Whisper Real-Time GPU Transcription Web UI

Bu proje, NVIDIA GPU destekli (Faster-Whisper) kullanarak tarayıcı üzerinden anlık olarak Türkçe ses-metin dönüşümü yapan bir web uygulamasıdır. Konuşmalar bittiğinde otomatik olarak temiz ve tarih damgalı `.txt` dosyaları olarak kaydedilir.



## 🚀 Özellikler
- **Anlık Akış (Real-Time):** WebSocket protokolü ile konuştuğunuz anda metni ekranda görün.
- **GPU Hızlandırma:** Faster-Whisper (Medium model) ve CUDA desteği ile milisaniyeler içinde sonuç.
- [cite_start]**Akıllı Kayıt:** Tekrarları temizleyen, oturum bazlı otomatik `.txt` dosyalama sistemi [cite: 1-8].
- **Dockerize Mimari:** Tek komutla tüm bağımlılıklar (CUDA, FFmpeg, Python) hazır şekilde kurulum.
- **Modern Web UI:** Kullanıcı dostu canlı akış ekranı.

## 🛠️ Sistem Gereksinimleri
- NVIDIA GPU (RTX 3000/4000 serisi önerilir).
- Ubuntu/Linux işletim sistemi.
- Docker ve [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) yüklü olmalıdır.

## 📦 Kurulum ve Çalıştırma

Projeyi klonladıktan sonra dizine gidin ve şu komutu çalıştırın:

```bash
docker compose up --build -d
```

Uygulama başlatıldıktan sonra tarayıcınızdan şu adrese gidin:
**http://localhost:3333**

## 🔧 Önemli: Mikrofon Erişimi
Tarayıcılar `localhost` dışındaki HTTP bağlantılarında mikrofonu engeller. Eğer projeye başka bir cihazdan (Örn: 10.1.1.1) bağlanıyorsanız:
1. Chrome'da şu adresi açın: `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
2. Sunucu adresini (http://10.1.1.1:3333) listeye ekleyin ve **Enabled** yapın.
3. Tarayıcıyı yeniden başlatın.

## 📂 Dosya Yapısı
- `main_api.py`: FastAPI ve WebSocket sunucu mantığı.
- `templates/index.html`: Web arayüzü ve MediaRecorder akışı.
- `kayitlar/`: Otomatik oluşturulan konuşma metinlerinin saklandığı klasör.

## 📜 Lisans
Bu proje MIT lisansı ile lisanslanmıştır.
