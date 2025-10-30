"""
Voice Input Module
Handles speech-to-text conversion
"""

from typing import Optional, Dict

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Warning: speech_recognition not available. Voice features will be limited.")


class VoiceModule:
    """
    Voice input module for speech-to-text conversion.
    """

    def __init__(self, language: str = "en-US"):
        """
        Initialize the voice module.
        
        Args:
            language: Language code for recognition
        """
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
        self.language = language

    def _get_microphone(self):
        """Get or initialize microphone."""
        if not SPEECH_RECOGNITION_AVAILABLE:
            return None
        if self.microphone is None:
            self.microphone = sr.Microphone()
        return self.microphone

    def listen_once(self, timeout: Optional[int] = None, 
                    phrase_time_limit: Optional[int] = None) -> Optional[str]:
        """
        Listen for a single voice command.
        
        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for the phrase
            
        Returns:
            Recognized text or None
        """
        if not SPEECH_RECOGNITION_AVAILABLE:
            print("Voice recognition not available")
            return None
        
        try:
            with self._get_microphone() as source:
                print("Listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("Processing...")
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error during voice recognition: {e}")
            return None

    def listen_continuous(self, callback, stop_phrase: str = "stop listening"):
        """
        Continuously listen for voice commands.
        
        Args:
            callback: Function to call with recognized text
            stop_phrase: Phrase to stop listening
        """
        print(f"Starting continuous listening. Say '{stop_phrase}' to stop.")
        
        while True:
            text = self.listen_once()
            
            if text is None:
                continue
            
            if stop_phrase.lower() in text.lower():
                print("Stopping continuous listening")
                break
            
            callback(text)

    def listen_with_wake_word(self, wake_word: str, callback, 
                              timeout: Optional[int] = None):
        """
        Listen for a wake word before processing commands.
        
        Args:
            wake_word: Word/phrase to activate listening
            callback: Function to call with recognized text after wake word
            timeout: Maximum time to wait for wake word
        """
        print(f"Waiting for wake word: '{wake_word}'")
        
        while True:
            text = self.listen_once(timeout=timeout)
            
            if text and wake_word.lower() in text.lower():
                print(f"Wake word detected! Listening for command...")
                command = self.listen_once(phrase_time_limit=10)
                if command:
                    callback(command)

    def get_available_microphones(self):
        """
        Get list of available microphone devices.
        
        Returns:
            List of microphone names
        """
        return sr.Microphone.list_microphone_names()

    def set_microphone_index(self, index: int):
        """
        Set the microphone device to use.
        
        Args:
            index: Microphone device index
        """
        self.microphone = sr.Microphone(device_index=index)

    def test_microphone(self) -> bool:
        """
        Test if microphone is working.
        
        Returns:
            True if microphone is accessible, False otherwise
        """
        try:
            with self._get_microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                return True
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False

    def recognize_from_file(self, audio_file_path: str) -> Optional[str]:
        """
        Recognize speech from an audio file.
        
        Args:
            audio_file_path: Path to audio file (WAV format)
            
        Returns:
            Recognized text or None
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=self.language)
                return text
        except Exception as e:
            print(f"Error recognizing from file: {e}")
            return None

    def set_energy_threshold(self, threshold: int):
        """
        Set the energy threshold for detecting speech.
        
        Args:
            threshold: Energy threshold value (default is 300)
        """
        self.recognizer.energy_threshold = threshold

    def set_dynamic_energy_threshold(self, enabled: bool = True):
        """
        Enable/disable dynamic energy threshold adjustment.
        
        Args:
            enabled: Whether to enable dynamic adjustment
        """
        self.recognizer.dynamic_energy_threshold = enabled
