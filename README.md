# 🎙️ Whisper Real-Time Transcription (Docker & GPU)

Bu proje, NVIDIA GPU destekli Whisper modelini kullanarak anlık Türkçe ses-metin dönüşümü sağlar.

## 🚀 Hızlı Başlangıç
```bash
docker compose up --build -d
```

## ⚠️ Önemli: Mikrofon İzni Hatası
Tarayıcılar, HTTPS olmayan bağlantılarda mikrofonu engeller. Uygulamayı yerel ağ üzerinden kullanıyorsanız şu ayarı yapmalısınız:
1. Chrome'da `chrome://flags/#unsafely-treat-insecure-origin-as-secure` sayfasını açın.
2. `http://sunucu-ip-adresiniz:3333` adresini ekleyin.
3. Ayarı **Enabled** yapıp tarayıcıyı yeniden başlatın.
