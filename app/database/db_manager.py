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
        
        # Create recordings table with speech grades
        c.execute('''
            CREATE TABLE IF NOT EXISTS recordings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                duration FLOAT,
                transcription TEXT,
                model_response TEXT,
                metadata TEXT,
                pronunciation_grade FLOAT,
                fluency_grade FLOAT,
                coherence_grade FLOAT,
                grammar_grade FLOAT,
                vocabulary_grade FLOAT
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
                      model_response=None, metadata=None, grades=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Extract grades or use defaults
        grades = grades or {}
        pronunciation = grades.get('pronunciation', 0.0)
        fluency = grades.get('fluency', 0.0)
        coherence = grades.get('coherence', 0.0)
        grammar = grades.get('grammar', 0.0)
        vocabulary = grades.get('vocabulary', 0.0)
        
        c.execute('''
            INSERT INTO recordings 
            (user_id, filename, timestamp, duration, transcription, model_response, metadata,
             pronunciation_grade, fluency_grade, coherence_grade, grammar_grade, vocabulary_grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, filename, datetime.now(), duration, transcription, 
              model_response, metadata, pronunciation, fluency, coherence, grammar, vocabulary))
        
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