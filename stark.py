"""
STARK - Superior Tactical AI Recognition Kernel
Advanced Voice Assistant with Bulletproof Architecture

Created: 2025
Author: AI Assistant Team
Version: 1.2.0 - NILA WAKE WORD

CLEAR AGENDA:
1. Rock-solid wake word detection with "NILA"
2. Continuous voice monitoring that NEVER stops
3. Dual input (voice + text) with seamless switching
4. FIXED search algorithm
5. Perfect conversation flow
6. Bulletproof error handling and recovery
7. Clean, maintainable code architecture
"""

import sys
import os
import time
import webbrowser
from datetime import datetime
import random
import threading
import json
from typing import Optional, Dict, List, Tuple

# === DEPENDENCY MANAGEMENT ===
class DependencyManager:
    """Manages all external dependencies with graceful fallbacks"""
    
    def __init__(self):
        self.tts_available = False
        self.voice_input_available = False
        self.tts_engine = None
        self.speech_recognizer = None
        self.microphone = None
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Initialize all dependencies with proper error handling"""
        print("🔧 Initializing STARK dependencies...")
        
        # Text-to-Speech Setup
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 190)
            self.tts_engine.setProperty('volume', 0.9)
            
            # Test TTS
            self.tts_engine.say("STARK systems initializing")
            self.tts_engine.runAndWait()
            
            self.tts_available = True
            print("✅ Text-to-Speech: ONLINE")
            
        except Exception as e:
            print(f"❌ TTS Setup Failed: {e}")
            print("💡 Install: pip install pyttsx3")
            self.tts_available = False
        
        # Speech Recognition Setup
        try:
            import speech_recognition as sr
            
            self.speech_recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Optimize recognition settings for better accuracy
            self.speech_recognizer.energy_threshold = 3000  # Lower for better sensitivity
            self.speech_recognizer.pause_threshold = 0.6    # Shorter pause
            self.speech_recognizer.phrase_threshold = 0.3
            self.speech_recognizer.dynamic_energy_threshold = True
            
            # Calibrate microphone
            print("🎙️ Calibrating microphone for optimal performance...")
            with self.microphone as source:
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=1.5)
            
            self.voice_input_available = True
            print("✅ Speech Recognition: ONLINE (Google API)")
            
        except ImportError:
            print("❌ Speech Recognition Not Installed")
            print("💡 Install: pip install speechrecognition pyaudio")
            self.voice_input_available = False
        except Exception as e:
            print(f"❌ Microphone Setup Failed: {e}")
            self.voice_input_available = False

# === COMMAND PROCESSOR ===
class CommandProcessor:
    """Handles all command processing with modular architecture"""
    
    def __init__(self, stark_core):
        self.stark = stark_core
        self.command_registry = self._build_command_registry()
    
    def _build_command_registry(self) -> Dict:
        """Build comprehensive command registry"""
        return {
            'time': {
                'triggers': ['time', 'what time', 'current time', 'tell me the time'],
                'handler': self._handle_time,
                'description': 'Get current time'
            },
            'date': {
                'triggers': ['date', 'what date', 'today', 'current date', 'what day'],
                'handler': self._handle_date,
                'description': 'Get current date'
            },
            'youtube': {
                'triggers': ['youtube', 'open youtube', 'launch youtube', 'go to youtube'],
                'handler': self._handle_youtube,
                'description': 'Open YouTube'
            },
            'google': {
                'triggers': ['google', 'open google', 'launch google', 'go to google'],
                'handler': self._handle_google,
                'description': 'Open Google'
            },
            'search': {
                'triggers': ['search', 'look up', 'find', 'google search', 'search for'],
                'handler': self._handle_search,
                'description': 'Search the web'
            },
            'greeting': {
                'triggers': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon'],
                'handler': self._handle_greeting,
                'description': 'Exchange greetings'
            },
            'status': {
                'triggers': ['status', 'system status', 'how are you', 'report'],
                'handler': self._handle_status,
                'description': 'Get system status'
            },
            'joke': {
                'triggers': ['joke', 'tell joke', 'tell me joke', 'funny', 'make me laugh'],
                'handler': self._handle_joke,
                'description': 'Tell a joke'
            },
            'voice_control': {
                'triggers': ['voice on', 'voice off', 'enable voice', 'disable voice', 'mute', 'unmute'],
                'handler': self._handle_voice_control,
                'description': 'Control voice features'
            },
            'help': {
                'triggers': ['help', 'commands', 'what can you do', 'assistance'],
                'handler': self._handle_help,
                'description': 'Show available commands'
            },
            'shutdown': {
                'triggers': ['exit', 'quit', 'goodbye', 'bye', 'shutdown', 'stop'],
                'handler': self._handle_shutdown,
                'description': 'Shutdown STARK'
            }
        }
    
    def process_command(self, command_text: str) -> bool:
        """Process command with intelligent matching"""
        command_text = command_text.lower().strip()
        
        if not command_text:
            return False
        
        print(f"🔍 Processing: '{command_text}'")
        
        # Find matching command
        for cmd_name, cmd_data in self.command_registry.items():
            for trigger in cmd_data['triggers']:
                if trigger in command_text:
                    print(f"✅ Command matched: {cmd_name}")
                    return cmd_data['handler'](command_text)
        
        # No specific command found - general response
        return self._handle_general_response(command_text)
    
    def _handle_time(self, cmd: str) -> bool:
        current_time = datetime.now().strftime("%I:%M %p")
        self.stark.speak(f"The current time is {current_time}, Sir.")
        return True
    
    def _handle_date(self, cmd: str) -> bool:
        today = datetime.now().strftime("%A, %B %d, %Y")
        self.stark.speak(f"Today is {today}, Sir.")
        return True
    
    def _handle_youtube(self, cmd: str) -> bool:
        webbrowser.open('https://youtube.com')
        self.stark.speak("Opening YouTube for you, Sir.")
        return True
    
    def _handle_google(self, cmd: str) -> bool:
        webbrowser.open('https://google.com')
        self.stark.speak("Opening Google for you, Sir.")
        return True
    
    def _handle_search(self, cmd: str) -> bool:
        """Handle search commands with FIXED algorithm"""
        # Extract search query
        query = ""
        
        # FIXED: Better search query extraction
        search_triggers = ['search for', 'search', 'look up', 'find']
        
        for trigger in search_triggers:
            if trigger in cmd:
                query = cmd.split(trigger, 1)[-1].strip()
                break
        
        # FIXED: Ensure we have a valid query
        if query and len(query) > 1:
            # Clean up the query
            query = query.replace('for me', '').replace('please', '').strip()
            
            if query:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                print(f"🔍 Opening search: {search_url}")
                
                try:
                    webbrowser.open(search_url)
                    self.stark.speak(f"Searching for {query}, Sir.")
                    return True
                except Exception as e:
                    print(f"❌ Browser error: {e}")
                    self.stark.speak("I couldn't open the browser, Sir.")
                    return False
        
        # If no query found, ask for clarification
        self.stark.speak("What would you like me to search for, Sir?")
        return True
    
    def _handle_greeting(self, cmd: str) -> bool:
        greetings = [
            "Hello, Sir! How can I assist you today?",
            "Good day, Sir! STARK systems ready to serve.",
            "Greetings, Sir! All systems operational.",
            "Hello! Standing by for your commands, Sir.",
            "Good to see you, Sir! How may I help?"
        ]
        self.stark.speak(random.choice(greetings))
        return True
    
    def _handle_status(self, cmd: str) -> bool:
        status_parts = ["All STARK systems operational, Sir."]
        
        if self.stark.deps.tts_available:
            status_parts.append("Speech output online.")
        
        if self.stark.deps.voice_input_available:
            status_parts.append("Voice recognition active.")
        
        status_parts.append("Standing by for commands.")
        
        self.stark.speak(" ".join(status_parts))
        return True
    
    def _handle_joke(self, cmd: str) -> bool:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my computer a joke about UDP, but I'm not sure it got it.",
            "There are only 10 types of people: those who understand binary and those who don't.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "I would tell you a joke about the cloud, but it's over your head!",
            "Why did the developer go broke? Because he used up all his cache!"
        ]
        self.stark.speak(random.choice(jokes))
        return True
    
    def _handle_voice_control(self, cmd: str) -> bool:
        if any(phrase in cmd for phrase in ['voice off', 'disable voice', 'mute']):
            self.stark.voice_enabled = False
            self.stark.speak("Voice input disabled, Sir. Text commands only.")
        elif any(phrase in cmd for phrase in ['voice on', 'enable voice', 'unmute']):
            if self.stark.deps.voice_input_available:
                self.stark.voice_enabled = True
                self.stark.speak("Voice input enabled, Sir.")
            else:
                self.stark.speak("Voice input not available, Sir.")
        return True
    
    def _handle_help(self, cmd: str) -> bool:
        help_text = """STARK Command Reference:
        
