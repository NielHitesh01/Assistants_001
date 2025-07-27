"""
Fixed Voice JARVIS - Continuous listening that actually works
"""

import sys
import os
import time
import webbrowser
from datetime import datetime
import random
import threading

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

# Try speech_recognition
VOICE_INPUT_AVAILABLE = False
try:
    import speech_recognition as sr
    
    # Test microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Adjust for ambient noise
    print("🎙️ Calibrating microphone...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    
    print("✅ Speech Recognition: READY (Google)")
    VOICE_INPUT_AVAILABLE = True
    
except ImportError:
    print("❌ Install speech recognition: pip install speechrecognition pyaudio")
    VOICE_INPUT_AVAILABLE = False
except Exception as e:
    print(f"❌ Microphone setup failed: {e}")
    VOICE_INPUT_AVAILABLE = False

class FixedVoiceJARVIS:
    def __init__(self):
        self.running = True
        self.user_name = "Sir"
        self.debug_mode = True
        self.voice_output_enabled = True
        self.voice_input_enabled = VOICE_INPUT_AVAILABLE
        
        # **SIMPLIFIED WAKE WORDS - Just the main one**
        self.wake_words = ["jarvis"]
        
        # Speech recognition settings
        if VOICE_INPUT_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # **BETTER SETTINGS FOR WAKE WORD DETECTION**
            self.recognizer.energy_threshold = 4000  # Higher threshold
            self.recognizer.pause_threshold = 0.8    # Longer pause
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.dynamic_energy_threshold = True
        
        # Test voice output
        if TTS_AVAILABLE:
            try:
                TTS_ENGINE.say("Fixed Voice JARVIS initializing")
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

    def listen_for_speech(self, timeout=5, phrase_time_limit=None):
        """Listen for speech using speech_recognition"""
        if not self.voice_input_enabled:
            return None
        
        try:
            with self.microphone as source:
                print("🎙️ Listening...")
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize speech using Google
            text = self.recognizer.recognize_google(audio).lower()
            print(f"🔍 Heard: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("🔇 Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Audio error: {e}")
            return None

    def continuous_voice_loop(self):
        """COMPLETELY REWRITTEN - Simple and reliable wake word detection"""
        if not self.voice_input_enabled:
            print("⚠️ Voice input not available")
            return
        
        print("🎤 WAKE WORD DETECTION ACTIVE")
        print("💬 Say 'JARVIS' to activate, then give your command")
        print("💬 Or say 'JARVIS [command]' directly")
        
        while self.running and self.voice_input_enabled:
            try:
                # **STEP 1: Listen for speech**
                text = self.listen_for_speech(timeout=5, phrase_time_limit=8)
                
                if text:
                    # **STEP 2: Simple wake word check**
                    if "jarvis" in text:
                        print(f"✅ WAKE WORD DETECTED in: '{text}'")
                        
                        # **STEP 3: Remove 'jarvis' and get the command**
                        command = text.replace("jarvis", "").strip()
                        print(f"📝 Extracted command: '{command}'")
                        
                        if command:  # **Direct command**
                            print(f"🚀 Executing direct command: '{command}'")
                            self.speak("Right away, Sir.")
                            success = self.execute_command(command, command)
                            
                            if success:
                                print("✅ Command completed successfully")
                            else:
                                print("⚠️ Command had issues")
                                
                        else:  # **Just 'jarvis' - wait for command**
                            print("🎧 Wake word only - waiting for command...")
                            self.speak("Yes, Sir? What can I do for you?")
                            
                            # **Listen for the actual command**
                            command_text = self.listen_for_speech(timeout=10, phrase_time_limit=8)
                            
                            if command_text:
                                print(f"🚀 Executing follow-up: '{command_text}'")
                                success = self.execute_command(command_text, command_text)
                                
                                if success:
                                    print("✅ Follow-up completed successfully")
                                else:
                                    print("⚠️ Follow-up had issues")
                            else:
                                print("🔇 No follow-up command received")
                                self.speak("I'm ready when you are, Sir.")
                        
                        print("🔄 Returning to wake word detection...")
                        time.sleep(1)  # Brief pause before continuing
                        
                    else:
                        # **No wake word detected**
                        print(f"⏸️ No wake word in: '{text}' - continuing to listen...")
                
                # **Small delay to prevent CPU overload**
                time.sleep(0.2)
                
            except Exception as e:
                print(f"❌ Voice loop error: {e}")
                time.sleep(1)
                continue
        
        print("🔇 Voice monitoring stopped")

    def execute_command(self, cmd, original_command):
        """Execute commands with FIXED search handling"""
        try:
            cmd = cmd.lower().strip()
            print(f"🔧 DEBUG: Processing command: '{cmd}'")  # Debug line
            
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
            
            # **FIXED SEARCH LOGIC**
            elif any(word in cmd for word in ['search', 'look up', 'find', 'google search']):
                print(f"🔍 DEBUG: Search command detected in: '{cmd}'")
                
                # Better search term extraction
                query = cmd
                
                # Remove search-related words
                search_words = ['search for', 'search about', 'search', 'look up', 'find', 'google search', 'google']
                for word in search_words:
                    query = query.replace(word, '').strip()
                
                print(f"🔍 DEBUG: Extracted search query: '{query}'")
                
                if query and len(query) > 1:  # Make sure we have a real query
                    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    print(f"🔍 DEBUG: Opening URL: {search_url}")
                    webbrowser.open(search_url)
                    self.speak(f"Searching for {query}, Sir.")
                else:
                    print("🔍 DEBUG: No valid search query found")
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
                self.speak("All systems operational, Sir. Voice input active and ready to assist.")
                return True
            
            elif any(word in cmd for word in ['joke', 'tell joke', 'tell me joke', 'funny']):
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "I told my computer a joke about UDP, but I'm not sure it got it.",
                    "There are only 10 types of people: those who understand binary and those who don't.",
                    "Why do programmers prefer dark mode? Because light attracts bugs!",
                    "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
                ]
                self.speak(random.choice(jokes))
                return True
            
            elif any(phrase in cmd for phrase in ['disable voice', 'turn off voice', 'voice off']):
                self.voice_input_enabled = False
                self.speak("Voice input disabled, Sir. Text commands only.")
                return True
                
            elif any(phrase in cmd for phrase in ['enable voice', 'turn on voice', 'voice on']):
                if VOICE_INPUT_AVAILABLE:
                    self.voice_input_enabled = True
                    self.speak("Voice input enabled, Sir.")
                    return True
                else:
                    self.speak("Voice input not available, Sir.")
                    return True
            
            elif any(word in cmd for word in ['exit', 'quit', 'goodbye', 'bye', 'shutdown']):
                self.speak("Goodbye, Sir. It was a pleasure serving you today.")
                self.running = False
                return True
            
            elif 'help' in cmd:
                help_text = """Available commands, Sir:
                - Time, Date, YouTube, Google
                - Search for [anything]
                - Hello, Status, Joke
                - Voice on/off, Help, Exit"""
                self.speak("Here are my available commands, Sir.")
                print(help_text)
                return True
            
            else:
                print(f"🔍 DEBUG: No command matched for: '{cmd}'")
                responses = [
                    "I understand, Sir. How else may I assist?",
                    "Noted, Sir. What else can I help with?",
                    "I hear you, Sir. Anything else?",
                    "Processing that, Sir. What's next?"
                ]
                self.speak(random.choice(responses))
                return True
                
        except Exception as e:
            print(f"❌ Error in execute_command: {e}")
            self.speak("I encountered an error, Sir. Please try again.")
            return False

    def continuous_voice_loop(self):
        """IMPROVED wake word detection with better debugging"""
        if not self.voice_input_enabled:
            print("⚠️ Voice input not available")
            return
        
        print("🎤 WAKE WORD DETECTION ACTIVE")
        print("💬 Try saying: 'JARVIS search artificial intelligence'")
        print("💬 Or: 'JARVIS what time is it'")
        print("💬 Or: 'JARVIS' then wait and say 'tell me a joke'")
        
        while self.running and self.voice_input_enabled:
            try:
                # Listen for speech
                text = self.listen_for_speech(timeout=5, phrase_time_limit=10)
                
                if text:
                    print(f"🎧 RAW INPUT: '{text}'")  # Show exactly what was heard
                    
                    # Check for wake word (case insensitive)
                    if "jarvis" in text.lower():
                        print(f"✅ WAKE WORD DETECTED!")
                        
                        # Remove 'jarvis' and get the command
                        command = text.lower().replace("jarvis", "").strip()
                        print(f"📝 EXTRACTED COMMAND: '{command}'")
                        
                        if command and len(command) > 1:  # Direct command
                            print(f"🚀 EXECUTING DIRECT COMMAND: '{command}'")
                            self.speak("Right away, Sir.")
                            success = self.execute_command(command, command)
                            
                            if success:
                                print("✅ Command completed successfully")
                            else:
                                print("⚠️ Command had issues")
                                
                        else:  # Just 'jarvis' - wait for command
                            print("🎧 WAKE WORD ONLY - WAITING FOR COMMAND...")
                            self.speak("Yes, Sir? What can I do for you?")
                            
                            # Listen for the actual command
                            command_text = self.listen_for_speech(timeout=10, phrase_time_limit=10)
                            
                            if command_text:
                                print(f"🚀 EXECUTING FOLLOW-UP: '{command_text}'")
                                success = self.execute_command(command_text, command_text)
                                
                                if success:
                                    print("✅ Follow-up completed successfully")
                                else:
                                    print("⚠️ Follow-up had issues")
                            else:
                                print("🔇 No follow-up command received")
                                self.speak("I'm ready when you are, Sir.")
                        
                        print("🔄 RETURNING TO WAKE WORD DETECTION...")
                        time.sleep(1)
                        
                    else:
                        # No wake word detected
                        print(f"⏸️ NO WAKE WORD in: '{text}' - continuing...")
                
                # Small delay to prevent CPU overload
                time.sleep(0.2)
                
            except Exception as e:
                print(f"❌ Voice loop error: {e}")
                time.sleep(1)
                continue
        
        print("🔇 Voice monitoring stopped")

    def execute_command(self, cmd, original_command):
        """Execute commands with FIXED search handling"""
        try:
            cmd = cmd.lower().strip()
            print(f"🔧 DEBUG: Processing command: '{cmd}'")  # Debug line
            
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
            
            # **FIXED SEARCH LOGIC**
            elif any(word in cmd for word in ['search', 'look up', 'find', 'google search']):
                print(f"🔍 DEBUG: Search command detected in: '{cmd}'")
                
                # Better search term extraction
                query = cmd
                
                # Remove search-related words
                search_words = ['search for', 'search about', 'search', 'look up', 'find', 'google search', 'google']
                for word in search_words:
                    query = query.replace(word, '').strip()
                
                print(f"🔍 DEBUG: Extracted search query: '{query}'")
                
                if query and len(query) > 1:  # Make sure we have a real query
                    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    print(f"🔍 DEBUG: Opening URL: {search_url}")
                    webbrowser.open(search_url)
                    self.speak(f"Searching for {query}, Sir.")
                else:
                    print("🔍 DEBUG: No valid search query found")
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
                self.speak("All systems operational, Sir. Voice input active and ready to assist.")
                return True
            
            elif any(word in cmd for word in ['joke', 'tell joke', 'tell me joke', 'funny']):
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "I told my computer a joke about UDP, but I'm not sure it got it.",
                    "There are only 10 types of people: those who understand binary and those who don't.",
                    "Why do programmers prefer dark mode? Because light attracts bugs!",
                    "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
                ]
                self.speak(random.choice(jokes))
                return True
            
            elif any(phrase in cmd for phrase in ['disable voice', 'turn off voice', 'voice off']):
                self.voice_input_enabled = False
                self.speak("Voice input disabled, Sir. Text commands only.")
                return True
                
            elif any(phrase in cmd for phrase in ['enable voice', 'turn on voice', 'voice on']):
                if VOICE_INPUT_AVAILABLE:
                    self.voice_input_enabled = True
                    self.speak("Voice input enabled, Sir.")
                    return True
                else:
                    self.speak("Voice input not available, Sir.")
                    return True
            
            elif any(word in cmd for word in ['exit', 'quit', 'goodbye', 'bye', 'shutdown']):
                self.speak("Goodbye, Sir. It was a pleasure serving you today.")
                self.running = False
                return True
            
            elif 'help' in cmd:
                help_text = """Available commands, Sir:
                - Time, Date, YouTube, Google
                - Search for [anything]
                - Hello, Status, Joke
                - Voice on/off, Help, Exit"""
                self.speak("Here are my available commands, Sir.")
                print(help_text)
                return True
            
            else:
                print(f"🔍 DEBUG: No command matched for: '{cmd}'")
                responses = [
                    "I understand, Sir. How else may I assist?",
                    "Noted, Sir. What else can I help with?",
                    "I hear you, Sir. Anything else?",
                    "Processing that, Sir. What's next?"
                ]
                self.speak(random.choice(responses))
                return True
                
        except Exception as e:
            print(f"❌ Error in execute_command: {e}")
            self.speak("I encountered an error, Sir. Please try again.")
            return False

    def start_voice_monitoring(self):
        """Start voice monitoring in background thread"""
        if self.voice_input_enabled and VOICE_INPUT_AVAILABLE:
            self.voice_thread = threading.Thread(target=self.continuous_voice_loop, daemon=True)
            self.voice_thread.start()
            print("✅ Voice monitoring thread started")
            return True
        return False

    def text_interface(self):
        """Text interface"""
        print("\n" + "="*70)
        print("🚀 FIXED VOICE JARVIS - WAKE WORD DETECTION")
        print("="*70)
        print("⌨️ Text Commands: Type your requests")
        print("🎤 Voice Output: Enabled" if self.voice_output_enabled else "🔇 Voice Output: Disabled")
        
        if self.voice_input_enabled:
            print("🎙️ Voice Input: Say 'JARVIS' to activate")
        else:
            print("⚠️ Voice Input: Disabled")
        
        print("")
        print("🎤 Voice Examples:")
        print("   • 'JARVIS what time is it'")
        print("   • 'JARVIS' → 'tell me a joke'")
        print("   • 'JARVIS open YouTube'")
        print("")
        print("⌨️ Text Commands:")
        print("   • time, date, youtube, google")
        print("   • search [query], hello, status, joke")
        print("   • voice on/off, help, exit")
        print("="*70)
        
        self.speak("Fixed Voice JARVIS ready. Say JARVIS to activate voice commands, Sir.")
            
        while self.running:
            try:
                command = input(f"\n🧠 {self.user_name}: ").strip()
                if command:
                    print(f"📝 Processing: '{command}'")
                    self.execute_command(command.lower(), command)
                else:
                    print("💭 Waiting for your command, Sir...")
                    
            except KeyboardInterrupt:
                print("\n⏹️ Shutting down...")
                self.speak("Goodbye, Sir.")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue

    def run_system(self):
        """Start Fixed Voice JARVIS"""
        print("="*70)
        print("🚀 FIXED VOICE JARVIS v2.1")
        print("🎤 Wake Word Detection System")
        print("="*70)
        
        # System status
        print("🔍 System Status:")
        if TTS_AVAILABLE:
            print("✅ Speech Output: ONLINE")
        else:
            print("❌ Speech Output: OFFLINE")
        
        if VOICE_INPUT_AVAILABLE:
            print("✅ Voice Input: ONLINE (Google Speech)")
        else:
            print("❌ Voice Input: OFFLINE")
        
        print("✅ Text Interface: ONLINE") 
        print("✅ Web Browser: ONLINE")
        print("✅ Command Processing: ONLINE")
        
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
        print("🚀 Initializing Fixed Voice JARVIS v2.1...")
        jarvis = FixedVoiceJARVIS()
        jarvis.run_system()
    except Exception as e:
        print(f"❌ Critical Error: {e}")
    finally:
        print("\n🔹 Fixed Voice JARVIS shutdown complete")
        print("Thank you for using Fixed Voice JARVIS!")

if __name__ == "__main__":
    main()