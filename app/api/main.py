from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent.parent
sys.path.append(str(app_dir))

from model.predictor import AIModel
from database.db_manager import DatabaseManager
from storage.storage_manager import StorageManager
import uuid
import json

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
model = AIModel()
db_manager = DatabaseManager()
storage_manager = StorageManager()

@app.post("/api/analyze-audio")
async def analyze_audio(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    result = model.predict(audio_bytes)
    
    # Save to storage and database
    filename = f"recording_{uuid.uuid4()}.wav"
    storage_manager.save_recording(user_id="default", audio_data=audio_bytes, filename=filename)
    db_manager.save_recording(
        user_id="default",
        filename=filename,
        model_response=json.dumps(result),
        grades=result.get('grades', {})
    )
    
    return result

@app.get("/api/recordings")
async def get_recordings(user_id: str = "default"):
    recordings = db_manager.get_user_recordings(user_id)
    return recordings 