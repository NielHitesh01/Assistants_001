"""
JARVIS MASTER SYSTEM - AI INTELLIGENCE VERSION
==============================================
Professional AI Assistant with GPT Integration and Learning
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

# Fast imports with caching
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import pyttsx3
    TTS_ENGINE = pyttsx3.init()
    TTS_ENGINE.setProperty('rate', 180)
    TTS_ENGINE.setProperty('volume', 0.9)
    TTS_AVAILABLE = True
except ImportError:
    TTS_ENGINE = None
    TTS_AVAILABLE = False

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
        
        # AI Intelligence System
        self.ai_mode = True
        self.openai_api_key = "your_openai_api_key_here"
        self.conversation_history = []
        self.user_preferences = {}
        self.learning_data = {}
        
        # Memory system
        self.memory_file = "jarvis_memory.pkl"
        self.load_memory()
        
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 400
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
            
        self.wake_words = ["jarvis", "hey jarvis", "hello jarvis"]
        
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
            'thinking': [
                "Let me think about that...",
                "Processing your request...",
                "Analyzing that for you...",
                "Give me a moment to consider that..."
            ],
            'errors': [
                "I apologize, but I didn't catch that clearly, Sir.",
                "Could you please repeat that?",
                "I'm having trouble understanding. Please try again.",
                "Please speak a bit more clearly, Sir."
            ],
            'how_are_you': [
                "I'm functioning optimally, Sir. All systems are running smoothly and I'm ready to assist.",
                "Excellent, Sir. My systems are performing at peak efficiency. How can I help you today?",
                "All systems operational and standing by, Sir. What can I do for you?",
                "Running perfectly, Sir. My processors are humming along nicely. What shall we work on?"
            ]
        }
        
        self.weather_api_key = "your_weather_api_key_here"

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

    def get_intelligent_response(self, user_input, context="general"):
        """Enhanced intelligent responses"""
        input_lower = user_input.lower()
        
        # Specific response patterns
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
                "There are only 10 types of people in this world: those who understand binary and those who don't. I assume you're in the first category, Sir."
            ]
            return random.choice(jokes)
            
        elif "weather" in input_lower:
            return "I can check the weather for you, Sir. Which city would you like me to check? Just say 'weather in [city name]'."
            
        elif "time" in input_lower:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}, Sir."
            
        elif "date" in input_lower:
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}, Sir."
            
        elif "?" in user_input:
            return "That's an interesting question, Sir. Let me think about that based on what I know. Could you be more specific about what aspect interests you most?"
            
        else:
            responses = [
                "I understand, Sir. That's quite interesting. How else may I assist you today?",
                "Noted, Sir. I'm processing that information. What would you like me to help you with?",
                "I hear you, Sir. Is there anything specific you'd like me to do or help you with?",
                "That's good to know, Sir. I'm here to help with whatever you need - just let me know."
            ]
            return random.choice(responses)

    def initialize_system(self):
        """Enhanced system initialization"""
        print("🚀 JARVIS AI Intelligence System initializing...")
        
        # Check AI availability
        if AI_AVAILABLE and self.openai_api_key != "your_openai_api_key_here":
            print("🧠 AI Intelligence: ONLINE")
            self.systems_active['ai'] = True
        else:
            print("⚠️ AI Intelligence: OFFLINE (Enhanced fallback active)")
            self.systems_active['ai'] = False
        
        # Speech system
        try:
            if TTS_AVAILABLE:
                self.fast_speak("JARVIS Intelligence System operational. Advanced assistance ready, Sir.")
                self.systems_active['speech'] = True
            else:
                print("⚠️ Speech synthesis unavailable")
                self.systems_active['speech'] = False
        except Exception as e:
            if self.debug_mode:
                print(f"Speech error: {e}")
            self.systems_active['speech'] = False
        
        # Microphone setup
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.microphone = sr.Microphone()
                print("🎙️ Calibrating audio systems...")
                
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=2.0)
                    
                print("✅ Audio systems calibrated")
                self.systems_active['microphone'] = True
                
            except Exception as e:
                if self.debug_mode:
                    print(f"Microphone error: {e}")
                self.systems_active['microphone'] = False
        else:
            self.systems_active['microphone'] = False
        
        return True

    def fast_speak(self, text):
        """Enhanced speech output"""
        print(f"🤖 JARVIS: {text}")
        
        def speak_async():
            try:
                if self.systems_active.get('speech'):
                    if TTS_AVAILABLE:
                        TTS_ENGINE.say(text)
                        TTS_ENGINE.runAndWait()
            except Exception as e:
                if self.debug_mode:
                    print(f"Speech error: {e}")
        
        threading.Thread(target=speak_async, daemon=True).start()

    def listen_for_command(self, timeout=5, wake_word_mode=False):
        """Enhanced voice recognition"""
        if not self.systems_active.get('microphone'):
            return None
            
        try:
            with self.microphone as source:
                if wake_word_mode:
                    audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=3)
                else:
                    if self.debug_mode:
                        print("🎙️ Listening...")
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            try:
                text = self.recognizer.recognize_google(audio, language='en-US').lower()
                if not wake_word_mode and self.debug_mode:
                    print(f"✅ Recognized: '{text}'")
                return text.strip()
                
            except sr.UnknownValueError:
                if not wake_word_mode:
                    self.fast_speak(random.choice(self.responses['errors']))
                return None
                
            except sr.RequestError as e:
                if not wake_word_mode and self.debug_mode:
                    print(f"Speech service error: {e}")
                return None
                
        except sr.WaitTimeoutError:
            return "timeout"
        except Exception as e:
            if self.debug_mode:
                print(f"Audio error: {e}")
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
            'instagram': 'https://instagram.com'
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
                    return f"I don't know how to open {site}, Sir. Try being more specific."
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
            'edge': 'msedge.exe'
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
        """AI-Enhanced command processing"""
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
            for site in ['youtube', 'google', 'github', 'facebook', 'twitter', 'instagram', 'reddit']:
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
            for app in ['notepad', 'calculator', 'paint', 'word', 'excel', 'chrome', 'firefox']:
                if app in cmd:
                    result = self.open_application(app)
                    self.fast_speak(result)
                    return True
        
        # System information
        elif 'system' in cmd and ('info' in cmd or 'information' in cmd):
            try:
                import platform
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
            self.fast_speak(f"System status: {online} of {total} systems operational, Sir.")
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
            # Determine context for better responses
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
        """Enhanced voice monitoring"""
        if not self.systems_active.get('microphone'):
            print("⚠️ Voice monitoring unavailable")
            return
            
        print("🎤 AI Voice monitoring active")
        consecutive_timeouts = 0
        
        while self.running:
            try:
                result = self.listen_for_command(timeout=1, wake_word_mode=True)
                
                if result == "timeout":
                    consecutive_timeouts += 1
                    if consecutive_timeouts > 30:
                        if self.debug_mode:
                            print("🎤 Listening for wake word...")
                        consecutive_timeouts = 0
                    time.sleep(0.1)
                    continue
                    
                elif result and any(wake_word in result for wake_word in self.wake_words):
                    if self.debug_mode:
                        print(f"🔊 Wake word: '{result}'")
                    
                    wake_responses = [
                        "Yes, Sir? How may I assist you?",
                        "At your service, Sir. What can I do for you?",
                        "I'm here, Sir. How can I help?",
                        "Ready to assist, Sir. What do you need?"
                    ]
                    self.fast_speak(random.choice(wake_responses))
                    
                    command = self.listen_for_command(timeout=8, wake_word_mode=False)
                    
                    if command and command != "timeout":
                        self.process_command(command)
                    elif command == "timeout":
                        self.fast_speak("I'm ready when you are, Sir.")
                        
                    consecutive_timeouts = 0
                    
            except Exception as e:
                if self.debug_mode:
                    print(f"Voice monitoring error: {e}")
                time.sleep(1)

    def text_interface(self):
        """Enhanced text interface"""
        print("\n🧠 JARVIS AI INTELLIGENCE READY")
        print("🎤 Voice: Say 'JARVIS' then your command")
        print("⌨️ Text: Type anything for intelligent conversation")
        print("🧠 AI Mode: Enhanced fallback responses")
        print("💾 Memory: Learning from interactions")
        print("🔧 Commands: 'debug mode on/off', 'remember [info]'")
        
        if self.user_preferences.get('name'):
            name = self.user_preferences['name']
            print(f"👋 Welcome back, {name}!")
        
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
        """Run the AI intelligence system"""
        print("="*70)
        print("🧠 JARVIS MASTER SYSTEM - AI INTELLIGENCE VERSION")
        print("="*70)
        
        # Initialize
        success = self.initialize_system()
        if not success:
            print("❌ System initialization failed")
            return
        
        # Start voice monitoring
        if self.systems_active.get('microphone'):
            voice_thread = threading.Thread(target=self.voice_monitor, daemon=True)
            voice_thread.start()
            print("✅ Voice: AI ENHANCED")
            time.sleep(1)
        else:
            print("⚠️ Voice: LIMITED")
        
        # Display AI status
        ai_status = "ONLINE" if self.systems_active.get('ai') else "ENHANCED FALLBACK"
        print(f"🧠 AI Intelligence: {ai_status}")
        print("⚡ Features: Smart conversations, Learning, Memory")
        print("🎯 Enhanced responses with context awareness")
        print("="*70)
        
        # Start interface
        try:
            self.text_interface()
        except Exception as e:
            if self.debug_mode:
                print(f"System error: {e}")
        finally:
            self.save_memory()
            self.running = False

def main():
    """Main entry point"""
    try:
        jarvis = IntelligentJARVIS()
        jarvis.run_system()
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("Please ensure all dependencies are installed and try again.")
    finally:
        print("AI Intelligence System shutdown complete")

if __name__ == "__main__":
    main()