"""
Enhanced JARVIS - Text + Voice Input with Better Audio Handling
Builds on the working Text JARVIS foundation
"""

import sys
import os
import time
import webbrowser
from datetime import datetime
import random
import threading
import queue

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

# Enhanced audio handling
VOICE_INPUT_AVAILABLE = False
WHISPER_MODEL = None

try:
    import numpy as np
    print("✅ NumPy: READY")
    
    # Try different audio backends
    audio_backend = None
    
    # Method 1: Try sounddevice first
    try:
        import sounddevice as sd
        
        # Test audio devices
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        
        if input_devices:
            print(f"✅ SoundDevice: Found {len(input_devices)} input devices")
            
            # Set default input device to first available
            default_input = None
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    default_input = i
                    print(f"🎙️ Default microphone: {device['name']}")
                    break
            
            if default_input is not None:
                sd.default.device[0] = default_input  # Set input device
                audio_backend = 'sounddevice'
                print("✅ Audio Backend: SoundDevice")
        else:
            print("❌ SoundDevice: No input devices found")
            
    except Exception as e:
        print(f"❌ SoundDevice failed: {e}")
    
    # Method 2: Try PyAudio as fallback
    if audio_backend is None:
        try:
            import pyaudio
            
            # Test PyAudio
            pa = pyaudio.PyAudio()
            device_count = pa.get_device_count()
            
            input_devices = []
            for i in range(device_count):
                info = pa.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    input_devices.append(info)
            
            pa.terminate()
            
            if input_devices:
                print(f"✅ PyAudio: Found {len(input_devices)} input devices")
                audio_backend = 'pyaudio'
                print("✅ Audio Backend: PyAudio")
            else:
                print("❌ PyAudio: No input devices found")
                
        except Exception as e:
            print(f"❌ PyAudio failed: {e}")
    
    # Load Whisper if audio backend is available
    if audio_backend:
        try:
            import whisper
            print("🧠 Loading Whisper model...")
            
            # Use 'tiny' model for speed and reliability
            WHISPER_MODEL = whisper.load_model("tiny")
            print("✅ Whisper TINY: READY (Fast & Reliable)")
            VOICE_INPUT_AVAILABLE = True
            
        except Exception as e:
            print(f"❌ Whisper failed: {e}")
            print("Install with: pip install openai-whisper")
    
    # Import soundfile for audio processing
    if VOICE_INPUT_AVAILABLE:
        try:
            import soundfile as sf
            print("✅ Audio processing: READY")
        except ImportError:
            print("❌ Install soundfile: pip install soundfile")
            VOICE_INPUT_AVAILABLE = False

except ImportError as e:
    print(f"❌ NumPy required: {e}")
    print("Install with: pip install numpy")

if not VOICE_INPUT_AVAILABLE:
    print("⚠️ Voice input disabled - using text-only mode")

