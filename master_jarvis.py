"""
JARVIS MASTER SYSTEM - AI INTELLIGENCE VERSION
==============================================
Professional AI Assistant with Enhanced Intelligence
"""

import os
import sys
import time
import random
import json
import threading
import traceback
import subprocess
import platform
import pickle  # ✅ FIXED: Added missing pickle import
from datetime import datetime
import webbrowser

# Voice and Speech Recognition
try:
    import pyttsx3
    # ✅ FIXED: Properly initialize TTS engine
    TTS_ENGINE = pyttsx3.init()
    
    # Configure voice settings
    voices = TTS_ENGINE.getProperty('voices')
    if voices:
        # Try to use a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                TTS_ENGINE.setProperty('voice', voice.id)
                break
        else:
            # Use first available voice
            TTS_ENGINE.setProperty('voice', voices[0].id)
    
    # Set speech properties
    TTS_ENGINE.setProperty('rate', 180)    # Speed of speech
    TTS_ENGINE.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    TTS_AVAILABLE = True
    print("✅ Text-to-Speech: Available")
except ImportError:
    TTS_ENGINE = None
    TTS_AVAILABLE = False
    print("❌ Text-to-Speech: Not available - install pyttsx3")
except Exception as e:
    TTS_ENGINE = None
    TTS_AVAILABLE = False
    print(f"❌ Text-to-Speech initialization error: {e}")

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
    print("✅ Speech Recognition: Available")
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("❌ Speech Recognition: Not available - install speechrecognition")

