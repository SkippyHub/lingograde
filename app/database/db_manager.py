import sqlite3
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv('DATABASE_PATH', "app/database/recordings.db")
        self.conn = sqlite3.connect(self.db_path)
        self.init_db()
        self.migrate_db()
        self.create_tables()

    def init_db(self):
        c = self.conn.cursor()
        
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
        
        self.conn.commit()

    def migrate_db(self):
        """Add new columns if they don't exist"""
        c = self.conn.cursor()
        
        # Get existing columns
        c.execute('PRAGMA table_info(recordings)')
        columns = {col[1] for col in c.fetchall()}
        
        # Add missing columns
        new_columns = {
            'pronunciation_grade': 'FLOAT',
            'fluency_grade': 'FLOAT',
            'coherence_grade': 'FLOAT',
            'grammar_grade': 'FLOAT',
            'vocabulary_grade': 'FLOAT'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in columns:
                c.execute(f'ALTER TABLE recordings ADD COLUMN {col_name} {col_type}')
        
        self.conn.commit()

    def save_recording(self, user_id, filename, duration=None, transcription=None, 
                      model_response=None, metadata=None, grades=None):
        c = self.conn.cursor()
        
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
        
        self.conn.commit()

    def get_user_recordings(self, user_id):
        c = self.conn.cursor()
        
        c.execute('SELECT * FROM recordings WHERE user_id = ? ORDER BY timestamp DESC', 
                 (user_id,))
        recordings = c.fetchall()
        
        # Convert to list of dicts with properly formatted timestamps
        columns = ['id', 'user_id', 'filename', 'timestamp', 'duration', 'transcription', 
                  'model_response', 'metadata', 'pronunciation_grade', 'fluency_grade', 
                  'coherence_grade', 'grammar_grade', 'vocabulary_grade']
        
        formatted_recordings = []
        for recording in recordings:
            recording_dict = dict(zip(columns, recording))
            # Format timestamp as ISO string
            if isinstance(recording_dict['timestamp'], str):
                try:
                    # Parse the string timestamp
                    dt = datetime.strptime(recording_dict['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                    recording_dict['timestamp'] = dt.isoformat()
                except ValueError:
                    try:
                        # Try alternate format without microseconds
                        dt = datetime.strptime(recording_dict['timestamp'], '%Y-%m-%d %H:%M:%S')
                        recording_dict['timestamp'] = dt.isoformat()
                    except ValueError:
                        # If parsing fails, leave as is
                        pass
            elif isinstance(recording_dict['timestamp'], datetime):
                recording_dict['timestamp'] = recording_dict['timestamp'].isoformat()
            
            formatted_recordings.append(recording_dict)
        
        return formatted_recordings

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def create_user(self, username: str, password: str) -> bool:
        try:
            password_hash = pwd_context.hash(password)
            with self.conn:
                self.conn.execute(
                    'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                    (username, password_hash)
                )
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def verify_user(self, username: str, password: str) -> bool:
        try:
            with self.conn:
                result = self.conn.execute(
                    'SELECT password_hash FROM users WHERE username = ?',
                    (username,)
                ).fetchone()
                if result and pwd_context.verify(password, result[0]):
                    return True
            return False
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False

    def delete_recording(self, user_id: str, filename: str) -> bool:
        """Delete a recording from the database"""
        try:
            c = self.conn.cursor()
            c.execute('''
                DELETE FROM recordings 
                WHERE user_id = ? AND filename = ?
            ''', (user_id, filename))
            self.conn.commit()
            return c.rowcount > 0
        except Exception as e:
            print(f"Error deleting recording: {e}")
            return False

    def delete_recording_by_id(self, user_id: str, recording_id: int) -> bool:
        """Delete a recording from the database by ID"""
        try:
            c = self.conn.cursor()
            c.execute('''
                DELETE FROM recordings 
                WHERE user_id = ? AND id = ?
            ''', (user_id, recording_id))
            self.conn.commit()
            return c.rowcount > 0
        except Exception as e:
            print(f"Error deleting recording: {e}")
            return False

    def get_recording_by_id(self, user_id: str, recording_id: int) -> dict:
        """Get a recording by ID"""
        try:
            c = self.conn.cursor()
            c.execute('''
                SELECT * FROM recordings 
                WHERE user_id = ? AND id = ?
            ''', (user_id, recording_id))
            recording = c.fetchone()
            if recording:
                columns = ['id', 'user_id', 'filename', 'timestamp', 'duration', 'transcription', 
                          'model_response', 'metadata', 'pronunciation_grade', 'fluency_grade', 
                          'coherence_grade', 'grammar_grade', 'vocabulary_grade']
                return dict(zip(columns, recording))
            return None
        except Exception as e:
            print(f"Error getting recording: {e}")
            return None