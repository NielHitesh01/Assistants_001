"""
Fast JARVIS - Uses smaller Whisper model for speed
"""

import sys
import os
import threading
import time
import webbrowser
from datetime import datetime
import random

# Import dependencies with error handling
try:
    import pyttsx3
    TTS_ENGINE = pyttsx3.init()
    TTS_ENGINE.setProperty('rate', 200)
    TTS_ENGINE.setProperty('volume', 0.9)
    TTS_AVAILABLE = True
    print("✅ Text-to-Speech: READY")
except Exception as e:
    print(f"❌ TTS Error: {e}")
    TTS_ENGINE = None
    TTS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    print("❌ Install: pip install numpy")
    NUMPY_AVAILABLE = False

# Fast Whisper setup
try:
    import whisper
    import sounddevice as sd
    import soundfile as sf
    
    if NUMPY_AVAILABLE:
        print("🧠 Loading Whisper BASE model (fast)...")
        WHISPER_MODEL = whisper.load_model("base")  # Much faster than large
        print("✅ Whisper BASE: READY (Fast & Accurate)")
        WHISPER_AVAILABLE = True
    else:
        WHISPER_AVAILABLE = False
        
except ImportError:
    print("❌ Install: pip install openai-whisper sounddevice soundfile")
    WHISPER_AVAILABLE = False

