import os
from dotenv import load_dotenv
import time
from typing import Union, Dict, Any
import random
from google.cloud import speech
import io

# Load environment variables
load_dotenv()

# Now you can access the variables like this:
project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
api_key = os.getenv('GOOGLE_CLOUD_API_KEY')

print("\n=== Google Cloud Speech-to-Text Configuration ===")
print(f"Project ID: {project_id}")
print(f"Credentials file: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
print("=============================================\n")

class AIModel:
    def __init__(self):
        self.loaded = False
        try:
            # Initialize the Speech-to-Text client
            print("\n Initializing Google Cloud Speech-to-Text client...")
            self.client = speech.SpeechClient()
            self.loaded = True
            print("✅ Google Cloud Speech client initialized successfully!")
            print("=============================================\n")
        except Exception as e:
            print("\n❌ Error initializing Speech client:")
            print(f"Error details: {str(e)}")
            print("=============================================\n")
            raise
    
    def preprocess_audio(self, audio_bytes: bytes) -> Dict[str, Any]:
        """Process audio for Google Cloud Speech-to-Text"""
        try:
            print("\n🎵 Processing audio...")
            print(f"Audio size: {len(audio_bytes)} bytes")
            
            # Convert the audio bytes to proper format if needed
            audio = speech.RecognitionAudio(content=audio_bytes)
            
            # Define the recognition config with the correct sample rate
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code="en-US",
                enable_automatic_punctuation=True,
                use_enhanced=True,
                model="default"
            )
            
            print("✅ Audio preprocessing complete")
            print(f"Sample rate: 48000 Hz")
            print(f"Encoding: WEBM_OPUS")
            print("=============================================\n")
            
            return {
                "audio": audio,
                "config": config,
                "duration": len(audio_bytes) / 48000
            }
        except Exception as e:
            print("\n❌ Error in preprocessing:")
            print(f"Error details: {str(e)}")
            print("=============================================\n")
            raise
    
    def transcribe_audio(self, processed_data: Dict[str, Any]) -> str:
        """Transcribe audio using Google Cloud Speech-to-Text"""
        try:
            # Get the audio and config from processed data
            audio = processed_data.get("audio")
            config = processed_data.get("config")
            
            if not audio or not config:
                raise ValueError("Missing audio or config in processed data")
            
            # Perform the transcription
            print("Starting transcription...")
            response = self.client.recognize(config=config, audio=audio)
            
            # Process the response
            transcript = ""
            for result in response.results:
                alternative = result.alternatives[0]
                transcript += alternative.transcript + " "
                print(f"Confidence: {alternative.confidence}")
                
            if not transcript:
                print("No transcription result")
                return "Could not transcribe audio"
                
            print(f"Transcription completed: {transcript.strip()}")
            return transcript.strip()
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            raise
    
    def generate_response(self, text: str) -> Dict[str, Any]:
        """Simulate AI response generation"""
        # Simulate some processing time
        time.sleep(0.5)
        
        # use gemma model to generate questions.
        
        responses = {
            "Hello, how can I help you today?": {
                "response": "I'm here to help! What would you like to know?",
                "confidence": 0.92,
                "sentiment": "positive"
            },
            "I'd like to schedule an appointment.": {
                "response": "I can help you schedule an appointment. What time works best for you?",
                "confidence": 0.88,
                "sentiment": "neutral"
            },
            "Could you please explain that again?": {
                "response": "I'll try to explain more clearly. Which part would you like me to clarify?",
                "confidence": 0.85,
                "sentiment": "neutral"
            },
            "Thank you for your assistance.": {
                "response": "You're welcome! Let me know if you need anything else.",
                "confidence": 0.95,
                "sentiment": "positive"
            }
        }
        
        return responses.get(text, {
            "response": "I'm not sure I understood that correctly. Could you rephrase?",
            "confidence": 0.6,
            "sentiment": "neutral"
        })
    
    def generate_speech_grades(self, text: str) -> Dict[str, float]:
        """Generate speech quality grades"""
        # In a real implementation, this would use actual NLP models
        # For now, we'll generate realistic-looking random grades
        
        
        
        return {
            'pronunciation': round(random.uniform(0.6, 1.0), 2),
            'fluency': round(random.uniform(0.6, 1.0), 2),
            'coherence': round(random.uniform(0.6, 1.0), 2),
            'grammar': round(random.uniform(0.6, 1.0), 2),
            'vocabulary': round(random.uniform(0.6, 1.0), 2)
        }
    
    def predict(self, audio_bytes: bytes) -> Dict[str, Any]:
        """Main prediction pipeline"""
        if not self.loaded:
            raise RuntimeError("Model not loaded")
        
        try:
            # Process audio
            processed_data = self.preprocess_audio(audio_bytes)
            
            # Get transcription
            transcription = self.transcribe_audio(processed_data)
            
            # Generate response
            response = self.generate_response(transcription)
            
            # Generate speech grades
            grades = self.generate_speech_grades(transcription)
            
            return {
                "status": "success",
                "transcription": transcription,
                "response": response["response"],
                "grades": grades,
                "metadata": {
                    "confidence": response["confidence"],
                    "sentiment": response["sentiment"],
                    "audio_duration": processed_data["duration"],
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }