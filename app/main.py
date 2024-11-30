import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
from model.predictor import AIModel
from database.db_manager import DatabaseManager
from storage.storage_manager import StorageManager
import uuid
import queue
import logging
import soundfile as sf
import os
import json

# Set up detailed logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class StreamlitApp:
    def __init__(self):
        logger.debug("Initializing StreamlitApp")
        print("Loading AI model...")
        self.model = AIModel()
        print("Model loaded successfully!")
        
        # Initialize managers
        self.storage_manager = StorageManager()
        self.db_manager = DatabaseManager()
        
        # For backwards compatibility and testing
        self.recordings_dir = self.storage_manager.base_path
        logger.debug(f"Recordings directory: {self.recordings_dir}")
        
        # Initialize session state for recording handling and results
        if 'new_recording' not in st.session_state:
            st.session_state.new_recording = False
        if 'last_result' not in st.session_state:
            st.session_state.last_result = None
        if 'last_audio' not in st.session_state:
            st.session_state.last_audio = None
    
    def refresh_sidebar(self):
        """Force sidebar to refresh by incrementing a key"""
        st.session_state.recordings_key += 1
    
    def save_audio_file(self, audio_bytes: bytes, filename: str) -> str:
        """Save audio data using StorageManager"""
        logger.debug(f"Saving audio file: {filename}")
        return self.storage_manager.save_recording(
            user_id=st.session_state.user_id,
            audio_data=audio_bytes,
            filename=filename
        )
    
    def initialize_session(self):
        logger.debug("Initializing session state")
        if 'user_id' not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
            logger.debug(f"Created new user_id: {st.session_state.user_id}")
        if 'audio_buffer' not in st.session_state:
            st.session_state.audio_buffer = []
            logger.debug("Initialized empty audio buffer")
    
    def save_test_audio(self):
        """Generate and save a test audio file to verify storage functionality"""
        import numpy as np
        
        logger.debug("Generating test audio file")
        
        # Generate a 1-second test tone
        sample_rate = 48000
        duration = 1  # seconds
        frequency = 440  # Hz (A4 note)
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        test_tone = 0.5 * np.sin(2 * np.pi * frequency * t)
        test_tone = test_tone.astype(np.float32)
        
        # Generate filename
        filename = f"test_tone_{uuid.uuid4()}.wav"
        file_path = os.path.join(self.recordings_dir, filename)
        
        try:
            logger.debug(f"Attempting to save test audio to {file_path}")
            logger.debug(f"Test audio shape: {test_tone.shape}")
            logger.debug(f"Test audio type: {test_tone.dtype}")
            
            import soundfile as sf
            sf.write(file_path, test_tone, sample_rate)
            
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                logger.debug(f"Successfully saved test audio. Size: {file_size} bytes")
                return file_path
            else:
                logger.error("Test file was not created")
                return None
                
        except Exception as e:
            logger.error(f"Error saving test audio: {str(e)}", exc_info=True)
            return None
    
    def run(self):
        self.initialize_session()
        st.title("AI Model Interface")
        
        # Initialize recordings_key if not exists
        if 'recordings_key' not in st.session_state:
            st.session_state.recordings_key = 0
        
        # Sidebar for displaying recordings
        with st.sidebar:
            st.header("Your Recordings")
            recordings = self.db_manager.get_user_recordings(st.session_state.user_id)
            
            if not recordings:
                st.info("No recordings yet")
            else:
                for recording in recordings:
                    # Debug log to see what we're getting
                    logger.debug(f"Recording data: {recording}")
                    
                    try:
                        # Unpack the recording tuple safely
                        recording_data = list(recording)
                        recording_id = recording_data[0]
                        filename = recording_data[2] if len(recording_data) > 2 else "Unknown"
                        model_response = recording_data[3] if len(recording_data) > 3 else None
                        
                        # Create an expander for each recording
                        with st.expander(f"📝 {filename}"):
                            st.write(f"**Recording ID:** {recording_id}")
                            if model_response:
                                try:
                                    response_data = json.loads(model_response)
                                    st.write("**AI Response:**")
                                    st.write(response_data)
                                except json.JSONDecodeError:
                                    st.write(model_response)
                            
                            # Play audio button
                            audio_path = self.storage_manager.get_recording_path(
                                st.session_state.user_id, 
                                filename
                            )
                            if audio_path.exists():
                                st.audio(str(audio_path))
                    except Exception as e:
                        logger.error(f"Error processing recording: {e}")
                        st.error(f"Error displaying recording: {str(e)}")
        
        # Main content area
        st.write("### Record Audio")
        
        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e85252",
            neutral_color="#6aa36f"
        )

        # Display last result if exists
        if st.session_state.last_result:
            st.write("### Result:")
            st.write(st.session_state.last_result)
            if st.session_state.last_audio:
                st.audio(st.session_state.last_audio)

        if audio_bytes and not st.session_state.new_recording:
            try:
                filename = f"recording_{uuid.uuid4()}.wav"
                file_path = self.save_audio_file(audio_bytes, filename)
                
                # Process with model
                with st.spinner("Processing..."):
                    result = self.model.predict(audio_bytes)
                    
                # Save to database with grades
                self.db_manager.save_recording(
                    user_id=st.session_state.user_id,
                    filename=filename,
                    model_response=json.dumps(result),
                    grades=result.get('grades', {})
                )
                
                # Display results including grades
                st.write("### Speech Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Transcription:**")
                    st.write(result['transcription'])
                    
                with col2:
                    st.write("**Grades:**")
                    for grade_name, grade_value in result['grades'].items():
                        st.write(f"{grade_name.title()}: {grade_value:.2f}")
                
                st.audio(audio_bytes)
                
                # Store results in session state
                st.session_state.last_result = result
                st.session_state.last_audio = audio_bytes
                
                # Set flag and rerun
                st.session_state.new_recording = True
                st.rerun()
                
            except Exception as e:
                logger.error(f"Error processing audio: {str(e)}", exc_info=True)
                st.error(f"Error processing audio: {str(e)}")
        else:
            # Reset the recording flag after rerun
            st.session_state.new_recording = False

if __name__ == "__main__":
    # Set up root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S",
        force=True,
    )
    
    logger.debug("Starting application")
    app = StreamlitApp()
    app.run()