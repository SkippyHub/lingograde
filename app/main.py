import streamlit as st
from model.predictor import AIModel
from database.db_manager import DatabaseManager
from storage.storage_manager import StorageManager
import uuid

class StreamlitApp:
    def __init__(self):
        self.model = AIModel()
        self.db_manager = DatabaseManager()
        self.storage_manager = StorageManager()
        
    def initialize_session(self):
        if 'user_id' not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
    
    def run(self):
        self.initialize_session()
        st.title("AI Model Interface")
        
        # Sidebar for user info and recordings
        with st.sidebar:
            st.header("Your Recordings")
            recordings = self.db_manager.get_user_recordings(st.session_state.user_id)
            for recording in recordings:
                st.write(f"Recording: {recording[2]}")  # filename
                if st.button(f"Play {recording[2]}"):
                    audio_path = self.storage_manager.get_recording_path(
                        st.session_state.user_id, 
                        recording[2]
                    )
                    if audio_path.exists():
                        st.audio(str(audio_path))
        
        # Main content area
        st.write("### Record Audio")
        audio_bytes = st.audio_recorder()
        
        if audio_bytes:
            # Save the recording
            filename = self.storage_manager.save_recording(
                st.session_state.user_id, 
                audio_bytes
            )
            
            # Process with model
            with st.spinner("Processing..."):
                result = self.model.predict(audio_bytes)
                
            # Save to database
            self.db_manager.save_recording(
                user_id=st.session_state.user_id,
                filename=filename,
                model_response=result
            )
            
            st.write("### Result:")
            st.write(result)

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()