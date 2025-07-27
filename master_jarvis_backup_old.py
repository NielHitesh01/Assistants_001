"""
JARVIS MASTER SYSTEM - AI INTELLIGENCE VERSION
==============================================
Professional AI Assistant with Enhanced Intelligence
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

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    print("❌ Installing speech_recognition: pip install speechrecognition")
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import openai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class IntelligentJARVIS:
    def __init__(self):
        """Initialize JARVIS with all required attributes"""
        self.running = True
        self.systems_active = {}
        self.user_name = "Sir"
        self.debug_mode = False
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
                TTS_ENGINE.say("Voice output test successful")
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

    def get_intelligent_response(self, user_input, context="general"):
        """Enhanced intelligent responses"""
        input_lower = user_input.lower()
        
        # Specific response patterns
        if context == "greeting" or any(word in input_lower for word in ['hello', 'hi', 'hey']):
            return random.choice(self.responses['greetings'])
            
        elif "how are you" in input_lower:
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

    def fast_speak(self, text):
        """Optimized speech output"""
        print(f"🤖 JARVIS: {text}")
        
        if self.voice_output_enabled and TTS_AVAILABLE and TTS_ENGINE:
            try:
                TTS_ENGINE.say(text)
                TTS_ENGINE.runAndWait()
                
                if self.debug_mode:
                    print("🔊 Voice output completed")
                    
            except Exception as e:
                if self.debug_mode:
                    print(f"🔊 Voice error: {e}")
                
                # Quick recovery attempt
                try:
                    time.sleep(0.1)
                    TTS_ENGINE.say(text)
                    TTS_ENGINE.runAndWait()
                except:
                    if self.debug_mode:
                        print("🔊 Voice recovery failed")
        else:
            # Debug why voice isn't working
            if not self.voice_output_enabled:
                print("🔇 Voice output is disabled")
            elif not TTS_AVAILABLE:
                print("🔇 TTS engine not available")
            elif not TTS_ENGINE:
                print("🔇 TTS engine not initialized")

    def initialize_system(self):
        """Single, clean system initialization"""
        print("🚀 JARVIS AI Intelligence System initializing...")
        
        # Check AI availability
        if AI_AVAILABLE and self.openai_api_key != "your_openai_api_key_here":
            print("🧠 AI Intelligence: ONLINE")
            self.systems_active['ai'] = True
        else:
            print("⚠️ AI Intelligence: OFFLINE (Enhanced fallback active)")
            self.systems_active['ai'] = False
    
        # Speech system setup
        try:
            if TTS_AVAILABLE and TTS_ENGINE:
                print("🔊 Text-to-Speech: ONLINE")
                
                # Test voice output
                print("🔊 Testing voice output...")
                TTS_ENGINE.say("JARVIS Intelligence System operational. Voice output active and ready, Sir.")
                TTS_ENGINE.runAndWait()
                print("✅ Voice output confirmed working")
                
                self.systems_active['speech'] = True
            else:
                print("❌ Text-to-Speech: OFFLINE")
                self.systems_active['speech'] = False
        except Exception as e:
            print(f"❌ Speech error: {e}")
            self.systems_active['speech'] = False
    
        # Microphone setup
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                print("🎙️ Available microphones:")
                for i, name in enumerate(sr.Microphone.list_microphone_names()[:5]):  # Limit output
                    print(f"  {i}: {name}")
            
                self.microphone = sr.Microphone()
                print("🎙️ Calibrating audio systems...")
            
                with self.microphone as source:
                    print("📊 Adjusting for ambient noise... Please be quiet.")
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                    
                    # Set reasonable threshold
                    threshold = self.recognizer.energy_threshold
                    if threshold > 1000:
                        self.recognizer.energy_threshold = 500
                    elif threshold < 200:
                        self.recognizer.energy_threshold = 300
                    
                    print(f"🔊 Energy threshold set to: {self.recognizer.energy_threshold}")
                
                print("✅ Audio systems calibrated")
                self.systems_active['microphone'] = True
                
                # Test microphone
                self.fast_speak("Testing microphone. Can you hear me clearly?")
            
            except Exception as e:
                print(f"❌ Microphone error: {e}")
                self.systems_active['microphone'] = False
        else:
            print("❌ Speech recognition not available")
            self.systems_active['microphone'] = False
    
        return True

    def voice_monitor(self):
        """Clean voice monitoring system"""
        if not self.systems_active.get('microphone'):
            print("⚠️ Voice monitoring unavailable")
            return
        
        print("🎤 Voice monitoring active - Say 'JARVIS' to activate")
        
        while self.running:
            try:
                result = self.listen_for_command(timeout=2, wake_word_mode=True)
                
                if result == "timeout":
                    time.sleep(0.1)
                    continue
                    
                elif result and any(wake_word in result for wake_word in self.wake_words):
                    print(f"✅ Wake word detected: '{result}'")
                    
                    # Check for complete command
                    command_part = result
                    for wake_word in self.wake_words:
                        if wake_word in command_part:
                            command_part = command_part.replace(wake_word, "").strip()
                            break
                    
                    if command_part and len(command_part.split()) >= 2:
                        # Direct command
                        print(f"🔊 Direct command: '{command_part}'")
                        self.fast_speak("Right away, Sir.")
                        self._execute_command(command_part.lower(), command_part)
                    else:
                        # Just wake word
                        self.fast_speak("Yes, Sir?")
                        
                        command = self.listen_for_command(timeout=5, wake_word_mode=False)
                        
                        if command and command != "timeout":
                            print(f"🔊 Command: '{command}'")
                            self._execute_command(command.lower(), command)
                        elif command == "timeout":
                            self.fast_speak("Ready when you are, Sir.")
                    
                    time.sleep(0.2)
                    continue
                
            except Exception as e:
                if self.debug_mode:
                    print(f"Voice error: {e}")
                time.sleep(0.3)

    def listen_for_command(self, timeout=5, wake_word_mode=False):
        """Clean voice recognition"""
        if not self.systems_active.get('microphone'):
            return None
            
        try:
            with self.microphone as source:
                self.recognizer.energy_threshold = 300
                self.recognizer.pause_threshold = 0.6
                self.recognizer.dynamic_energy_threshold = True
                
                if wake_word_mode:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
                else:
                    print("🎙️ Listening for your command...")
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=6)
            
            try:
                text = self.recognizer.recognize_google(audio, language='en-US').lower()
                if not wake_word_mode:
                    print(f"✅ Recognized: '{text}'")
                return text.strip()
                
            except sr.UnknownValueError:
                if not wake_word_mode:
                    print("❌ Could not understand audio")
                    self.fast_speak("I didn't catch that clearly, Sir. Please try again.")
                return None
                
            except sr.RequestError as e:
                if self.debug_mode:
                    print(f"❌ Speech service error: {e}")
                return None
                
        except sr.WaitTimeoutError:
            return "timeout"
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Audio error: {e}")
            return None

    def _execute_command(self, cmd, original_command):
        """Clean command execution"""
        
        # Voice control
        if 'voice test' in cmd or 'test voice' in cmd:
            self.fast_speak("Voice test successful. All voice systems operational, Sir.")
            return True

        # System commands
        elif any(word in cmd for word in ['exit', 'quit', 'goodbye', 'shutdown']):
            self.fast_speak("Goodbye, Sir. It was a pleasure serving you today.")
            self.save_memory()
            self.running = False
            return True
        
        # Quick commands
        elif 'time' in cmd:
            current_time = datetime.now().strftime("%I:%M %p")
            self.fast_speak(f"The time is {current_time}, Sir.")
            return True
            
        elif 'date' in cmd:
            today = datetime.now().strftime("%A, %B %d, %Y")
            self.fast_speak(f"Today is {today}, Sir.")
            return True
        
        # Web operations
        elif 'open youtube' in cmd:
            webbrowser.open('https://youtube.com')
            self.fast_speak("Opening YouTube, Sir.")
            return True
            
        elif 'open google' in cmd:
            webbrowser.open('https://google.com')
            self.fast_speak("Opening Google, Sir.")
            return True
            
        elif 'open' in cmd:
            sites = ['youtube', 'google', 'github', 'reddit', 'facebook']
            for site in sites:
                if site in cmd:
                    webbrowser.open(f'https://{site}.com')
                    self.fast_speak(f"Opening {site.title()}, Sir.")
                    return True
            self.fast_speak("What should I open, Sir?")
            return True
        
        elif 'search' in cmd:
            query = cmd.replace('search for', '').replace('search', '').strip()
            if query:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                self.fast_speak(f"Searching for {query}, Sir.")
            else:
                self.fast_speak("What should I search for, Sir?")
            return True
        
        # Help
        elif 'help' in cmd:
            self.fast_speak("I can help with time, websites, searches, and conversations, Sir.")
            return True
        
        # Conversation
        elif any(word in cmd for word in ['hello', 'hi', 'hey']):
            self.fast_speak("Hello, Sir! How can I help?")
            return True
            
        elif 'how are you' in cmd:
            self.fast_speak("All systems operational, Sir.")
            return True
        
        # Default intelligent response
        else:
            response = self.get_intelligent_response(original_command)
            self.fast_speak(response)
            return True

    def text_interface(self):
        """Clean text interface"""
        print("\n🧠 JARVIS READY - OPTIMIZED MODE")
        print("🎤 Voice: Say 'JARVIS' + command")
        print("⌨️ Text: Type commands")
        print("⚡ Response time optimized")
        print("🎯 Try: 'JARVIS what time is it' or 'JARVIS open youtube'")
        
        self.fast_speak("JARVIS ready. Voice monitoring is active, Sir.")
            
        while self.running:
            try:
                command = input(f"\n🧠 {self.user_name}: ").strip()
                if command:
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
        """Clean system startup"""
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
        
        # Display status
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
        print("🔹 Voice-Enabled AI System shutdown complete")

if __name__ == "__main__":
    main()