class EnhancedJARVIS:
    def __init__(self):
        self.running = True
        self.user_name = "Sir"
        self.debug_mode = False
        self.voice_output_enabled = True
        self.voice_input_enabled = VOICE_INPUT_AVAILABLE
        
        # Voice recognition settings
        self.sample_rate = 16000
        self.chunk_duration = 2  # Shorter chunks for responsiveness
        self.wake_word_duration = 3
        self.command_duration = 5
        
        # Wake words (flexible matching)
        self.wake_words = [
            "jarvis", "hey jarvis", "hello jarvis", 
            "computer", "assistant", "hey computer"
        ]
        
        # Audio queue for processing
        self.audio_queue = queue.Queue()
        self.listening_for_command = False
        
        # Test voice output
        if TTS_AVAILABLE:
            try:
                TTS_ENGINE.say("Enhanced JARVIS initializing")
                TTS_ENGINE.runAndWait()
                print("✅ Voice output tested successfully")
            except Exception as e:
                print(f"❌ Voice test failed: {e}")
                self.voice_output_enabled = False

    def speak(self, text):
        """Reliable speech output"""
        print(f"🤖 JARVIS: {text}")
        
        if self.voice_output_enabled and TTS_AVAILABLE:
            try:
                TTS_ENGINE.say(text)
                TTS_ENGINE.runAndWait()
            except Exception as e:
                if self.debug_mode:
                    print(f"❌ Speech error: {e}")

    def record_audio_chunk(self, duration):
        """Record audio with better error handling"""
        try:
            if audio_backend == 'sounddevice':
                import sounddevice as sd
                
                audio_data = sd.rec(
                    int(duration * self.sample_rate),
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype=np.float32
                )
                sd.wait()
                return audio_data.flatten()
                
            elif audio_backend == 'pyaudio':
                import pyaudio
                
                pa = pyaudio.PyAudio()
                
                stream = pa.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=1024
                )
                
                frames = []
                for _ in range(int(self.sample_rate / 1024 * duration)):
                    data = stream.read(1024)
                    frames.append(np.frombuffer(data, dtype=np.float32))
                
                stream.stop_stream()
                stream.close()
                pa.terminate()
                
                return np.concatenate(frames)
            
            else:
                return None
                
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Audio recording error: {e}")
            return None

    def transcribe_audio(self, audio_data):
        """Transcribe audio with Whisper"""
        try:
            if audio_data is None or WHISPER_MODEL is None:
                return None
            
            # Quick transcription with tiny model
            result = WHISPER_MODEL.transcribe(
                audio_data,
                language="en",
                verbose=False,
                temperature=0.2,  # Slightly more deterministic
                no_speech_threshold=0.6,  # Filter out silence
                condition_on_previous_text=False  # Fresh context each time
            )
            
            text = result["text"].strip().lower()
            
            if len(text) > 1:
                if self.debug_mode:
                    print(f"🔍 Transcribed: '{text}'")
                return text
            else:
                return None
                
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Transcription error: {e}")
            return None

    def listen_for_wake_word(self):
        """Listen for wake words in background"""
        if not self.voice_input_enabled:
            return
        
        print("🎤 Listening for wake word... (say 'JARVIS')")
        
        while self.running and self.voice_input_enabled:
            try:
                # Short audio chunks for responsiveness
                audio_chunk = self.record_audio_chunk(self.chunk_duration)
                
                if audio_chunk is not None:
                    text = self.transcribe_audio(audio_chunk)
                    
                    if text:
                        # Check for wake words
                        for wake_word in self.wake_words:
                            if wake_word in text:
                                print(f"✅ Wake word detected: '{wake_word}' in '{text}'")
                                
                                # Check if there's a command after the wake word
                                command_part = text.replace(wake_word, "").strip()
                                
                                if len(command_part) > 2:  # Has command
                                    print(f"🚀 Direct command: '{command_part}'")
                                    self.speak("Right away, Sir.")
                                    self.execute_command(command_part, command_part)
                                else:
                                    # Just wake word - listen for command
                                    self.listen_for_command()
                                
                                break
                
                time.sleep(0.1)  # Small pause for system resources
                
            except Exception as e:
                if self.debug_mode:
                    print(f"❌ Wake word detection error: {e}")
                time.sleep(1)

    def listen_for_command(self):
        """Listen for a command after wake word"""
        try:
            self.listening_for_command = True
            self.speak("Yes, Sir? I'm listening.")
            
            print("🎙️ Listening for command...")
            
            # Longer recording for full command
            audio_data = self.record_audio_chunk(self.command_duration)
            
            if audio_data is not None:
                text = self.transcribe_audio(audio_data)
                
                if text and len(text) > 1:
                    print(f"🚀 Command received: '{text}'")
                    self.execute_command(text, text)
                else:
                    self.speak("I didn't catch that, Sir. Please try again.")
            else:
                self.speak("I'm ready when you are, Sir.")
            
            self.listening_for_command = False
            
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Command listening error: {e}")
            self.speak("I encountered an audio issue, Sir. Please use text commands.")
            self.listening_for_command = False

    def execute_command(self, cmd, original_command):
        """Execute commands (same as Text JARVIS + voice controls)"""
        
        if any(word in cmd for word in ['time', 'what time', 'current time']):
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}, Sir.")
            return True
            
        elif any(word in cmd for word in ['date', 'what date', 'today', 'current date']):
            today = datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}, Sir.")
            return True
        
        elif any(word in cmd for word in ['youtube', 'open youtube', 'launch youtube']):
            webbrowser.open('https://youtube.com')
            self.speak("Opening YouTube for you, Sir.")
            return True
            
        elif any(word in cmd for word in ['google', 'open google', 'launch google']):
            webbrowser.open('https://google.com')
            self.speak("Opening Google for you, Sir.")
            return True
        
        elif 'search' in cmd:
            search_terms = ['search for', 'search', 'look up', 'find']
            query = cmd
            for term in search_terms:
                query = query.replace(term, '').strip()
            
            if query:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                self.speak(f"Searching for {query}, Sir.")
            else:
                self.speak("What would you like me to search for, Sir?")
            return True
        
        elif any(word in cmd for word in ['hello', 'hi', 'hey', 'greetings']):
            greetings = [
                "Hello, Sir! How can I assist you today?",
                "Good day, Sir! I'm ready to help.",
                "Greetings, Sir! What can I do for you?",
                "Hello! All systems operational and at your service, Sir."
            ]
            self.speak(random.choice(greetings))
            return True
            
        elif any(phrase in cmd for phrase in ['how are you', 'status', 'system status']):
            status_info = []
            if TTS_AVAILABLE:
                status_info.append("speech output online")
            if self.voice_input_enabled:
                status_info.append("voice input active")
            
            status_text = ", ".join(status_info) if status_info else "basic systems"
            self.speak(f"All systems operational, Sir. {status_text} and ready to assist.")
            return True
        
        elif 'joke' in cmd:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my computer a joke about UDP, but I'm not sure it got it.",
                "There are only 10 types of people: those who understand binary and those who don't.",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
            ]
            self.speak(random.choice(jokes))
            return True
        
        # Voice control commands
        elif any(phrase in cmd for phrase in ['disable voice', 'turn off voice', 'voice off']):
            self.voice_input_enabled = False
            self.speak("Voice input disabled, Sir. Text commands only.")
            return True
            
        elif any(phrase in cmd for phrase in ['enable voice', 'turn on voice', 'voice on']):
            if VOICE_INPUT_AVAILABLE:
                self.voice_input_enabled = True
                self.speak("Voice input enabled, Sir.")
                # Restart voice monitoring
                if not hasattr(self, 'voice_thread') or not self.voice_thread.is_alive():
                    self.start_voice_monitoring()
            else:
                self.speak("Voice input not available, Sir. Missing audio dependencies.")
            return True
        
        elif any(word in cmd for word in ['exit', 'quit', 'goodbye', 'bye', 'shutdown']):
            self.speak("Goodbye, Sir. It was a pleasure serving you today.")
            self.running = False
            return True
        
        elif 'help' in cmd:
            help_text = """Available commands, Sir:
            - Time: Ask for current time
            - Date: Ask for today's date  
            - YouTube: Open YouTube
            - Google: Open Google
            - Search: Search for anything
            - Hello: Greetings
            - Status: System status
            - Joke: Tell a joke
            - Voice on/off: Control voice input
            - Help: Show this help
            - Exit: Shutdown JARVIS"""
            self.speak("Here are my available commands, Sir.")
            print(help_text)
            return True
        
        else:
            responses = [
                "I understand, Sir. How else may I assist you today?",
                "Noted, Sir. What else can I help you with?",
                "I hear you, Sir. Is there anything specific you'd like me to do?",
                "Understood, Sir. What other tasks can I handle for you?",
                "I'm processing that, Sir. How else may I be of service?"
            ]
            self.speak(random.choice(responses))
            return True

    def start_voice_monitoring(self):
        """Start voice monitoring in background thread"""
        if self.voice_input_enabled and VOICE_INPUT_AVAILABLE:
            self.voice_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
            self.voice_thread.start()
            return True
        return False

    def text_interface(self):
        """Enhanced text interface with voice status"""
        print("\n" + "="*70)
        print("🚀 ENHANCED JARVIS - TEXT + VOICE")
        print("="*70)
        print("⌨️ Text Commands: Type your requests")
        print("🎤 Voice Output: Enabled" if self.voice_output_enabled else "🔇 Voice Output: Disabled")
        
        if self.voice_input_enabled:
            print("🎙️ Voice Input: Enabled - Say 'JARVIS' + command")
        else:
            print("⚠️ Voice Input: Disabled (type 'enable voice' to retry)")
        
        print("🛡️ Dual Mode Interface")
        print("")
        print("💡 Quick Commands:")
        print("   • time, date, youtube, google")
        print("   • search [query], hello, status, joke")
        print("   • enable voice, disable voice")
        print("   • help, exit")
        print("="*70)
        
        self.speak("Enhanced JARVIS ready with voice and text capabilities, Sir.")
            
        while self.running:
            try:
                if not self.listening_for_command:  # Don't show prompt during voice command
                    command = input(f"\n🧠 {self.user_name}: ").strip()
                    if command:
                        print(f"📝 Processing: '{command}'")
                        self.execute_command(command.lower(), command)
                    else:
                        print("💭 Waiting for your command, Sir...")
                else:
                    time.sleep(0.1)  # Wait during voice command processing
                    
            except KeyboardInterrupt:
                print("\n⏹️ Shutting down...")
                self.speak("Goodbye, Sir.")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.speak("I encountered an error, Sir. Please try again.")
                continue

    def run_system(self):
        """Start Enhanced JARVIS"""
        print("="*70)
        print("🚀 ENHANCED JARVIS - VOICE + TEXT EDITION")
        print("🎤 Advanced Audio Processing")
        print("="*70)
        
        # System status
        print("🔍 System Status:")
        if TTS_AVAILABLE:
            print("✅ Speech Output: ONLINE")
        else:
            print("❌ Speech Output: OFFLINE")
        
        if VOICE_INPUT_AVAILABLE:
            print(f"✅ Voice Input: ONLINE ({audio_backend})")
        else:
            print("❌ Voice Input: OFFLINE")
        
        print("✅ Text Interface: ONLINE") 
        print("✅ Web Browser: ONLINE")
        print("✅ Command Processing: ONLINE")
        print("✅ Error Handling: ACTIVE")
        
        print("="*70)
        
        # Start voice monitoring if available
        if self.voice_input_enabled:
            voice_started = self.start_voice_monitoring()
            if voice_started:
                print("🎤 Voice monitoring started...")
            else:
                print("⚠️ Voice monitoring failed to start")
        
        # Start interface
        self.text_interface()

def main():
    try:
        print("🚀 Initializing Enhanced JARVIS...")
        jarvis = EnhancedJARVIS()
        jarvis.run_system()
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        print("📋 Falling back to text-only mode would be recommended")
    finally:
        print("\n🔹 Enhanced JARVIS shutdown complete")
        print("Thank you for using Enhanced JARVIS!")

if __name__ == "__main__":
    main()