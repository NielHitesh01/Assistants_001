"""
JARVIS Multimodal Interface - Simple & Clear Version
"""

import speech_recognition as sr
import threading
import time
import sys
import os
from core.speech import speak, get_command, CHAT_MODE, toggle_voice_mode
import queue
from datetime import datetime

class SimpleJARVISInterface:
    def __init__(self):
        print("🚀 JARVIS Multimodal Interface Starting...")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        self.running = True
        self.command_queue = queue.Queue()
        
        # Startup voice feedback
        print("🎙️ Setting up microphone...")
        try:
            with self.microphone as source:
                print("📊 Calibrating audio... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
                print(f"✅ Audio calibrated. Energy threshold: {self.recognizer.energy_threshold}")
            
            # Clear startup voice confirmation
            speak("JARVIS Multimodal Interface is now online and ready, Sir.")
            print("✅ Voice output working")
            
        except Exception as e:
            print(f"❌ Microphone setup failed: {e}")
            speak("Warning: Microphone setup encountered issues, Sir.")

    def voice_listener(self):
        """Simple voice listener"""
        print("🎙️ Voice monitoring started")
        
        while self.running:
            try:
                with self.microphone as source:
                    # Listen for voice input
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio).lower().strip()
                    if text and len(text) > 1:
                        self.command_queue.put(('voice', text))
                        print(f"🎙️ Voice: '{text}'")
                        
                except sr.UnknownValueError:
                    pass  # Ignore unclear audio
                except sr.RequestError as e:
                    print(f"❌ Speech service error: {e}")
                    
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Voice listener error: {e}")
                time.sleep(0.5)

    def text_listener(self):
        """Simple text listener"""
        print("⌨️ Text input ready")
        
        while self.running:
            try:
                text = input().strip()
                if text:
                    self.command_queue.put(('text', text))
                    print(f"⌨️ Text: '{text}'")
                    
            except (EOFError, KeyboardInterrupt):
                self.running = False
                break
            except Exception as e:
                print(f"Text input error: {e}")

    def start_interface(self):
        """Start the multimodal interface"""
        print("\n" + "="*50)
        print("🧠 JARVIS MULTIMODAL INTERFACE")
        print("="*50)
        print("💬 Ready for voice and text commands")
        print("🔊 Voice commands: Just speak naturally")
        print("⌨️ Text commands: Type and press Enter")
        print("🛑 Exit: Say or type 'exit', 'quit', or 'goodbye'")
        print("="*50)
        
        # Final startup confirmation
        speak("Interface fully operational. You may now speak or type your commands, Sir.")
        
        # Start voice and text listeners
        voice_thread = threading.Thread(target=self.voice_listener, daemon=True)
        text_thread = threading.Thread(target=self.text_listener, daemon=True)
        
        voice_thread.start()
        text_thread.start()
        
        # Main command processing loop
        self.process_commands()

    def process_commands(self):
        """Process incoming commands"""
        while self.running:
            try:
                # Wait for command
                input_type, command = self.command_queue.get(timeout=1.0)
                
                # Process the command
                self.handle_command(command, input_type)
                
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                break
        
        # Shutdown
        speak("Goodbye, Sir. Interface shutting down.")
        print("👋 JARVIS Interface closed")

    def handle_command(self, command, input_type):
        """Handle individual commands"""
        cmd = command.lower().strip()
        
        # Exit commands
        if any(word in cmd for word in ['exit', 'quit', 'goodbye', 'shutdown']):
            self.running = False
            return
        
        # Basic commands
        if any(word in cmd for word in ['hello', 'hi', 'hey']):
            speak("Hello, Sir. How may I assist you?")
            
        elif any(word in cmd for word in ['time', 'what time']):
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}, Sir.")
            
        elif any(word in cmd for word in ['date', 'what date', 'today']):
            today = datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {today}, Sir.")
            
        elif any(word in cmd for word in ['help', 'commands']):
            speak("I can respond to: hello, time, date, status, help, and exit commands, Sir.")
            
        elif any(word in cmd for word in ['status', 'how are you']):
            speak("All systems are operational and ready to assist, Sir.")
            
        elif 'test' in cmd:
            speak("Test completed successfully. Voice and text input are both working perfectly, Sir.")
            
        else:
            # Generic response
            speak("I understand, Sir. How else may I help you?")
        
        print(f"✅ Command processed via {input_type}")

def main():
    """Main function"""
    try:
        # Create and start interface
        jarvis = SimpleJARVISInterface()
        jarvis.start_interface()
        
    except KeyboardInterrupt:
        print("\n⏹️ Program interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")
        speak("An error occurred, Sir. Please restart the interface.")

if __name__ == "__main__":
    main()
