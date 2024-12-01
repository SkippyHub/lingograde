from fastapi import FastAPI, UploadFile, File, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from .auth import create_access_token, get_current_user, User, Token
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import sys
from pathlib import Path
import logging
from fastapi.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

# Create FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the app directory to Python path
app_dir = Path(__file__).parent.parent
sys.path.append(str(app_dir))

from model.predictor import AIModel
from database.db_manager import DatabaseManager
from storage.storage_manager import StorageManager
import uuid
import json

# Initialize services
model = AIModel()
db_manager = DatabaseManager()
storage_manager = StorageManager()

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/api/analyze-audio")
async def analyze_audio(
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    logger.debug(f"Received audio file: {audio.filename}")
    audio_bytes = await audio.read()
    logger.debug(f"Audio size: {len(audio_bytes)} bytes")
    
    result = model.predict(audio_bytes)
    logger.debug(f"Model prediction result: {result}")
    
    # Save to storage and database using current user's username
    filename = f"recording_{uuid.uuid4()}.wav"
    storage_manager.save_recording(user_id=current_user.username, audio_data=audio_bytes, filename=filename)
    db_manager.save_recording(
        user_id=current_user.username,
        filename=filename,
        transcription=result.get('transcription'),
        model_response=json.dumps(result),
        grades=result.get('grades', {})
    )
    
    logger.debug(f"Returning result: {result}")
    return result

@app.get("/api/recordings")
async def get_recordings(current_user: User = Depends(get_current_user)):
    logger.debug(f"Fetching recordings for user: {current_user.username}")
    recordings = db_manager.get_user_recordings(current_user.username)
    logger.debug(f"Found recordings: {recordings}")
    return recordings

@app.get("/api/recordings/{filename}")
async def get_recording_audio(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """Get audio file for a recording"""
    logger.debug(f"Fetching audio file: {filename}")
    
    file_path = storage_manager.get_recording_path(current_user.username, filename)
    if file_path.exists():
        return FileResponse(
            path=str(file_path),
            media_type="audio/wav",
            filename=filename
        )
    return {"error": "File not found"}

@app.post("/api/signup")
async def signup(user: UserCreate):
    if db_manager.create_user(user.username, user.password):
        return {"message": "User created successfully"}
    raise HTTPException(
        status_code=400,
        detail="Username already exists"
    )

@app.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if db_manager.verify_user(form_data.username, form_data.password):
        access_token = create_access_token(
            data={"sub": form_data.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=400,
        detail="Incorrect username or password"
    )

@app.delete("/api/recordings/{recording_id}")
async def delete_recording(
    recording_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        logger.debug(f"Deleting recording: {recording_id} for user: {current_user.username}")
        
        # First get the recording to find its filename
        recording = db_manager.get_recording_by_id(current_user.username, recording_id)
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        # Delete the audio file
        storage_manager.delete_recording(current_user.username, recording['filename'])
        
        # Delete from database
        result = db_manager.delete_recording_by_id(current_user.username, recording_id)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to delete recording from database")
            
        return {"message": "Recording deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting recording: {e}")
        raise HTTPException(status_code=500, detail=str(e))