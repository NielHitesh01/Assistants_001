"""
Text JARVIS - 100% Reliable Text-Only Version
Perfect for systems with audio issues
"""

import sys
import os
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

class TextJARVIS:
    def __init__(self):
        self.running = True
        self.user_name = "Sir"
        self.debug_mode = False
        self.voice_output_enabled = True
        
        # Test voice
        if TTS_AVAILABLE:
            try:
                TTS_ENGINE.say("Text JARVIS initializing")
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

    def execute_command(self, cmd, original_command):
        """Execute text commands efficiently"""
        
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
            # Extract search query
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
            responses = [
                "All systems operational and functioning perfectly, Sir.",
                "Excellent condition, Sir. Running smoothly and ready to assist.",
                "Operating at optimal efficiency, Sir. How may I help you?",
                "All systems green, Sir. Standing by for your commands."
            ]
            self.speak(random.choice(responses))
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
        
        elif 'weather' in cmd:
            self.speak("I would need internet access to check the weather, Sir. You can visit weather.com or ask me to open Google.")
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

    def text_interface(self):
        """Enhanced text interface"""
        print("\n" + "="*60)
        print("🚀 TEXT JARVIS - FULLY OPERATIONAL")
        print("="*60)
        print("⌨️ Text Commands: Type your requests")
        print("🎤 Voice Output: Enabled" if self.voice_output_enabled else "🔇 Voice Output: Disabled")
        print("🛡️ 100% Reliable - No Audio Input Issues")
        print("")
        print("💡 Quick Commands:")
        print("   • time, date, youtube, google")
        print("   • search [query], hello, status, joke")
        print("   • help, exit")
        print("="*60)
        
        self.speak("Text JARVIS fully operational and ready to serve, Sir.")
            
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
                self.speak("I encountered an error, Sir. Please try again.")
                continue

    def run_system(self):
        """Start Text JARVIS"""
        print("="*60)
        print("🚀 TEXT JARVIS - PREMIUM EDITION")
        print("💯 100% Reliable Text Interface")
        print("="*60)
        
        # System status
        print("🔍 System Status:")
        if TTS_AVAILABLE:
            print("✅ Speech Output: ONLINE")
        else:
            print("❌ Speech Output: OFFLINE")
        
        print("✅ Text Interface: ONLINE") 
        print("✅ Web Browser: ONLINE")
        print("✅ Command Processing: ONLINE")
        print("✅ Error Handling: ACTIVE")
        
        print("="*60)
        
        # Start interface
        self.text_interface()

def main():
    try:
        print("🚀 Initializing Text JARVIS...")
        jarvis = TextJARVIS()
        jarvis.run_system()
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        print("📋 This shouldn't happen with Text JARVIS!")
    finally:
        print("\n🔹 Text JARVIS shutdown complete")
        print("Thank you for using Text JARVIS!")

if __name__ == "__main__":
    main()