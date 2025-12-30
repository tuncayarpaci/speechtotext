import os
import uvicorn
import io
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from faster_whisper import WhisperModel
from datetime import datetime

# --- YOL AYARLARI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
KAYIT_KLASORU = os.path.join(BASE_DIR, "kayitlar")

if not os.path.exists(KAYIT_KLASORU):
    os.makedirs(KAYIT_KLASORU)

# Jinja2 Şablon Ayarı
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# --- WHISPER MODEL YÜKLEME ---
# RTX 4000 GPU'larını en verimli kullanacak int8_float16 modu
print("Whisper Model (medium) GPU üzerinde yükleniyor...")
model = WhisperModel("medium", device="cuda", compute_type="int8_float16")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    audio_buffer = bytearray()
    son_islenen_metin = "" # Tekrarlı kayıtları önlemek için kritik değişken
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Yeni canlı oturum başladı.")
    
    try:
        while True:
            # Tarayıcıdan gelen binary ses parçasını al
            data = await websocket.receive_bytes()
            audio_buffer.extend(data)
            
            # Bellekte işlenecek kadar veri biriktiğinde (yaklaşık 2 saniye)
            if len(audio_buffer) > 32000:
                try:
                    # Mevcut tüm buffer'ı işle
                    segments, _ = model.transcribe(
                        io.BytesIO(audio_buffer), 
                        language="tr",
                        vad_filter=True,
                        beam_size=5
                    )
                    
                    # Tüm segmentleri birleştirerek tam metni oluştur
                    full_text = " ".join([s.text for s in segments]).strip()
                    
                    # Eğer metin değiştiyse tarayıcıya gönder (akıcılık sağlar)
                    if full_text and full_text != son_islenen_metin:
                        son_islenen_metin = full_text
                        await websocket.send_text(full_text)
                        
                except Exception as e:
                    print(f"İşleme hatası: {e}")
                    continue
                    
    except WebSocketDisconnect:
        # OTURUM SONU: "Durdur"a basıldığında tetiklenir
        if son_islenen_metin:
            tarih_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            dosya_adi = f"konusma_{tarih_str}.txt"
            dosya_yolu = os.path.join(KAYIT_KLASORU, dosya_adi)
            
            # Sadece en son ve en kapsamlı metni temiz bir şekilde kaydet
            with open(dosya_yolu, "w", encoding="utf-8") as f:
                f.write(f"Kayıt Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 40 + "\n")
                f.write(son_islenen_metin)
            
            # Genel geçmiş dosyasına da ekle
            with open(os.path.join(KAYIT_KLASORU, "tum_konusmalar.txt"), "a", encoding="utf-8") as f:
                f.write(f"\n[{tarih_str}] {son_islenen_metin}\n")
            
            print(f"Oturum başarıyla kaydedildi: {dosya_adi}")
        
        audio_buffer.clear()
        print("Bağlantı kapatıldı.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3333)