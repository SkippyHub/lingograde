import os
from dotenv import load_dotenv
import time
from typing import Union, Dict, Any
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from google.cloud import speech
import json
import datetime
import logging

# Load environment variables
load_dotenv()

print("\n=== Google Cloud Configuration ===")
print(f"Project ID: {os.getenv('GOOGLE_CLOUD_PROJECT_ID')}")
print("=============================================\n")

class AIModel:
    def __init__(self):
        self.loaded = False
        try:
            print("\n Initializing Google Cloud clients...")
            # Initialize Speech-to-Text client
            self.speech_client = speech.SpeechClient()
            
            # Initialize Vertex AI
            vertexai.init(
                project=os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
                location=os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
            )
            
            # Get Gemini model
            self.model = GenerativeModel("gemini-pro")
            
            # Configure generation settings
            self.generation_config = {
                "max_output_tokens": 8192,
                "temperature": 1,
                "top_p": 0.95,
            }
            
            # Configure safety settings
            self.safety_settings = [
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=SafetySetting.HarmBlockThreshold.OFF
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=SafetySetting.HarmBlockThreshold.OFF
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=SafetySetting.HarmBlockThreshold.OFF
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=SafetySetting.HarmBlockThreshold.OFF
                ),
            ]
            
            self.loaded = True
            print("✅ Google Cloud clients initialized successfully!")
            
            print("=============================================\n")
        except Exception as e:
            print("\n❌ Error initializing clients:")
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
            audio = processed_data.get("audio")
            config = processed_data.get("config")
            
            if not audio or not config:
                raise ValueError("Missing audio or config in processed data")
            
            print("Starting transcription...")
            response = self.speech_client.recognize(config=config, audio=audio)
            
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

    def grade_response(self, question: str, response: str) -> dict:
            """
            Grade a user's response using Gemini
            Returns a structured format for both database storage and API response
            """
            try:
                prompt = f"""
                Given a question and user response, return a JSON format evaluating the user's response based on coherence, grammar, and vocabulary.

                Question: "{question}"
                User Response: "{response}"

                Return only a JSON format with:
                {{
                    "coherence": (score between 0-1),
                    "grammar": (score between 0-1),
                    "vocabulary": (score between 0-1),
                    "explanation": "brief explanation of the grades",
                    "notes": "additional observations about the response"
                }}

                Definitions:
                - Coherence: Measures how clearly and logically the response aligns with the question
                - Grammar: Evaluates grammatical correctness of the response
                - Vocabulary: Assesses the diversity and appropriateness of vocabulary used
                """

                print("\n🤖 Sending grading prompt to Gemini:")
                print(prompt)
                print("=============================================\n")

                # Get Gemini's response
                gemini_response = self.model.generate_content(prompt)
                
                # Parse the response
                try:
                    # Extract JSON from response text
                    response_text = gemini_response.text
                    # Find the JSON block between ```json and ```
                    json_str = response_text[response_text.find('{'):response_text.rfind('}')+1]
                    grading_result = json.loads(json_str)
                    
                    # Add timestamp for database storage
                    grading_result['timestamp'] = datetime.datetime.utcnow().isoformat()
                    
                    return grading_result
                    
                except json.JSONDecodeError:
                    return {
                        'coherence': 0.0,
                        'grammar': 0.0,
                        'vocabulary': 0.0,
                        'explanation': 'Failed to parse response',
                        'notes': 'Error occurred during grading',
                        'timestamp': datetime.datetime.utcnow().isoformat()
                    }
                    
            except Exception as e:
                logging.error(f"Error in grade_response: {str(e)}")
                return {
                    'coherence': 0.0,
                    'grammar': 0.0,
                    'vocabulary': 0.0,
                    'explanation': 'Failed to parse response',
                    'notes': 'Error occurred during grading',
                    'timestamp': datetime.datetime.utcnow().isoformat()
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
            
            # Get detailed grading
            grading_result = self.grade_response(
                "Describe your ideal vacation destination",  # This should come from the prompt
                transcription
            )
            
            return {
                "status": "success",
                "transcription": transcription,
                "grading_details": grading_result,
                "metadata": {
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

    