class FastJARVIS:
    def __init__(self):
        self.running = True
        self.user_name = "Sir"
        self.debug_mode = True
        self.voice_output_enabled = True
        self.systems_active = {}
        
        # Whisper settings
        self.sample_rate = 16000
        self.audio_duration = 3      # Shorter for speed
        self.wake_word_duration = 2  # Shorter for speed
        
        # Wake words
        self.wake_words = ["jarvis", "hey jarvis", "hello jarvis", "computer"]
        
        # Test voice
        if TTS_AVAILABLE:
            try:
                TTS_ENGINE.say("Fast JARVIS initializing")
                TTS_ENGINE.runAndWait()
            except:
                pass

    def record_audio(self, duration, wake_word_mode=False):
        """Record audio quickly"""
        try:
            if not wake_word_mode:
                print("🎙️ Listening...")
            
            audio_data = sd.rec(
                int(duration * self.sample_rate), 
                samplerate=self.sample_rate, 
                channels=1, 
                dtype=np.float32
            )
            sd.wait()
            return audio_data.flatten()
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Recording error: {e}")
            return None

    def whisper_transcribe(self, audio_data, wake_word_mode=False):
        """Fast Whisper transcription"""
        try:
            if audio_data is None:
                return None
            
            result = WHISPER_MODEL.transcribe(
                audio_data, 
                language="en",
                verbose=False,
                fp16=False
            )
            
            text = result["text"].strip().lower()
            
            if text and len(text) > 1:
                if self.debug_mode:
                    print(f"🔍 Heard: '{text}'")
                return text
            else:
                return None
                
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Whisper error: {e}")
            return None

    def listen_for_command(self, wake_word_mode=False):
        """Fast voice recognition"""
        if not WHISPER_AVAILABLE:
            return None
        
        duration = self.wake_word_duration if wake_word_mode else self.audio_duration
        audio_data = self.record_audio(duration, wake_word_mode)
        
        if audio_data is None:
            return None
        
        return self.whisper_transcribe(audio_data, wake_word_mode)

    def speak(self, text):
        """Fast speech output"""
        print(f"🤖 JARVIS: {text}")
        
        if self.voice_output_enabled and TTS_AVAILABLE:
            try:
                TTS_ENGINE.say(text)
                TTS_ENGINE.runAndWait()
            except:
                pass

    def execute_command(self, cmd, original_command):
        """Execute commands quickly"""
        
        if 'time' in cmd:
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}, Sir.")
            return True
            
        elif 'date' in cmd:
            today = datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}, Sir.")
            return True
        
        elif 'youtube' in cmd:
            webbrowser.open('https://youtube.com')
            self.speak("Opening YouTube, Sir.")
            return True
            
        elif 'google' in cmd:
            webbrowser.open('https://google.com')
            self.speak("Opening Google, Sir.")
            return True
        
        elif any(word in cmd for word in ['hello', 'hi', 'hey']):
            greetings = [
                "Hello, Sir! How can I assist you?",
                "Good day, Sir! Ready to help.",
                "Greetings, Sir! What can I do for you?"
            ]
            self.speak(random.choice(greetings))
            return True
            
        elif 'how are you' in cmd:
            responses = [
                "All systems operational, Sir.",
                "Functioning perfectly, Sir.",
                "Running smoothly and ready to assist, Sir."
            ]
            self.speak(random.choice(responses))
            return True
        
        elif any(word in cmd for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.speak("Goodbye, Sir. It was a pleasure serving you.")
            self.running = False
            return True
        
        else:
            responses = [
                "Understood, Sir. How else may I assist?",
                "I hear you, Sir. What else can I help with?",
                "Noted, Sir. Anything else I can do?"
            ]
            self.speak(random.choice(responses))
            return True

    def voice_monitor(self):
        """Fast voice monitoring"""
        if not WHISPER_AVAILABLE:
            print("⚠️ Voice monitoring unavailable")
            return
        
        print("🎤 Fast voice monitoring - Say 'JARVIS' clearly")
        
        while self.running:
            try:
                result = self.listen_for_command(wake_word_mode=True)
                
                if result:
                    # Check for wake words
                    for wake_word in self.wake_words:
                        if wake_word in result:
                            print(f"✅ Wake word detected: '{wake_word}'")
                            
                            # Extract command
                            command_part = result.replace(wake_word, "").strip()
                            
                            if command_part and len(command_part.split()) >= 1:
                                # Direct command
                                print(f"🚀 Direct: '{command_part}'")
                                self.speak("Right away, Sir.")
                                self.execute_command(command_part.lower(), command_part)
                            else:
                                # Just wake word
                                self.speak("Yes, Sir?")
                                
                                # Listen for command
                                command = self.listen_for_command(wake_word_mode=False)
                                
                                if command:
                                    print(f"🚀 Command: '{command}'")
                                    self.execute_command(command.lower(), command)
                                else:
                                    self.speak("Ready when you are, Sir.")
                            
                            break
                
                time.sleep(0.1)
                
            except Exception as e:
                if self.debug_mode:
                    print(f"Voice error: {e}")
                time.sleep(0.5)

    def text_interface(self):
        """Fast text interface"""
        print("\n🚀 FAST JARVIS READY")
        
        if WHISPER_AVAILABLE:
            print("🎤 Voice: Say 'JARVIS' + command")
        else:
            print("⚠️ Voice: DISABLED")
            
        print("⌨️ Text: Type commands")
        print("⚡ Optimized for SPEED")
        
        self.speak("Fast JARVIS ready, Sir.")
            
        while self.running:
            try:
                command = input(f"\n🧠 {self.user_name}: ").strip()
                if command:
                    self.execute_command(command.lower(), command)
            except KeyboardInterrupt:
                print("\n⏹️ Shutting down...")
                self.speak("Goodbye, Sir.")
                self.running = False
                break
            except Exception as e:
                if self.debug_mode:
                    print(f"Error: {e}")
                continue

    def run_system(self):
        """Start Fast JARVIS"""
        print("="*50)
        print("🚀 FAST JARVIS - BASE MODEL")
        print("⚡ Quick & Responsive")
        print("="*50)
        
        # Check systems
        if TTS_AVAILABLE:
            print("✅ Speech: ONLINE")
            self.systems_active['speech'] = True
        else:
            print("❌ Speech: OFFLINE")
            
        if WHISPER_AVAILABLE:
            print("✅ Voice: FAST MODE")
            self.systems_active['microphone'] = True
            
            # Start voice monitoring
            voice_thread = threading.Thread(target=self.voice_monitor, daemon=True)
            voice_thread.start()
        else:
            print("❌ Voice: DISABLED")
        
        print("="*50)
        
        # Start interface
        self.text_interface()

def main():
    try:
        jarvis = FastJARVIS()
        jarvis.run_system()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🔹 Fast JARVIS shutdown complete")

if __name__ == "__main__":
    main()