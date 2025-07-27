"""
Simple Voice JARVIS - Basic but reliable voice input
Uses speech_recognition library instead of direct audio handling
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

# Try speech_recognition (simpler and more reliable)
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
    print("💡 Try: pip install pyaudio")
    VOICE_INPUT_AVAILABLE = False

class SimpleVoiceJARVIS:
    def __init__(self):
        self.running = True
        self.user_name = "Sir"
        self.debug_mode = True
        self.voice_output_enabled = True
        self.voice_input_enabled = VOICE_INPUT_AVAILABLE
        self.listening_for_command = False
        
        # Wake words
        self.wake_words = [
            "jarvis", "hey jarvis", "hello jarvis", 
            "computer", "assistant"
        ]
        
        # Speech recognition settings
        if VOICE_INPUT_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Optimize settings
            self.recognizer.energy_threshold = 300
            self.recognizer.pause_threshold = 0.5
            self.recognizer.phrase_threshold = 0.3
        
        # Test voice output
        if TTS_AVAILABLE:
            try:
                TTS_ENGINE.say("Simple Voice JARVIS initializing")
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
                if self.debug_mode:
                    print("🎙️ Listening...")
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize speech using Google
            text = self.recognizer.recognize_google(audio).lower()
            
            if self.debug_mode:
                print(f"🔍 Heard: '{text}'")
            
            return text
            
        except sr.WaitTimeoutError:
            if self.debug_mode:
                print("🔇 Listening timeout")
            return None
        except sr.UnknownValueError:
            if self.debug_mode:
                print("🔇 Could not understand audio")
            return None
        except sr.RequestError as e:
            if self.debug_mode:
                print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Audio error: {e}")
            return None

    def listen_for_wake_word(self):
        """Listen for wake words continuously"""
        if not self.voice_input_enabled:
            print("⚠️ Voice input not available")
            return
        
        print("🎤 Listening for wake word... (say 'JARVIS')")
        consecutive_errors = 0
        
        while self.running and self.voice_input_enabled:
            try:
                # Listen for wake word with short timeout
                text = self.listen_for_speech(timeout=2, phrase_time_limit=3)
                
                if text:
                    consecutive_errors = 0  # Reset error count
                    
                    # Check for wake words
                    wake_word_found = False
                    for wake_word in self.wake_words:
                        if wake_word in text:
                            wake_word_found = True
                            print(f"✅ Wake word detected: '{wake_word}' in '{text}'")
                            
                            # Check if there's a command after the wake word
                            command_part = text.replace(wake_word, "").strip()
                            
                            if len(command_part) > 2:  # Direct command
                                print(f"🚀 Direct command: '{command_part}'")
                                self.speak("Right away, Sir.")
                                self.execute_command(command_part, command_part)
                            else:
                                # Just wake word - listen for command
                                self.listen_for_command()
                            
                            break
                    
                    if not wake_word_found and self.debug_mode:
                        print(f"🔍 No wake word in: '{text}'")
                
                else:
                    # Handle timeouts gracefully
                    time.sleep(0.1)
                
            except Exception as e:
                consecutive_errors += 1
                if self.debug_mode:
                    print(f"❌ Wake word error: {e}")
                
                if consecutive_errors > 10:
                    print("⚠️ Too many voice errors. Disabling voice input.")
                    self.voice_input_enabled = False
                    break
                
                time.sleep(1)

    def listen_for_command(self):
        """Listen for a command after wake word"""
        try:
            self.listening_for_command = True
            self.speak("Yes, Sir? I'm listening.")
            
            # Listen for command with longer timeout
            text = self.listen_for_speech(timeout=8, phrase_time_limit=7)
            
            if text:
                print(f"🚀 Command received: '{text}'")
                self.execute_command(text, text)
            else:
                self.speak("I didn't catch that, Sir. Please try again.")
            
            self.listening_for_command = False
            
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Command listening error: {e}")
            self.speak("I encountered an issue, Sir. Please use text commands.")
            self.listening_for_command = False

    def execute_command(self, cmd, original_command):
        """Execute commands"""
        
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
                self.speak("Voice input not available, Sir. Please install dependencies.")
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
        """Text interface with voice status"""
        print("\n" + "="*70)
        print("🚀 SIMPLE VOICE JARVIS")
        print("="*70)
        print("⌨️ Text Commands: Type your requests")
        print("🎤 Voice Output: Enabled" if self.voice_output_enabled else "🔇 Voice Output: Disabled")
        
        if self.voice_input_enabled:
            print("🎙️ Voice Input: Enabled - Say 'JARVIS' + command")
        else:
            print("⚠️ Voice Input: Disabled (type 'enable voice' to retry)")
        
        print("🛡️ Reliable Speech Recognition")
        print("")
        print("💡 Quick Commands:")
        print("   • time, date, youtube, google")
        print("   • search [query], hello, status, joke")
        print("   • enable voice, disable voice")
        print("   • help, exit")
        print("="*70)
        
        self.speak("Simple Voice JARVIS ready with reliable speech recognition, Sir.")
            
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
        """Start Simple Voice JARVIS"""
        print("="*70)
        print("🚀 SIMPLE VOICE JARVIS")
        print("🎤 Google Speech Recognition")
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
            print("💡 Install: pip install speechrecognition pyaudio")
        
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
        print("🚀 Initializing Simple Voice JARVIS...")
        jarvis = SimpleVoiceJARVIS()
        jarvis.run_system()
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        print("📋 Install dependencies: pip install speechrecognition pyaudio")
    finally:
        print("\n🔹 Simple Voice JARVIS shutdown complete")
        print("Thank you for using Simple Voice JARVIS!")

if __name__ == "__main__":
    main()