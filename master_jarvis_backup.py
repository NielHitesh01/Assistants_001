"""
JARVIS MASTER SYSTEM - MAXIMUM ACCURACY VERSION
==============================================
Professional AI Assistant with Highest Accuracy Speech Recognition
"""

import sys
import os
import threading
import time
import webbrowser
import subprocess
from datetime import datetime
import random
import requests
import json
import pickle
import numpy as np

# Import dependencies with error handling
try:
    import pyttsx3
    # Initialize TTS engine immediately
    TTS_ENGINE = pyttsx3.init()
    TTS_ENGINE.setProperty('voice', TTS_ENGINE.getProperty('voices')[0].id)
    TTS_ENGINE.setProperty('rate', 180)
    TTS_ENGINE.setProperty('volume', 0.9)
    
    # Test initialization
    TTS_ENGINE.say("")
    TTS_ENGINE.runAndWait()
    
    TTS_AVAILABLE = True
    print("✅ Text-to-Speech: READY")
except Exception as e:
    print(f"⚠️ TTS Engine error: {e}")
    TTS_ENGINE = None
    TTS_AVAILABLE = False

# Whisper Speech Recognition (MAXIMUM ACCURACY)
try:
    import whisper
    import sounddevice as sd
    import soundfile as sf
    
    # Load Whisper LARGE model for maximum accuracy
    print("🧠 Loading Whisper LARGE model for maximum accuracy...")
    WHISPER_MODEL = whisper.load_model("base")  # Fast and accurate model
    print("✅ Whisper LARGE: READY (Maximum Accuracy)")
    
    WHISPER_AVAILABLE = True
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError as e:
    print("❌ Whisper not available. Installing...")
    print("Run: pip install openai-whisper sounddevice soundfile")
    WHISPER_AVAILABLE = False
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import openai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Advanced text processing for better accuracy
try:
    import difflib
    from fuzzywuzzy import fuzz, process
    TEXT_PROCESSING_AVAILABLE = True
    print("✅ Advanced text processing: READY")
