"""
Simple JARVIS - Basic version that should work
"""

import pyttsx3
import time
import webbrowser
from datetime import datetime

class SimpleJARVIS:
    def __init__(self):
        # Initialize text-to-speech
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 200)
            self.voice_available = True
            print("✅ Voice system ready")
        except:
            self.voice_available = False
            print("❌ Voice system failed")
    
    def speak(self, text):
        print(f"🤖 JARVIS: {text}")
        if self.voice_available:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
    
    def process_command(self, command):
        cmd = command.lower()
        
        if 'time' in cmd:
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")
        
        elif 'date' in cmd:
            today = datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {today}")
        
        elif 'youtube' in cmd:
            webbrowser.open('https://youtube.com')
            self.speak("Opening YouTube")
        
        elif 'google' in cmd:
            webbrowser.open('https://google.com')
            self.speak("Opening Google")
        
        elif any(word in cmd for word in ['hello', 'hi', 'hey']):
            self.speak("Hello! How can I help you today?")
        
        elif any(word in cmd for word in ['exit', 'quit', 'bye']):
            self.speak("Goodbye!")
            return False
        
        else:
            self.speak("I understand. What else can I help you with?")
        
        return True
    
    def run(self):
        print("🚀 Simple JARVIS Ready!")
        self.speak("Simple JARVIS ready. Type your commands.")
        
        while True:
            try:
                command = input("\n🧠 You: ").strip()
                if command:
                    if not self.process_command(command):
                        break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    jarvis = SimpleJARVIS()
    jarvis.run()