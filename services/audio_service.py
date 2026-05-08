import logging
import base64
import io
from typing import Optional, Dict, Any
from openai import OpenAI
from config.settings import config
from utils.decorators_simple import handle_errors, monitor_performance

logger = logging.getLogger(__name__)


class AudioService:
    """Service for AI-powered text-to-speech using OpenAI's advanced TTS"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the audio service with OpenAI API key"""
        self.api_key = api_key or config.api_key
        self.client = None
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                logger.info("AudioService initialized with OpenAI client")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        else:
            logger.warning("No API key provided for AudioService")
    
    @handle_errors()
    @monitor_performance()
    def generate_speech(self, text: str, voice: str = "alloy", model: str = "tts-1-hd") -> Optional[bytes]:
        """
        Generate speech audio using OpenAI's TTS model
        
        Args:
            text: The text to convert to speech
            voice: Voice ID (alloy, echo, fable, onyx, nova, shimmer)
            model: TTS model (tts-1, tts-1-hd)
            
        Returns:
            Audio data as bytes, or None if failed
        """
        if not self.client:
            logger.warning("No OpenAI client available for speech generation")
            return None
        
        try:
            logger.info(f"Generating speech for text: {text[:50]}...")
            
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format="wav"
            )
            
            # Convert audio data to bytes
            audio_bytes = response.content
            logger.info(f"Successfully generated {len(audio_bytes)} bytes of audio data")
            
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return None
    
    @handle_errors()
    def get_available_voices(self) -> Optional[Dict[str, Any]]:
        """Get information about available TTS voices"""
        if not self.client:
            return None
        
        try:
            voices = {
                "alloy": {"name": "Alloy", "language": "English", "gender": "Neutral", "description": "Natural, balanced voice"},
                "echo": {"name": "Echo", "language": "English", "gender": "Male", "description": "Deep, resonant voice"},
                "fable": {"name": "Fable", "language": "English", "gender": "Male", "description": "Expressive, warm voice"},
                "onyx": {"name": "Onyx", "language": "English", "gender": "Male", "description": "Deep, authoritative voice"},
                "nova": {"name": "Nova", "language": "English", "gender": "Female", "description": "Bright, friendly voice"},
                "shimmer": {"name": "Shimmer", "language": "English", "gender": "Female", "description": "Soft, ethereal voice"}
            }
            return voices
        except Exception as e:
            logger.error(f"Error getting voice information: {e}")
            return None
    
    def save_audio_file(self, audio_data: bytes, filename: str) -> bool:
        """
        Save audio data to a file
        
        Args:
            audio_data: Audio data as bytes
            filename: Name for the audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'wb') as f:
                f.write(audio_data)
            logger.info(f"Audio saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving audio file: {e}")
            return False
    
    def get_audio_base64(self, audio_data: bytes) -> str:
        """
        Convert audio data to base64 string for web playback
        
        Args:
            audio_data: Audio data as bytes
            
        Returns:
            Base64 encoded audio string
        """
        try:
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            return audio_b64
        except Exception as e:
            logger.error(f"Error converting audio to base64: {e}")
            return ""


# Create a global instance
audio_service = AudioService()