# AI Integration
try:
    import openai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class IntelligentJARVIS:
    def __init__(self):
        self.running = True
        self.systems_active = {}
        self.user_name = "Sir"
        self.debug_mode = False
        
        # Voice settings
        self.voice_enabled = True
        self.speech_rate = 180
        self.speech_volume = 0.9
        
        # AI Intelligence System
        self.ai_mode = True
        self.openai_api_key = "your_openai_api_key_here"
        self.conversation_history = []
        self.user_preferences = {}
        self.learning_data = {}
        
        # Memory system
        self.memory_file = "jarvis_memory.pkl"
        self.load_memory()
        
        # Speech Recognition Setup
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
        
        # Enhanced wake words
        self.wake_words = ["jarvis", "hey jarvis", "hello jarvis", "ok jarvis", "computer"]
        
        # Response collections
        self.responses = {
            'greetings': [
                "Good day, Sir! I'm operating at full capacity and ready to assist.",
                "Hello! All systems are operational. How may I help you today?",
                "Greetings, Sir. I'm here and ready for whatever you need.",
                "Good to see you! I'm functioning optimally and at your service."
            ],
            'how_are_you': [
                "I'm functioning optimally, Sir. All systems are running smoothly and I'm ready to assist.",
                "Excellent, Sir. My systems are performing at peak efficiency. How can I help you today?",
                "All systems operational and standing by, Sir. What can I do for you?",
                "Running perfectly, Sir. My processors are humming along nicely. What shall we work on?"
            ],
            'errors': [
                "I apologize, but I didn't catch that clearly, Sir.",
                "Could you please repeat that?",
                "I'm having trouble understanding. Please try again.",
                "Please speak a bit more clearly, Sir."
            ]
        }
        
        self.weather_api_key = "your_weather_api_key_here"

        # Load training data
        self.load_training_data()
    
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
            if self.debug_mode:
                print("💾 Memory saved")
        except Exception as e:
            if self.debug_mode:
                print(f"Memory save error: {e}")

    def configure_voice(self, rate=None, volume=None, voice_id=None):
        """Configure voice settings"""
        if not TTS_AVAILABLE or not TTS_ENGINE:  # ✅ FIXED: Added TTS_ENGINE check
            return False
        
        try:
            if rate:
                self.speech_rate = rate
                TTS_ENGINE.setProperty('rate', rate)
            
            if volume:
                self.speech_volume = volume
                TTS_ENGINE.setProperty('volume', volume)
            
            if voice_id:
                TTS_ENGINE.setProperty('voice', voice_id)
            
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Voice configuration error: {e}")
            return False

    def get_intelligent_response(self, user_input, context="general"):
        """Enhanced intelligent responses"""
        input_lower = user_input.lower()
        
        if context == "greeting" or any(word in input_lower for word in ['hello', 'hi', 'hey']):
            return random.choice(self.responses['greetings'])
            
        elif "how are you" in input_lower or "how's it going" in input_lower:
            return random.choice(self.responses['how_are_you'])
            
        elif "thank" in input_lower:
            return "You're very welcome, Sir. Always a pleasure to be of service."
            
        elif "joke" in input_lower or "funny" in input_lower:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything! Though I suppose that's rather fitting for my digital existence.",
                "I told my computer a joke about UDP, but I'm not sure it got it. Unlike TCP, there was no acknowledgment.",
                "There are only 10 types of people in this world: those who understand binary and those who don't.",
                "Why do programmers prefer dark mode? Because light attracts bugs!"
            ]
            return random.choice(jokes)
            
        elif "weather" in input_lower:
            return "I can check the weather for you, Sir. Which city would you like me to check?"
            
        elif "time" in input_lower:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}, Sir."
            
        elif "date" in input_lower:
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}, Sir."
            
        elif "?" in user_input:
            return "That's an interesting question, Sir. Let me think about that. Could you be more specific?"
            
        else:
            responses = [
                "I understand, Sir. How else may I assist you today?",
                "Noted, Sir. What would you like me to help you with?",
                "I hear you, Sir. Is there anything specific you'd like me to do?",
                "That's good to know, Sir. How can I assist you further?"
            ]
            return random.choice(responses)

    def initialize_system(self):
        """Enhanced system initialization with voice setup"""
        print("🚀 JARVIS Voice-Enabled System initializing...")
        
        # Check AI availability
        if AI_AVAILABLE and self.openai_api_key != "your_openai_api_key_here":
            print("🧠 AI Intelligence: ONLINE")
            self.systems_active['ai'] = True
        else:
            print("⚠️ AI Intelligence: OFFLINE (Enhanced fallback active)")
            self.systems_active['ai'] = False
        
        # Voice output system
        try:
            if TTS_AVAILABLE and TTS_ENGINE:  # ✅ FIXED: Added proper checks
                # Test voice output
                self.fast_speak("JARVIS Voice System operational. All voice functions ready, Sir.")
                self.systems_active['speech'] = True
                print("✅ Voice Output: ACTIVE")
            else:
                print("❌ Voice Output: UNAVAILABLE")
                print("💡 Install pyttsx3: pip install pyttsx3")
                self.systems_active['speech'] = False
        except Exception as e:
            print(f"❌ Voice output error: {e}")
            self.systems_active['speech'] = False
        
        # Voice input system
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                print("🎙️ Available microphones:")
                mic_list = sr.Microphone.list_microphone_names()
                for i, name in enumerate(mic_list):
                    print(f"  {i}: {name}")
                
                self.microphone = sr.Microphone()
                print("🎙️ Calibrating audio systems...")
                
                with self.microphone as source:
                    print("📊 Adjusting for ambient noise... Please be quiet for 3 seconds.")
                    self.recognizer.adjust_for_ambient_noise(source, duration=3)
                    print(f"🔊 Energy threshold set to: {self.recognizer.energy_threshold}")
                
                print("✅ Voice Input: ACTIVE")
                self.systems_active['microphone'] = True
                
                if self.systems_active['speech']:
                    self.fast_speak("Voice input and output systems fully operational, Sir.")
                
            except Exception as e:
                print(f"❌ Microphone initialization error: {e}")
                print("💡 Install pyaudio: pip install pyaudio")
                self.systems_active['microphone'] = False
        else:
            print("❌ Voice Input: UNAVAILABLE")
            print("💡 Install speechrecognition: pip install speechrecognition")
            self.systems_active['microphone'] = False
        
        return True

    def fast_speak(self, text):
        """Enhanced speech output with better error handling"""
        print(f"🤖 JARVIS: {text}")
        
        if not self.voice_enabled or not TTS_AVAILABLE or not TTS_ENGINE:  # ✅ FIXED: Added proper checks
            return
        
        def speak_async():
            try:
                if self.systems_active.get('speech'):
                    TTS_ENGINE.say(text)
                    TTS_ENGINE.runAndWait()
            except Exception as e:
                if self.debug_mode:
                    print(f"Speech error: {e}")
        
        # Run speech in separate thread to avoid blocking
        speech_thread = threading.Thread(target=speak_async, daemon=True)
        speech_thread.start()

    def listen_for_command(self, timeout=5, wake_word_mode=False):
        """Enhanced voice recognition"""
        if not self.systems_active.get('microphone'):
            return None
        
        try:
            with self.microphone as source:
                # Optimize microphone settings
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8
                
                if wake_word_mode:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=4)
                else:
                    print("🎙️ Listening for your command...")
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
            
            try:
                text = self.recognizer.recognize_google(audio, language='en-US').lower()
                if not wake_word_mode:
                    print(f"✅ Recognized: '{text}'")
                return text.strip()
                
            except sr.UnknownValueError:
                if not wake_word_mode:
                    print("❌ Could not understand audio")
                    self.fast_speak(random.choice(self.responses['errors']))
                return None
                
            except sr.RequestError as e:
                print(f"❌ Speech service error: {e}")
                if not wake_word_mode:
                    self.fast_speak("Speech recognition service is unavailable, Sir.")
                return None
                
        except sr.WaitTimeoutError:
            return "timeout"
        except Exception as e:
            print(f"❌ Audio error: {e}")
            return None

    def open_website(self, site):
        """Enhanced website opening"""
        sites = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'github': 'https://github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'reddit': 'https://reddit.com',
            'facebook': 'https://facebook.com',
            'twitter': 'https://twitter.com',
            'instagram': 'https://instagram.com',
            'chatgpt': 'https://chat.openai.com',
            'claude': 'https://claude.ai'
        }
        
        try:
            if site in sites:
                webbrowser.open(sites[site])
                return f"Opening {site.title()}, Sir."
            else:
                if '.' in site:
                    webbrowser.open(f"https://{site}")
                    return f"Opening {site}, Sir."
                else:
                    return f"I don't recognize {site}, Sir. Try being more specific."
        except Exception as e:
            if self.debug_mode:
                print(f"Browser error: {e}")
            return "Unable to open website, Sir."

    def open_application(self, app_name):
        """Enhanced application opening"""
        apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'vscode': 'code.exe'
        }
        
        try:
            if app_name in apps:
                subprocess.Popen([apps[app_name]])
                return f"Opening {app_name.title()}, Sir."
            else:
                subprocess.Popen([app_name])
                return f"Opening {app_name}, Sir."
        except Exception as e:
            if self.debug_mode:
                print(f"App error: {e}")
            return f"Unable to open {app_name}, Sir. Make sure it's installed."

    def search_web(self, query):
        """Enhanced web search"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching for '{query}', Sir. Opening results in your browser."
        except Exception as e:
            if self.debug_mode:
                print(f"Search error: {e}")
            return "Unable to perform web search, Sir."

    def process_command(self, command):
        """Enhanced command processing with voice support"""
        if not command:
            return False
        
        cmd = command.lower().strip()
        if self.debug_mode:
            print(f"📝 Processing: '{cmd}'")
        
        # System commands
        if any(word in cmd for word in ['exit', 'quit', 'goodbye', 'shutdown']):
            self.fast_speak("Goodbye, Sir. It was a pleasure serving you today.")
            self.save_memory()
            self.running = False
            return True
        
        # Voice control commands
        elif 'voice' in cmd and ('on' in cmd or 'enable' in cmd):
            self.voice_enabled = True
            self.fast_speak("Voice output enabled, Sir.")
            return True
        
        elif 'voice' in cmd and ('off' in cmd or 'disable' in cmd):
            self.fast_speak("Voice output disabled, Sir.")
            self.voice_enabled = False
            return True
        
        elif 'voice test' in cmd or 'test voice' in cmd:
            self.fast_speak("Voice test initiated. I can hear you clearly and speak clearly, Sir. All voice systems are operational.")
            return True
        
        # Debug toggle
        elif 'debug mode' in cmd:
            if 'on' in cmd or 'enable' in cmd:
                self.debug_mode = True
                self.fast_speak("Debug mode enabled, Sir.")
            elif 'off' in cmd or 'disable' in cmd:
                self.debug_mode = False
                self.fast_speak("Debug mode disabled, Sir.")
            else:
                status = "enabled" if self.debug_mode else "disabled"
                self.fast_speak(f"Debug mode is currently {status}, Sir.")
            return True
        
        # Quick commands
        elif cmd == 'time':
            current_time = datetime.now().strftime("%I:%M %p")
            self.fast_speak(f"The time is {current_time}, Sir.")
            return True
        
        elif cmd == 'date':
            today = datetime.now().strftime("%A, %B %d, %Y")
            self.fast_speak(f"Today is {today}, Sir.")
            return True
        
        # Web operations
        elif 'open' in cmd and any(site in cmd for site in ['youtube', 'google', 'github']):
            for site in ['youtube', 'google', 'github', 'facebook', 'twitter', 'instagram', 'reddit', 'chatgpt', 'claude']:
                if site in cmd:
                    result = self.open_website(site)
                    self.fast_speak(result)
                    return True
        
        elif 'search for' in cmd or 'search' in cmd:
            query = cmd.replace('search for', '').replace('search', '').strip()
            if query:
                result = self.search_web(query)
                self.fast_speak(result)
            else:
                self.fast_speak("What would you like me to search for, Sir?")
            return True
        
        # Application control
        elif 'open' in cmd and any(app in cmd for app in ['notepad', 'calculator', 'paint']):
            for app in ['notepad', 'calculator', 'paint', 'word', 'excel', 'chrome', 'firefox', 'vscode']:
                if app in cmd:
                    result = self.open_application(app)
                    self.fast_speak(result)
                    return True
        
        # System information
        elif 'system' in cmd and ('info' in cmd or 'information' in cmd):
            try:
                system = platform.system()
                version = platform.version()
                processor = platform.processor()
                info = f"System: {system} {version}, Processor: {processor}"
                self.fast_speak(info)
            except Exception as e:
                if self.debug_mode:
                    print(f"System info error: {e}")
                self.fast_speak("Unable to retrieve system information, Sir.")
            return True
        
        elif 'status' in cmd:
            online = sum(1 for status in self.systems_active.values() if status)
            total = len(self.systems_active)
            voice_status = "with full voice capability" if self.systems_active.get('speech') and self.systems_active.get('microphone') else "with limited voice features"
            self.fast_speak(f"System status: {online} of {total} systems operational {voice_status}, Sir.")
            return True
        
        # Memory commands
        elif 'remember' in cmd:
            info = cmd.replace('remember', '').strip()
            if info:
                self.user_preferences.setdefault('notes', []).append({
                    'content': info,
                    'timestamp': datetime.now().isoformat()
                })
                self.save_memory()
                self.fast_speak("I'll remember that, Sir.")
            else:
                self.fast_speak("What would you like me to remember, Sir?")
            return True
        
        elif 'what do you remember' in cmd or 'my notes' in cmd:
            notes = self.user_preferences.get('notes', [])
            if notes:
                recent_notes = notes[-3:]
                response = "Here's what I remember, Sir: " + "; ".join([note['content'] for note in recent_notes])
                self.fast_speak(response)
            else:
                self.fast_speak("I don't have any notes stored yet, Sir.")
            return True
        
        # Name learning
        elif "my name is" in cmd:
            try:
                name = cmd.split("my name is")[1].strip().split()[0].capitalize()
                self.user_name = name
                self.user_preferences['name'] = name
                self.save_memory()
                self.fast_speak(f"Pleasure to meet you, {name}. I'll remember that and address you properly from now on.")
                return True
            except:
                self.fast_speak("I didn't catch your name clearly, Sir. Could you repeat it?")
                return True
        
        # Help
        elif 'help' in cmd:
            help_text = "I can help with time, date, opening websites and applications, web searches, system information, remembering notes, and intelligent conversations, Sir."
            self.fast_speak(help_text)
            return True
        
        # Intelligent conversation mode
        else:
            context = "general"
            if any(word in cmd for word in ['hello', 'hi', 'hey']):
                context = "greeting"
            elif 'how are you' in cmd:
                context = "status"
            elif '?' in cmd:
                context = "question"
            
            response = self.get_intelligent_response(command, context)
            self.fast_speak(response)
            return True

    def voice_monitor(self):
        """Enhanced voice monitoring with better detection"""
        if not self.systems_active.get('microphone'):
            print("⚠️ Voice monitoring unavailable - microphone not initialized")
            return
        
        print("🎤 Voice monitoring active - Say 'JARVIS' to activate")
        print("🔊 Listening for wake words: " + ", ".join(self.wake_words))
        consecutive_timeouts = 0
        
        while self.running:
            try:
                result = self.listen_for_command(timeout=2, wake_word_mode=True)
                
                if result == "timeout":
                    consecutive_timeouts += 1
                    if consecutive_timeouts > 15:
                        print("🎤 Listening for 'JARVIS'...")
                        consecutive_timeouts = 0
                    time.sleep(0.2)
                    continue
                
                elif result and any(wake_word in result for wake_word in self.wake_words):
                    print(f"✅ Wake word detected: '{result}'")
                    
                    wake_responses = [
                        "Yes, Sir? How may I assist you?",
                        "At your service, Sir. What can I do for you?",
                        "I'm here, Sir. How can I help?",
                        "Ready to assist, Sir. What do you need?"
                    ]
                    self.fast_speak(random.choice(wake_responses))
                    
                    command = self.listen_for_command(timeout=10, wake_word_mode=False)
                    
                    if command and command != "timeout":
                        print(f"🔊 Command received: '{command}'")
                        self.process_command(command)
                    elif command == "timeout":
                        self.fast_speak("I'm ready when you are, Sir.")
                    else:
                        self.fast_speak("I didn't catch that, Sir. Please try again.")
                    
                    consecutive_timeouts = 0
                
                elif result:
                    if self.debug_mode:
                        print(f"🔍 Heard: '{result}' (not a wake word)")
            
            except Exception as e:
                print(f"❌ Voice monitoring error: {e}")
                time.sleep(1)

    def text_interface(self):
        """Enhanced text interface"""
        print("\n🧠 JARVIS AI INTELLIGENCE READY")
        print("🎤 Voice: Say 'JARVIS' then your command")
        print("⌨️ Text: Type anything for intelligent conversation")
        
        ai_status = "ONLINE" if self.systems_active.get('ai') else "ENHANCED FALLBACK"
        print(f"🧠 AI Mode: {ai_status}")
        print("💾 Memory: Learning from interactions")
        print("🔧 Commands: 'debug mode on/off', 'test voice', 'remember [info]'")
        
        if self.user_preferences.get('name'):
            name = self.user_preferences['name']
            print(f"👋 Welcome back, {name}!")
        
        online_systems = [name for name, status in self.systems_active.items() if status]
        print(f"⚡ Active Systems: {', '.join(online_systems) if online_systems else 'Text only'}")
        
        while self.running:
            try:
                command = input(f"\n🧠 {self.user_name}: ").strip()
                
                if command:
                    self.process_command(command)
            
            except KeyboardInterrupt:
                print("\n⏹️ Shutting down...")
                self.save_memory()
                self.fast_speak("Goodbye, Sir. Memory saved.")
                self.running = False
                break
            except Exception as e:
                if self.debug_mode:
                    print(f"Input error: {e}")
                continue

    def run_system(self):
        """Run the voice-enabled AI system"""
        print("=" * 70)
        print("🎤 JARVIS MASTER SYSTEM - VOICE ENABLED VERSION")
        print("=" * 70)
        
        try:
            success = self.initialize_system()
            if not success:
                print("❌ System initialization failed")
                return
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return
        
        # Start voice monitoring if available
        if self.systems_active.get('microphone'):
            try:
                voice_thread = threading.Thread(target=self.voice_monitor, daemon=True)
                voice_thread.start()
                print("✅ Voice: FULL DUPLEX ACTIVE (Input + Output)")
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Voice monitoring failed to start: {e}")
                print("⚠️ Voice: OUTPUT ONLY")
        else:
            if self.systems_active.get('speech'):
                print("⚠️ Voice: OUTPUT ONLY (Speech recognition unavailable)")
            else:
                print("⚠️ Voice: UNAVAILABLE (Text input only)")
        
        # Display comprehensive status
        ai_status = "ONLINE" if self.systems_active.get('ai') else "ENHANCED FALLBACK"
        print(f"🧠 AI Intelligence: {ai_status}")
        print("⚡ Features: Voice I/O, Smart conversations, Learning, Memory")
        print("🎯 Enhanced responses with full voice interaction")
        print("=" * 70)
        
        # Start main interface
        try:
            self.text_interface()
        except Exception as e:
            print(f"❌ System error: {e}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
        finally:
            print("💾 Saving memory...")
            self.save_memory()
            self.running = False

    def load_training_data(self):
        """Load training data from JSON file"""
        try:
            if os.path.exists('test_training_data.json'):
                with open('test_training_data.json', 'r') as f:
                    self.training_data = json.load(f)
                    print("✅ Training data loaded successfully")
            else:
                print("⚠️ Training data file not found - using defaults")
                self.training_data = {}
        except Exception as e:
            print(f"❌ Failed to load training data: {e}")
            self.training_data = {}

def main():
    """Main entry point"""
    try:
        print("🚀 Starting JARVIS Voice-Enabled AI System...")
        jarvis = IntelligentJARVIS()
        jarvis.run_system()
    except KeyboardInterrupt:
        print("\n⏹️ System interrupted by user")
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("💡 Please ensure all dependencies are installed:")
        print("   pip install speechrecognition pyttsx3 pyaudio")
    finally:
        print("🔹 Voice-Enabled AI System shutdown complete")

if __name__ == "__main__":
    main()    
    
    """Quick dependency installer for JARVIS"""
    
    import subprocess
    import sys
    
    def install_package(package):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
            return True
        except:
            print(f"❌ {package} failed")
            return False
    
    packages = ["speechrecognition", "pyttsx3", "pyaudio", "requests"]
    print("📦 Installing JARVIS dependencies...")
    
    for pkg in packages:
        install_package(pkg)
    
    print("🎤 JARVIS is ready!")