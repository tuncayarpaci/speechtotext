import os
import uvicorn
import io
import time
import asyncio
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from faster_whisper import WhisperModel
from pydantic import BaseModel
from typing import List, Optional

# Veritabanı fonksiyonlarını içe aktar
from database import generate_new_key, validate_key

app = FastAPI(title="Whisper Enterprise SaaS API")

# --- GPU KUYRUK KİLİDİ ---
gpu_lock = asyncio.Lock()

# --- GÜVENLİK (DYNAMIC AUTH) ---
async def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Anahtarı eksik (Header: x-api-key)")
    
    username = validate_key(x_api_key)
    if not username:
        raise HTTPException(status_code=403, detail="Geçersiz API Anahtarı")
    return username

# --- MODEL YÖNETİMİ ---
loaded_models = {}

def get_model(model_size: str):
    if model_size not in loaded_models:
        print(f"Model yükleniyor: {model_size}...")
        loaded_models[model_size] = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    return loaded_models[model_size]

# --- VERİ ŞEMALARI ---
class WordInfo(BaseModel):
    word: str
    start: float
    end: float
    probability: float

class TranscribeResponse(BaseModel):
    text: str
    model: str
    user: str
    queue_wait_time: float
    processing_time: float
    words: Optional[List[WordInfo]]

# --- API ENDPOINTLERİ ---

@app.post("/generate-key")
async def create_key(username: str):
    """Yeni bir API Anahtarı oluşturur."""
    key = generate_new_key(username)
    if not key:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış.")
    return {"username": username, "api_key": key}

@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_file(
    file: UploadFile = File(...), 
    model_type: str = "medium", 
    user: str = Depends(verify_api_key)
):
    """Kuyruk ve DB Doğrulamalı Transkripsiyon"""
    arrival_time = time.time()
    
    async with gpu_lock:
        wait_duration = round(time.time() - arrival_time, 2)
        start_process_time = time.time()
        
        current_model = get_model(model_type)
        content = await file.read()
        
        segments, _ = current_model.transcribe(
            io.BytesIO(content), 
            language="tr", 
            word_timestamps=True,
            vad_filter=True
        )
        
        full_text = ""
        words = []
        for segment in segments:
            full_text += segment.text
            for w in segment.words:
                words.append(WordInfo(word=w.word, start=w.start, end=w.end, probability=w.probability))
        
        return TranscribeResponse(
            text=full_text.strip(),
            model=model_type,
            user=user,
            queue_wait_time=wait_duration,
            processing_time=round(time.time() - start_process_time, 2),
            words=words
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3333)