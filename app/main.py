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
        
        # Sidebar for displaying recordings
        with st.sidebar:
            st.header("Your Recordings")
            recordings = self.db_manager.get_user_recordings(st.session_state.user_id)
            
            if not recordings:
                st.info("No recordings yet")
            else:
                for recording in recordings:
                    # Unpack recording data
                    _, _, filename, timestamp, duration, transcription, model_response, metadata = recording
                    
                    # Create an expander for each recording
                    with st.expander(f"📝 {timestamp}"):
                        st.write(f"**Filename:** {filename}")
                        if model_response:
                            try:
                                response_data = json.loads(model_response)
                                st.write("**Transcription:**")
                                st.write(response_data.get('transcription', 'No transcription available'))
                                st.write("**AI Response:**")
                                st.write(response_data.get('response', 'No response available'))
                                
                                # Display metadata if available
                                if 'metadata' in response_data:
                                    st.write("**Metadata:**")
                                    st.json(response_data['metadata'])
                            except json.JSONDecodeError:
                                st.write(model_response)
                        
                        # Play audio button
                        audio_path = self.storage_manager.get_recording_path(
                            st.session_state.user_id, 
                            filename
                        )
                        if audio_path.exists():
                            st.audio(str(audio_path))
        
        # Add test button at the top
        st.write("### Test Audio System")
        if st.button("Save Test Audio"):
            test_file = self.save_test_audio()
            if test_file:
                st.success(f"Test audio saved successfully to {test_file}")
                st.audio(test_file)
            else:
                st.error("Failed to save test audio")
        
        st.write("---")  # Add a separator
        
        # Main content area
        st.write("### Record Audio")
        
        # Use audio_recorder instead of st.audio_recorder
        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e85252",
            neutral_color="#6aa36f"
        )

        if audio_bytes:
            # Save the recorded audio
            try:
                filename = f"recording_{uuid.uuid4()}.wav"
                file_path = self.save_audio_file(audio_bytes, filename)
                
                logger.debug(f"Saved recorded audio to {file_path}")
                
                # Process with model
                with st.spinner("Processing..."):
                    result = self.model.predict(audio_bytes)
                    logger.debug(f"Model prediction result: {result}")
                
                # Save to database - convert dict to JSON string
                logger.debug(f"Saving recording metadata to database")
                self.db_manager.save_recording(
                    user_id=st.session_state.user_id,
                    filename=filename,
                    model_response=json.dumps(result)  # Convert dict to JSON string
                )
                
                # Show results
                st.write("### Result:")
                st.write(result)
                st.audio(audio_bytes)
                
            except Exception as e:
                logger.error(f"Error processing audio: {str(e)}", exc_info=True)
                st.error(f"Error processing audio: {str(e)}")

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