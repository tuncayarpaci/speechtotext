import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from faster_whisper import WhisperModel
from datetime import datetime

# --- YOL AYARLARI (Hata Almamak İçin Kritik) ---
# Bu dosyanın bulunduğu tam dizini al (/home/tuncay/Projects)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
KAYIT_KLASORU = os.path.join(BASE_DIR, "kayitlar")

# Gerekli klasörleri oluştur
if not os.path.exists(KAYIT_KLASORU):
    os.makedirs(KAYIT_KLASORU)

# Jinja2 Templates ayarı - Tam yol belirtiyoruz
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# --- WHISPER AYARLARI ---
MODEL_SIZE = "medium"
DEVICE = "cuda"
PORT = 3333
os.environ["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH", "") + ":/home/tuncay/Projects/Dataset/my_model_env/lib/python3.12/site-packages/nvidia/cudnn/lib"

app = FastAPI()

# Modeli yükle
print(f"Model ({MODEL_SIZE}) GPU üzerinde yükleniyor...")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="int8_float16")

# --- ENDPOINTLER ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # templates/index.html dosyasını render et
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    temp_file = os.path.join(BASE_DIR, f"temp_{file.filename}")
    try:
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        segments, _ = model.transcribe(temp_file, language="tr")
        full_text = " ".join([segment.text for segment in segments]).strip()
        
        if full_text:
            tarih = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            dosya_adi = f"konusma_{tarih}.txt"
            dosya_yolu = os.path.join(KAYIT_KLASORU, dosya_adi)
            with open(dosya_yolu, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"Kaydedildi: {dosya_adi}")
        
        return {"text": full_text}
    except Exception as e:
        print(f"Hata: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    print(f"Sunucu başlatılıyor: http://localhost:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)