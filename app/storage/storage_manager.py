from pathlib import Path
import shutil
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class StorageManager:
    def __init__(self, base_path=None):
        self.base_path = Path(base_path or os.getenv('STORAGE_PATH', "app/storage/recordings"))
        self.base_path.mkdir(parents=True, exist_ok=True)

    def get_user_directory(self, user_id):
        user_dir = self.base_path / user_id
        user_dir.mkdir(exist_ok=True)
        return user_dir

    def save_recording(self, user_id, audio_data, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        
        user_dir = self.get_user_directory(user_id)
        file_path = user_dir / filename
        
        # Save the audio data
        with open(file_path, 'wb') as f:
            f.write(audio_data)
            
        return str(file_path)

    def get_recording_path(self, user_id, filename):
        return self.base_path / user_id / filename

    def delete_recording(self, user_id: str, filename: str) -> bool:
        """Delete a recording file from storage"""
        try:
            file_path = self.get_recording_path(user_id, filename)
            if file_path.exists():
                file_path.unlink()  # Delete the file
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False 