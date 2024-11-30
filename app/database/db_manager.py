import sqlite3
from datetime import datetime
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="app/database/recordings.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create recordings table
        c.execute('''
            CREATE TABLE IF NOT EXISTS recordings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                duration FLOAT,
                transcription TEXT,
                model_response TEXT,
                metadata TEXT
            )
        ''')
        
        # Create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                created_at DATETIME NOT NULL,
                last_active DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_recording(self, user_id, filename, duration=None, transcription=None, 
                      model_response=None, metadata=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO recordings 
            (user_id, filename, timestamp, duration, transcription, model_response, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, filename, datetime.now(), duration, transcription, 
              model_response, metadata))
        
        conn.commit()
        conn.close()

    def get_user_recordings(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT * FROM recordings WHERE user_id = ? ORDER BY timestamp DESC', 
                 (user_id,))
        recordings = c.fetchall()
        
        conn.close()
        return recordings 