🕐 Time & Date: "what time is it", "what's the date"
🌐 Web Navigation: "open YouTube", "open Google"
🔍 Search: "search [query]", "look up [topic]"
💬 Interaction: "hello", "status", "tell me a joke"
🎤 Voice Control: "voice on/off", "mute/unmute"
❓ Help: "help", "what can you do"
🚪 Exit: "goodbye", "exit", "shutdown"

Say 'NILA' to activate voice commands, Sir."""
        
        self.stark.speak("Here are my available commands, Sir.")
        print(help_text)
        return True
    
    def _handle_shutdown(self, cmd: str) -> bool:
        farewell_messages = [
            "Goodbye, Sir. STARK systems shutting down.",
            "Until next time, Sir. It was a pleasure serving you.",
            "Farewell, Sir. STARK going offline.",
            "Goodbye, Sir. All systems powering down."
        ]
        self.stark.speak(random.choice(farewell_messages))
        self.stark.running = False
        return True
    
    def _handle_general_response(self, cmd: str) -> bool:
        responses = [
            "I understand, Sir. How else may I assist?",
            "Noted, Sir. What else can I help with?",
            "Processing that information, Sir. Anything else?",
            "I hear you, Sir. What's next?",
            "Understood, Sir. Standing by for further commands."
        ]
        self.stark.speak(random.choice(responses))
        return True

# === VOICE MONITORING SYSTEM ===
class VoiceMonitor:
    """Handles continuous voice monitoring with bulletproof reliability"""
    
    def __init__(self, stark_core):
        self.stark = stark_core
        # CHANGED: Beautiful and easy-to-pronounce wake words with "NILA"
        self.wake_words = ["nila", "hey nila", "hello nila", "computer", "assistant"]
        self.monitoring_active = False
        self.consecutive_errors = 0
        self.max_errors = 10  # Reduced for faster recovery
    
    def start_monitoring(self):
        """Start voice monitoring in separate thread"""
        if not self.stark.deps.voice_input_available:
            print("⚠️ Voice input not available - monitoring disabled")
            return False
        
        self.monitoring_active = True
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        print("✅ Voice monitoring started")
        return True
    
    def stop_monitoring(self):
        """Stop voice monitoring"""
        self.monitoring_active = False
        print("🔇 Voice monitoring stopped")
    
    def _monitoring_loop(self):
        """FIXED: Main voice monitoring loop with continuous operation"""
        print("🎤 STARK VOICE MONITORING ACTIVE")
        print("💬 Say 'NILA' followed by your command")
        print("💬 Or say 'NILA' and wait for prompt")
        print("💬 Voice monitoring will continue after each command")
        
        while self.stark.running and self.monitoring_active and self.stark.voice_enabled:
            try:
                # Listen for speech with shorter timeout for responsiveness
                audio_text = self._listen_for_speech(timeout=3, phrase_limit=8)
                
                if audio_text:
                    self.consecutive_errors = 0  # Reset error counter
                    self._process_audio_input(audio_text)
                
                # FIXED: Continue immediately without long delays
                time.sleep(0.05)  # Very short delay
                
            except Exception as e:
                self.consecutive_errors += 1
                if self.consecutive_errors <= 3:  # Only show first few errors
                    print(f"❌ Voice monitoring error #{self.consecutive_errors}: {e}")
                
                if self.consecutive_errors >= self.max_errors:
                    print("⚠️ Too many consecutive errors - restarting voice system")
                    self._restart_voice_system()
                
                time.sleep(0.2)  # Short delay on error
        
        print("🔇 Voice monitoring loop ended")
    
    def _listen_for_speech(self, timeout: int = 3, phrase_limit: int = None) -> Optional[str]:
        """Listen for speech with proper error handling"""
        if not self.stark.deps.voice_input_available:
            return None
        
        try:
            with self.stark.deps.microphone as source:
                # Reduced timeout for more responsive listening
                audio = self.stark.deps.speech_recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_limit
                )
            
            # Recognize speech
            text = self.stark.deps.speech_recognizer.recognize_google(audio).lower()
            print(f"🔍 Heard: '{text}'")
            return text
            
        except Exception as e:
            # Only show non-timeout errors
            if "WaitTimeoutError" not in str(type(e)) and "UnknownValueError" not in str(type(e)):
                print(f"🔇 Audio processing issue: {type(e).__name__}")
            return None
    
    def _process_audio_input(self, audio_text: str):
        """FIXED: Process detected audio input with immediate return to listening"""
        # Check for wake word
        wake_word_detected = False
        detected_wake_word = ""
        
        for wake_word in self.wake_words:
            if wake_word in audio_text:
                wake_word_detected = True
                detected_wake_word = wake_word
                break
        
        if wake_word_detected:
            print(f"✅ Wake word '{detected_wake_word}' detected!")
            
            # Extract command part
            command_part = audio_text.replace(detected_wake_word, "").strip()
            
            if command_part:
                # Direct command
                print(f"🚀 Direct command: '{command_part}'")
                self.stark.speak("Right away, Sir.")
                success = self.stark.command_processor.process_command(command_part)
                
                if success:
                    print("✅ Command executed successfully")
                else:
                    print("⚠️ Command execution had issues")
            else:
                # Wake word only - listen for command
                print("🎧 Wake word detected - waiting for command")
                self.stark.speak("Yes, Sir? I'm ready for your command.")
                
                follow_up = self._listen_for_speech(timeout=6, phrase_limit=8)
                
                if follow_up:
                    print(f"🚀 Follow-up command: '{follow_up}'")
                    success = self.stark.command_processor.process_command(follow_up)
                    
                    if success:
                        print("✅ Follow-up executed successfully")
                    else:
                        print("⚠️ Follow-up had issues")
                else:
                    self.stark.speak("Standing by for your next command, Sir.")
            
            # FIXED: Always return to listening immediately
            print("🔄 Returning to continuous voice monitoring...")
            print("🎙️ Ready for next command...")
            
        else:
            # Only show wake word messages occasionally to reduce spam
            if random.random() < 0.1:  # 10% chance to show message
                print(f"⏸️ Listening for 'NILA'...")
    
    def _restart_voice_system(self):
        """Restart voice recognition system"""
        try:
            import speech_recognition as sr
            
            self.stark.deps.speech_recognizer = sr.Recognizer()
            self.stark.deps.microphone = sr.Microphone()
            
            # Re-optimize settings
            self.stark.deps.speech_recognizer.energy_threshold = 3000
            self.stark.deps.speech_recognizer.pause_threshold = 0.6
            self.stark.deps.speech_recognizer.phrase_threshold = 0.3
            self.stark.deps.speech_recognizer.dynamic_energy_threshold = True
            
            self.consecutive_errors = 0
            print("✅ Voice system restarted successfully")
            
        except Exception as e:
            print(f"❌ Voice system restart failed: {e}")
            self.monitoring_active = False

# === MAIN STARK CORE ===
class STARK:
    """
    STARK - Superior Tactical AI Recognition Kernel
    Main AI assistant class with modular architecture
    """
    
    def __init__(self):
        self.running = True
        self.voice_enabled = True
        self.debug_mode = True
        
        # Initialize components
        self.deps = DependencyManager()
        self.command_processor = CommandProcessor(self)
        self.voice_monitor = VoiceMonitor(self)
        
        print("🤖 STARK Core initialized")
    
    def speak(self, text: str):
        """Handle text-to-speech output"""
        print(f"🤖 STARK: {text}")
        
        if self.deps.tts_available:
            try:
                self.deps.tts_engine.say(text)
                self.deps.tts_engine.runAndWait()
            except Exception as e:
                if self.debug_mode:
                    print(f"❌ Speech output error: {e}")
    
    def start_text_interface(self):
        """Start the text-based interface"""
        print("\n" + "="*80)
        print("🚀 STARK - SUPERIOR TACTICAL AI RECOGNITION KERNEL")
        print("="*80)
        print("⌨️ Text Commands: Type your requests below")
        print("🎤 Voice Commands: Say 'NILA' to activate")
        print(f"🔊 Speech Output: {'ENABLED' if self.deps.tts_available else 'DISABLED'}")
        print(f"🎙️ Voice Input: {'ENABLED' if self.deps.voice_input_available else 'DISABLED'}")
        print("")
        print("💡 Quick Start:")
        print("   • Type 'help' for full command list")
        print("   • Say 'NILA what time is it' for voice commands")
        print("   • Say 'NILA search artificial intelligence'")
        print("   • Type 'exit' to shutdown")
        print("="*80)
        
        self.speak("STARK systems online and ready for your commands, Sir.")
        
        while self.running:
            try:
                user_input = input(f"\n🧠 Command: ").strip()
                
                if user_input:
                    print(f"📝 Processing: '{user_input}'")
                    self.command_processor.process_command(user_input)
                else:
                    print("💭 Standing by for commands...")
                
            except KeyboardInterrupt:
                print("\n⏹️ Shutdown initiated...")
                self.speak("Goodbye, Sir.")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Interface error: {e}")
                continue
    
    def run(self):
        """Main STARK execution"""
        print("="*80)
        print("🚀 STARK v1.2 - NILA VOICE ASSISTANT")
        print("🎯 Wake word: NILA • Fixed search • Continuous listening")
        print("="*80)
        
        # System status report
        print("\n🔍 SYSTEM STATUS:")
        print(f"✅ Core System: ONLINE")
        print(f"{'✅' if self.deps.tts_available else '❌'} Speech Output: {'ONLINE' if self.deps.tts_available else 'OFFLINE'}")
        print(f"{'✅' if self.deps.voice_input_available else '❌'} Voice Input: {'ONLINE' if self.deps.voice_input_available else 'OFFLINE'}")
        print(f"✅ Command Processor: ONLINE ({len(self.command_processor.command_registry)} commands)")
        print(f"✅ Web Integration: ONLINE")
        print(f"🎤 Wake Word: NILA (beautiful and easy to pronounce)")
        print("="*80)
        
        # Start voice monitoring
        if self.voice_enabled and self.deps.voice_input_available:
            self.voice_monitor.start_monitoring()
        
        # Start text interface (blocking)
        self.start_text_interface()
        
        # Cleanup
        if self.voice_monitor.monitoring_active:
            self.voice_monitor.stop_monitoring()

# === MAIN EXECUTION ===
def main():
    """Main entry point"""
    try:
        print("🚀 Initializing STARK Advanced Voice Assistant v1.2...")
        stark = STARK()
        stark.run()
        
    except KeyboardInterrupt:
        print("\n⏹️ STARK shutdown by user")
    except Exception as e:
        print(f"❌ Critical STARK error: {e}")
    finally:
        print("\n🔹 STARK shutdown complete")
        print("Thank you for using STARK!")

if __name__ == "__main__":
    main()