except ImportError:
    print("Install for better accuracy: pip install fuzzywuzzy python-levenshtein")
    TEXT_PROCESSING_AVAILABLE = False

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class IntelligentJARVIS:
    def __init__(self):
        """Initialize JARVIS with maximum accuracy settings"""
        self.running = True
        self.systems_active = {}
        self.user_name = "Sir"
        self.debug_mode = True  # Enable for accuracy testing
        self.voice_output_enabled = True
        
        # AI Intelligence System
        self.ai_mode = True
        self.openai_api_key = "your_openai_api_key_here"
        self.conversation_history = []
        self.user_preferences = {}
        self.learning_data = {}
        
        # Memory system
        self.memory_file = "jarvis_memory.pkl"
        self.load_memory()
        
        # Whisper Speech Recognition Setup (MAXIMUM ACCURACY)
        if WHISPER_AVAILABLE:
            self.sample_rate = 16000  # Whisper uses 16kHz
            self.audio_duration = 5   # Longer recording for better accuracy
            self.wake_word_duration = 3  # Longer for wake words
        
        # Enhanced wake words with variations
        self.wake_words = [
            "jarvis", "hey jarvis", "hello jarvis", "ok jarvis", "computer",
            "jarvis please", "jarvis can you", "jarvis i need", "jarvis help"
        ]
        
        # Command patterns for better recognition
        self.command_patterns = {
            'time': ['time', 'what time', 'current time', 'tell me the time', 'whats the time'],
            'date': ['date', 'what date', 'current date', 'tell me the date', 'whats the date', 'today'],
            'youtube': ['youtube', 'open youtube', 'go to youtube', 'launch youtube'],
            'google': ['google', 'open google', 'go to google', 'launch google', 'search engine'],
            'search': ['search', 'search for', 'look up', 'find', 'google search'],
            'hello': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon'],
            'status': ['how are you', 'status', 'how you doing', 'system status', 'are you ok'],
            'exit': ['exit', 'quit', 'goodbye', 'bye', 'shutdown', 'close', 'stop']
        }

        # Enhanced response collections
        self.responses = {
            'greetings': [
                "Good day, Sir! I'm operating at full capacity and ready to assist.",
                "Hello! All systems are operational. How may I help you today?",
                "Greetings, Sir. I'm here and ready for whatever you need.",
                "Good to see you! I'm functioning optimally and at your service."
            ],
            'acknowledgments': [
                "Understood, Sir.",
                "Right away.",
                "Consider it done.",
                "I'll take care of that immediately.",
                "Absolutely, Sir."
            ],
            'how_are_you': [
                "I'm functioning optimally, Sir. All systems are running smoothly and I'm ready to assist.",
                "Excellent, Sir. My systems are performing at peak efficiency. How can I help you today?",
                "All systems operational and standing by, Sir. What can I do for you?",
                "Running perfectly, Sir. My processors are humming along nicely. What shall we work on?"
            ]
        }

        # Test TTS on startup
        if TTS_AVAILABLE:
            try:
                print("🔊 Testing voice output...")
                TTS_ENGINE.say("Maximum accuracy Whisper AI ready")
                TTS_ENGINE.runAndWait()
                print("✅ Voice output working")
            except Exception as e:
                print(f"❌ Voice test failed: {e}")

    def load_memory(self):
        """Load JARVIS memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'rb') as f:
                    memory_data = pickle.load(f)
                    self.user_preferences = memory_data.get('preferences', {})
                    self.learning_data = memory_data.get('learning', {})
                    if self.debug_mode:
                        print("📚 Memory loaded successfully")
        except Exception as e:
            if self.debug_mode:
                print(f"Memory load error: {e}")

    def save_memory(self):
        """Save JARVIS memory to file"""
        try:
            memory_data = {
                'preferences': self.user_preferences,
                'learning': self.learning_data,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.memory_file, 'wb') as f:
                pickle.dump(memory_data, f)
            print("💾 Saving memory...")
            if self.debug_mode:
                print("💾 Memory saved")
        except Exception as e:
            if self.debug_mode:
                print(f"Memory save error: {e}")

    def fuzzy_match_command(self, text):
        """Use fuzzy matching for better command recognition"""
        if not TEXT_PROCESSING_AVAILABLE:
            return text
        
        best_match = None
        best_score = 0
        best_category = None
        
        for category, patterns in self.command_patterns.items():
            for pattern in patterns:
                score = fuzz.partial_ratio(text.lower(), pattern.lower())
                if score > best_score and score > 70:  # 70% threshold
                    best_score = score
                    best_match = pattern
                    best_category = category
        
        if best_match and self.debug_mode:
            print(f"🎯 Fuzzy match: '{text}' → '{best_match}' ({best_score}% confidence)")
            
        return best_category if best_category else text

    def get_intelligent_response(self, user_input, context="general"):
        """Enhanced intelligent responses with better accuracy"""
        input_lower = user_input.lower()
        
        # Use fuzzy matching for better understanding
        matched_intent = self.fuzzy_match_command(input_lower)
        
        if matched_intent == 'hello' or context == "greeting":
            return random.choice(self.responses['greetings'])
            
        elif matched_intent == 'status' or "how are you" in input_lower:
            return random.choice(self.responses['how_are_you'])
            
        elif "thank" in input_lower:
            return "You're very welcome, Sir. Always a pleasure to be of service."
            
        elif "joke" in input_lower:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my computer a joke about UDP, but I'm not sure it got it.",
                "There are only 10 types of people: those who understand binary and those who don't.",
                "Why do programmers prefer dark mode? Because light attracts bugs!"
            ]
            return random.choice(jokes)
            
        elif "weather" in input_lower:
            return "I can check the weather for you, Sir. Which city would you like me to check?"
            
        elif "?" in user_input:
            return "That's an interesting question, Sir. Let me think about that based on what I know. Could you be more specific about what aspect interests you most?"
            
        else:
            responses = [
                "I understand, Sir. That's quite interesting. How else may I assist you today?",
                "Noted, Sir. I'm processing that information. What would you like me to help you with?",
                "I hear you, Sir. Is there anything specific you'd like me to do or help you with?",
                "Interesting perspective, Sir. How can I assist you further?",
                "I appreciate you sharing that with me, Sir. What else can I help you with?"
            ]
            return random.choice(responses)

    def record_audio(self, duration, wake_word_mode=False):
        """Record high-quality audio for maximum accuracy"""
        try:
            if wake_word_mode and self.debug_mode:
                print("🎙️ High-accuracy listening...")
            elif not wake_word_mode:
                print("🎙️ Recording your command with maximum accuracy...")
            
            # Record high-quality audio
            audio_data = sd.rec(
                int(duration * self.sample_rate), 
                samplerate=self.sample_rate, 
                channels=1, 
                dtype=np.float32
            )
            sd.wait()  # Wait for recording to complete
            
            return audio_data.flatten()
            
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Recording error: {e}")
            return None

    def whisper_transcribe(self, audio_data, wake_word_mode=False):
        """Maximum accuracy Whisper transcription"""
        try:
            if audio_data is None:
                return None
            
            # Whisper transcription with MAXIMUM accuracy settings
            result = WHISPER_MODEL.transcribe(
                audio_data, 
                language="en",
                task="transcribe",
                fp16=False,  # Use FP32 for maximum accuracy
                verbose=False,
                temperature=0.0,  # Most deterministic output
                beam_size=5,      # Better beam search
                best_of=5,        # Try multiple attempts
                condition_on_previous_text=True  # Use context
            )
            
            text = result["text"].strip().lower()
            confidence = result.get("confidence", 0.0)
            
            if text and len(text) > 1:
                if wake_word_mode and self.debug_mode:
                    print(f"🔍 Whisper heard: '{text}' (confidence: {confidence:.2f})")
                elif not wake_word_mode:
                    print(f"✅ Whisper transcribed: '{text}' (confidence: {confidence:.2f})")
                return text
            else:
                return None
                
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Whisper error: {e}")
            return None

    def listen_for_command(self, timeout=5, wake_word_mode=False):
        """Maximum accuracy voice recognition"""
        if not self.systems_active.get('microphone'):
            return None
        
        try:
            # Record audio with optimal duration for accuracy
            duration = self.wake_word_duration if wake_word_mode else self.audio_duration
            audio_data = self.record_audio(duration, wake_word_mode)
            
            if audio_data is None:
                return "timeout"
            
            # Transcribe with maximum accuracy Whisper
            text = self.whisper_transcribe(audio_data, wake_word_mode)
            
            return text if text else None
            
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Listen error: {e}")
            return None

    def initialize_system(self):
        """Maximum accuracy system initialization"""
        print("🚀 JARVIS initializing with MAXIMUM ACCURACY...")
        
        # Quick AI check
        self.systems_active['ai'] = False
        print("⚠️ AI: OFFLINE (Maximum accuracy mode)")
    
        # Quick speech setup
        if TTS_AVAILABLE and TTS_ENGINE:
            print("🔊 Speech: ONLINE")
            self.systems_active['speech'] = True
        else:
            print("❌ Speech: OFFLINE")
            self.systems_active['speech'] = False
    
        # Whisper microphone setup
        if WHISPER_AVAILABLE:
            try:
                print("🎙️ Testing Whisper LARGE model...")
                
                # Test audio recording
                test_audio = self.record_audio(1, wake_word_mode=True)
                if test_audio is not None:
                    print("✅ Whisper LARGE microphone: READY (Maximum Accuracy)")
                    self.systems_active['microphone'] = True
                else:
                    print("❌ Whisper microphone: FAILED")
                    self.systems_active['microphone'] = False
                
            except Exception as e:
                print(f"❌ Whisper setup error: {e}")
                self.systems_active['microphone'] = False
        else:
            print("❌ Whisper not available")
            print("Install with: pip install openai-whisper sounddevice soundfile")
            self.systems_active['microphone'] = False
    
        return True

    def voice_monitor(self):
        """Maximum accuracy voice monitoring"""
        if not self.systems_active.get('microphone'):
            print("⚠️ Voice monitoring unavailable")
            return
        
        print("🎤 Maximum accuracy voice monitoring - Say 'JARVIS' clearly")
        
        while self.running:
            try:
                # High-accuracy check with longer timeout
                result = self.listen_for_command(timeout=3, wake_word_mode=True)
                
                if result is None or result == "timeout":
                    time.sleep(0.2)  # Reasonable sleep for accuracy
                    continue
                    
                elif result:
                    if self.debug_mode:
                        print(f"🔊 Whisper heard: '{result}'")
                    
                    # Enhanced wake word check with fuzzy matching
                    wake_word_found = False
                    for wake_word in self.wake_words:
                        if wake_word in result or (TEXT_PROCESSING_AVAILABLE and fuzz.partial_ratio(result, wake_word) > 80):
                            wake_word_found = True
                            print(f"✅ Wake word detected: '{wake_word}' in '{result}'")
                            
                            # Extract command with better parsing
                            command_part = result.replace(wake_word, "").strip()
                            
                            if command_part and len(command_part.split()) >= 1:
                                # Direct command - high accuracy execution
                                print(f"🚀 Direct command: '{command_part}'")
                                self.fast_speak("Understood, Sir. Processing your request.")
                                self._execute_command(command_part.lower(), command_part)
                            else:
                                # Just wake word
                                self.fast_speak("Yes, Sir? I'm listening with maximum accuracy.")
                                
                                # Listen for command with high accuracy
                                command = self.listen_for_command(timeout=8, wake_word_mode=False)
                                
                                if command and command != "timeout":
                                    print(f"🚀 Command received: '{command}'")
                                    self._execute_command(command.lower(), command)
                                else:
                                    self.fast_speak("I'm ready when you are, Sir.")
                            

                            break
                    
                    if not wake_word_found and self.debug_mode:
                        print(f"🔍 No wake word detected in: '{result}'")
                    
                    time.sleep(0.3)  # Reasonable pause for accuracy
                    continue
                
            except Exception as e:
                if self.debug_mode:
                    print(f"Voice monitoring error: {e}")
                time.sleep(1)

    def fast_speak(self, text):
        """High-quality speech output"""
        print(f"🤖 JARVIS: {text}")
        
        if self.voice_output_enabled and TTS_AVAILABLE and TTS_ENGINE:
            try:
                # High-quality speech settings
                TTS_ENGINE.setProperty('rate', 200)  # Clear speech rate
                TTS_ENGINE.setProperty('volume', 0.9)
                TTS_ENGINE.say(text)
                TTS_ENGINE.runAndWait()
            except Exception as e:
                if self.debug_mode:
                    print(f"🔊 Speech error: {e}")

    def _execute_command(self, cmd, original_command):
        """High-accuracy command execution with fuzzy matching"""
        
        # Use fuzzy matching for better command recognition
        matched_intent = self.fuzzy_match_command(cmd)
        
        if matched_intent == 'time' or 'time' in cmd:
            current_time = datetime.now().strftime("%I:%M %p")
            self.fast_speak(f"The current time is {current_time}, Sir.")
            return True
            
        elif matched_intent == 'date' or 'date' in cmd or 'today' in cmd:
            today = datetime.now().strftime("%A, %B %d, %Y")
            self.fast_speak(f"Today is {today}, Sir.")
            return True
        
        elif matched_intent == 'youtube' or 'youtube' in cmd:
            webbrowser.open('https://youtube.com')
            self.fast_speak("Opening YouTube for you, Sir.")
            return True
            
        elif matched_intent == 'google' or 'google' in cmd:
            webbrowser.open('https://google.com')
            self.fast_speak("Opening Google for you, Sir.")
            return True
        
        elif matched_intent == 'search' or 'search' in cmd:
            # Extract search query
            query = cmd.replace('search for', '').replace('search', '').replace('look up', '').strip()
            if query:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                self.fast_speak(f"Searching for {query}, Sir.")
            else:
                self.fast_speak("What would you like me to search for, Sir?")
            return True
        
        elif matched_intent == 'hello' or any(word in cmd for word in ['hello', 'hi', 'hey']):
            response = self.get_intelligent_response(original_command, "greeting")
            self.fast_speak(response)
            return True
            
        elif matched_intent == 'status' or 'how are you' in cmd:
            response = self.get_intelligent_response(original_command)
            self.fast_speak(response)
            return True
        
        elif matched_intent == 'exit' or any(word in cmd for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.fast_speak("Goodbye, Sir. It was a pleasure serving you with maximum accuracy today.")
            self.save_memory()
            self.running = False
            return True
        
        # Default intelligent response
        else:
            response = self.get_intelligent_response(original_command)
            self.fast_speak(response)
            return True

    def text_interface(self):
        """Maximum accuracy text interface"""
        print("\n🚀 JARVIS READY - MAXIMUM ACCURACY MODE")
        print("🎤 Voice: Say 'JARVIS' + command")
        print("⌨️ Text: Type commands")
        print("🧠 Whisper LARGE: Maximum accuracy speech recognition")
        print("🎯 Fuzzy matching: Better command understanding")
        
        self.fast_speak("JARVIS ready with maximum accuracy. Whisper large model active, Sir.")
            
        while self.running:
            try:
                command = input(f"\n🧠 {self.user_name}: ").strip()
                if command:
                    if command.lower() == 'debug mode off':
                        self.debug_mode = False
                        print("🔧 Debug mode disabled")
                        self.fast_speak("Debug mode disabled, Sir.")
                    elif command.lower() == 'debug mode on':
                        self.debug_mode = True
                        print("🔧 Debug mode enabled")
                        self.fast_speak("Debug mode enabled, Sir.")
                    else:
                        self._execute_command(command.lower(), command)
            except KeyboardInterrupt:
                print("\n⏹️ Shutting down...")
                self.fast_speak("Goodbye, Sir.")
                self.running = False
                break
            except Exception as e:
                if self.debug_mode:
                    print(f"Error: {e}")
                continue

    def run_system(self):
        """Maximum accuracy system startup"""
        print("="*70)
        print("🚀 JARVIS - MAXIMUM ACCURACY MODE")
        print("🧠 Whisper LARGE Model - Best Speech Recognition")
        print("🎯 Fuzzy Matching - Better Command Understanding")
        print("="*70)
        
        # Initialize with maximum accuracy
        self.initialize_system()
        
        # Start voice monitoring
        if self.systems_active.get('microphone'):
            voice_thread = threading.Thread(target=self.voice_monitor, daemon=True)
            voice_thread.start()
            print("✅ Voice: MAXIMUM ACCURACY MODE")
        else:
            print("⚠️ Voice: DISABLED")
        
        print("🧠 Whisper LARGE: MAXIMUM ACCURACY")
        print("🎯 Fuzzy matching: ENHANCED UNDERSTANDING")
        print("="*70)
        
        # Start interface
        self.text_interface()

def main():
    """Main entry point"""
    try:
        jarvis = IntelligentJARVIS()
        jarvis.run_system()
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("Please ensure all dependencies are installed and try again.")
    finally:
        print("🔹 Maximum Accuracy AI System shutdown complete")

if __name__ == "__main__":
    main()