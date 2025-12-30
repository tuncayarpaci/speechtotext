import os
import queue
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from datetime import datetime

# --- KÜTÜPHANE YOLU HATASINI ÖNLEME ---
# Eğer kütüphane bulunamazsa manuel olarak yolu ekleyelim
import sys
env_path = "/home/tuncay/Projects/Dataset/my_model_env/lib/python3.12/site-packages/nvidia/cudnn/lib"
if os.path.exists(env_path):
    os.environ["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH", "") + ":" + env_path

# --- AYARLAR ---
MODEL_SIZE = "medium"  
DEVICE = "cuda"
DEVICE_INDEX = 0
# RTX 4000 için en verimli tip
COMPUTE_TYPE = "int8_float16" 

print(f"Model ({MODEL_SIZE}) GPU:{DEVICE_INDEX} üzerinde yükleniyor...")

try:
    model = WhisperModel(
        MODEL_SIZE, 
        device=DEVICE, 
        device_index=DEVICE_INDEX, 
        compute_type=COMPUTE_TYPE
    )
except Exception as e:
    print(f"GPU yükleme hatası: {e}")
    print("CPU moduna geri dönülüyor...")
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Ses Hatası: {status}")
    audio_queue.put(indata.copy())

print("\n--- SİSTEM HAZIR ---")
print("Dinleniyor... (Durdurmak için Ctrl+C)\n")

try:
    with sd.InputStream(samplerate=16000, channels=1, callback=audio_callback, blocksize=48000):
        with open("konusma_kayitlari.txt", "a", encoding="utf-8") as f:
            while True:
                audio_chunk = audio_queue.get().flatten()
                
                segments, _ = model.transcribe(
                    audio_chunk,
                    language="tr",
                    beam_size=5,
                    vad_filter=True,
                    condition_on_previous_text=False
                )

                for segment in segments:
                    text = segment.text.strip()
                    if len(text) > 1:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        log_entry = f"[{timestamp}] {text}"
                        print(log_entry)
                        f.write(log_entry + "\n")
                        f.flush()

except KeyboardInterrupt:
    print("\nProgram durduruldu.")
except Exception as e:
    print(f"\nBeklenmedik hata: {e}")