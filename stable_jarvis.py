"""
Stable JARVIS - Handles audio errors gracefully (FIXED)
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

# Try to load Whisper with better error handling
WHISPER_AVAILABLE = False
NUMPY_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
    print("✅ NumPy: READY")
except ImportError:
    print("❌ NumPy: Install with 'pip install numpy'")

try:
    import whisper
    import sounddevice as sd
    import soundfile as sf
    
    if NUMPY_AVAILABLE:
        # Test audio device first
        print("🔍 Testing audio devices...")
        devices = sd.query_devices()
        print(f"📱 Found {len(devices)} audio devices")
        
        # Try to find a working input device
        input_device = None
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                input_device = i
                print(f"🎙️ Using device {i}: {device['name']}")
                break
        
        if input_device is not None:
            print("🧠 Loading Whisper BASE model...")
            WHISPER_MODEL = whisper.load_model("base")
            print("✅ Whisper BASE: READY")
            WHISPER_AVAILABLE = True
        else:
            print("❌ No suitable microphone found")
            WHISPER_AVAILABLE = False
    else:
        WHISPER_AVAILABLE = False
        
except ImportError:
    print("❌ Whisper: Install with 'pip install openai-whisper sounddevice soundfile'")
    WHISPER_AVAILABLE = False
except Exception as e:
    print(f"❌ Audio setup error: {e}")
    WHISPER_AVAILABLE = False

class StableJARVIS:
    def __init__(self):
        self.running = True
        self.user_name = "Sir"
        self.debug_mode = True
        self.voice_output_enabled = True
        self.systems_active = {}
        self.audio_errors = 0
        self.max_audio_errors = 5
        self.voice_enabled = WHISPER_AVAILABLE  # Track voice state locally
        
        # Whisper settings
        self.sample_rate = 16000
        self.audio_duration = 3
        self.wake_word_duration = 2
        
        # Wake words
        self.wake_words = ["jarvis", "hey jarvis", "hello jarvis", "computer"]
        
        # Test voice
        if TTS_AVAILABLE:
            try:
                TTS_ENGINE.say("Stable JARVIS initializing")
                TTS_ENGINE.runAndWait()
            except Exception as e:
                print(f"❌ Voice test failed: {e}")

    def record_audio_safe(self, duration, wake_word_mode=False):
        """Safely record audio with error handling"""
        try:
            if not wake_word_mode:
                print("🎙️ Listening...")
            
            # Reset error counter on successful attempt
            self.audio_errors = 0
            
            # Record with specific device if available
            audio_data = sd.rec(
                int(duration * self.sample_rate), 
                samplerate=self.sample_rate, 
                channels=1, 
                dtype=np.float32,
                device=None  # Let sounddevice choose
            )
            sd.wait()
            return audio_data.flatten()
            
        except Exception as e:
            self.audio_errors += 1
            if self.debug_mode:
                print(f"❌ Audio error #{self.audio_errors}: {e}")
            
            # Disable voice after too many errors
            if self.audio_errors >= self.max_audio_errors:
                print(f"⚠️ Too many audio errors ({self.audio_errors}). Disabling voice recognition.")
                self.voice_enabled = False
                return None
            
            time.sleep(1)  # Wait before retry
            return None

    def whisper_transcribe_safe(self, audio_data, wake_word_mode=False):
        """Safely transcribe with Whisper"""
        try:
            if audio_data is None or not WHISPER_AVAILABLE:
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
                print(f"❌ Transcription error: {e}")
            return None

    def listen_for_command_safe(self, wake_word_mode=False):
        """Safely listen for commands"""
        if not self.voice_enabled or not WHISPER_AVAILABLE:
            return None
        
        duration = self.wake_word_duration if wake_word_mode else self.audio_duration
        audio_data = self.record_audio_safe(duration, wake_word_mode)
        
        if audio_data is None:
            return None
        
        return self.whisper_transcribe_safe(audio_data, wake_word_mode)

    def speak(self, text):
        """Safe speech output"""
        print(f"🤖 JARVIS: {text}")
        
        if self.voice_output_enabled and TTS_AVAILABLE:
            try:
                TTS_ENGINE.say(text)
                TTS_ENGINE.runAndWait()
            except Exception as e:
                if self.debug_mode:
                    print(f"❌ Speech error: {e}")

    def execute_command(self, cmd, original_command):
        """Execute commands"""
        
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
        
        elif 'disable voice' in cmd:
            self.voice_enabled = False
            self.speak("Voice recognition disabled, Sir. Text mode only.")
            return True
            
        elif 'enable voice' in cmd:
            if WHISPER_AVAILABLE:
                self.voice_enabled = True
                self.audio_errors = 0
                self.speak("Attempting to enable voice recognition, Sir.")
            else:
                self.speak("Voice recognition not available, Sir. Missing dependencies.")
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

    def voice_monitor_safe(self):
        """Safe voice monitoring with error recovery"""
        if not self.voice_enabled or not WHISPER_AVAILABLE:
            print("⚠️ Voice monitoring unavailable")
            return
        
        print("🎤 Safe voice monitoring - Say 'JARVIS' clearly")
        consecutive_errors = 0
        
        while self.running and self.voice_enabled and WHISPER_AVAILABLE:
            try:
                result = self.listen_for_command_safe(wake_word_mode=True)
                
                if result:
                    consecutive_errors = 0  # Reset on success
                    
                    # Check for wake words
                    wake_word_found = False
                    for wake_word in self.wake_words:
                        if wake_word in result:
                            wake_word_found = True
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
                                command = self.listen_for_command_safe(wake_word_mode=False)
                                
                                if command:
                                    print(f"🚀 Command: '{command}'")
                                    self.execute_command(command.lower(), command)
                                else:
                                    self.speak("Ready when you are, Sir.")
                            

                            break
                    
                    if not wake_word_found and self.debug_mode:
                        print(f"🔍 No wake word in: '{result}'")
                
                elif result is None:
                    consecutive_errors += 1
                    if consecutive_errors > 10:
                        print("⚠️ Too many consecutive errors. Taking a break...")
                        time.sleep(5)
                        consecutive_errors = 0
                
                time.sleep(0.2)  # Reasonable pause
                
            except Exception as e:
                consecutive_errors += 1
                if self.debug_mode:
                    print(f"Voice monitor error: {e}")
                
                if consecutive_errors > 5:
                    print("❌ Voice monitoring failed. Switching to text-only mode.")
                    self.voice_enabled = False
                    break
                
                time.sleep(1)

    def text_interface(self):
        """Text interface with voice status"""
        print("\n🚀 STABLE JARVIS READY")
        
        if self.voice_enabled and WHISPER_AVAILABLE:
            print("🎤 Voice: Say 'JARVIS' + command")
        else:
            print("⚠️ Voice: DISABLED (use 'enable voice' to retry)")
            
        print("⌨️ Text: Type commands")
        print("🛡️ Error-resistant design")
        print("💡 Commands: time, date, youtube, google, hello, exit")
        print("🔧 Special: 'disable voice', 'enable voice'")
        
        self.speak("Stable JARVIS ready, Sir.")
            
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
        """Start Stable JARVIS"""
        print("="*60)
        print("🚀 STABLE JARVIS - ERROR RESISTANT")
        print("🛡️ Safe Audio Handling")
        print("="*60)
        
        # Check systems
        if TTS_AVAILABLE:
            print("✅ Speech: ONLINE")
            self.systems_active['speech'] = True
        else:
            print("❌ Speech: OFFLINE")
            
        if self.voice_enabled and WHISPER_AVAILABLE:
            print("✅ Voice: SAFE MODE")
            self.systems_active['microphone'] = True
            
            # Start voice monitoring
            voice_thread = threading.Thread(target=self.voice_monitor_safe, daemon=True)
            voice_thread.start()
        else:
            print("❌ Voice: DISABLED")
        
        print("="*60)
        
        # Start interface
        self.text_interface()

def main():
    try:
        jarvis = StableJARVIS()
        jarvis.run_system()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📋 Quick fix suggestions:")
        print("1. pip install pyttsx3")
        print("2. pip install numpy")
        print("3. pip install openai-whisper sounddevice soundfile")
    finally:
        print("🔹 Stable JARVIS shutdown complete")

if __name__ == "__main__":
    main()