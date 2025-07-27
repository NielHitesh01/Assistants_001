"""
JARVIS Enhanced Wake Word Detection System
Advanced voice activation with multiple wake words and phrases
"""

import speech_recognition as sr
import threading
import time
import re
import random
from core.speech import speak
import sys
import os

class JARVISWakeWord:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        
        # 🔥 EXPANDED WAKE WORDS - Multiple Categories
        self.wake_words = {
            # Primary wake words
            "primary": [
                "jarvis",
                "hey jarvis", 
                "hello jarvis",
                "ok jarvis"
            ],
            
            # Polite activations
            "polite": [
                "excuse me jarvis",
                "jarvis please",
                "jarvis sir",
                "may i jarvis",
                "pardon me jarvis"
            ],
            
            # Urgent activations
            "urgent": [
                "jarvis help",
                "jarvis urgent",
                "jarvis emergency",
                "jarvis now",
                "jarvis quick"
            ],
            
            # Casual activations
            "casual": [
                "yo jarvis",
                "sup jarvis",
                "jarvis buddy",
                "jarvis dude",
                "what's up jarvis"
            ],
            
            # Formal activations
            "formal": [
                "computer",
                "ai assistant",
                "artificial intelligence",
                "voice assistant",
                "digital assistant"
            ],
            
            # Iron Man style
            "iron_man": [
                "friday",
                "computer jarvis",
                "stark",
                "tony stark",
                "iron man"
            ],
            
            # Wake up commands
            "wake_up": [
                "wake up jarvis",
                "jarvis wake up",
                "jarvis online",
                "jarvis activate",
                "jarvis start",
                "jarvis boot up",
                "jarvis power on"
            ],
            
            # Attention commands
            "attention": [
                "attention jarvis",
                "jarvis attention",
                "listen jarvis",
                "jarvis listen",
                "focus jarvis"
            ],
            
            # Question starters
            "questions": [
                "jarvis can you",
                "jarvis could you",
                "jarvis would you",
                "jarvis will you",
                "jarvis do you"
            ],
            
            # Time-based
            "time_based": [
                "good morning jarvis",
                "good afternoon jarvis", 
                "good evening jarvis",
                "good night jarvis"
            ],
            
            # Status checks
            "status": [
                "jarvis status",
                "jarvis are you there",
                "jarvis respond",
                "jarvis check"
            ]
        }
        
        # Flatten all wake words into single list for easy checking
        self.all_wake_words = []
        for category, words in self.wake_words.items():
            self.all_wake_words.extend(words)
        
        # Response categories based on wake word type
        self.responses = {
            "primary": [
                "Yes, Sir? How may I assist you?",
                "At your service, Sir. What can I do for you?",
                "I'm here, Sir. How can I help?",
                "Ready to assist, Sir. What do you need?"
            ],
            "polite": [
                "Of course, Sir. How may I be of service?",
                "Certainly, Sir. What can I help you with?",
                "Yes, Sir? I'm listening attentively.",
                "At your disposal, Sir. How may I assist?"
            ],
            "urgent": [
                "I'm here, Sir! What's the emergency?",
                "Standing by for urgent assistance, Sir!",
                "Ready for immediate action, Sir!",
                "Emergency protocols active, Sir. How can I help?"
            ],
            "casual": [
                "What's up, Sir? How can I help?",
                "Hey there! What do you need?",
                "I'm here, buddy! What's going on?",
                "Ready when you are, Sir!"
            ],
            "formal": [
                "Computer systems online, Sir. Awaiting instructions.",
                "AI assistant ready for your commands, Sir.",
                "Digital assistant at your service, Sir.",
                "Systems operational. How may I assist you today?"
            ],
            "iron_man": [
                "Stark technology online, Sir. How may I assist?",
                "Friday protocols activated, Sir.",
                "Arc reactor powered and ready, Sir.",
                "Stark Industries AI at your service, Sir."
            ],
            "wake_up": [
                "Good morning, Sir! Systems are now online.",
                "Awakening complete, Sir. All systems operational.",
                "Boot sequence complete, Sir. Ready for commands.",
                "JARVIS online and ready, Sir!"
            ],
            "attention": [
                "You have my full attention, Sir.",
                "Listening intently, Sir. What do you need?",
                "Focused and ready, Sir.",
                "All sensors directed to you, Sir."
            ],
            "questions": [
                "Absolutely, Sir. What would you like me to do?",
                "Certainly, Sir. What's your request?",
                "Of course, Sir. I'm ready to help.",
                "Yes, Sir. What can I do for you?"
            ],
            "time_based": [
                "Good morning, Sir! Hope you're having a wonderful day.",
                "Good afternoon, Sir! How may I brighten your day?",
                "Good evening, Sir! How can I assist you tonight?",
                "Good night, Sir! What can I help you with?"
            ],
            "status": [
                "All systems operational, Sir. Standing by.",
                "I'm here and ready, Sir. Status: fully operational.",
                "Online and functional, Sir. How may I assist?",
                "Systems check complete, Sir. Ready for commands."
            ]
        }
        
        # Sensitivity settings
        self.confidence_threshold = 0.7
        self.partial_match_threshold = 0.8
        
        # Adjust for ambient noise
        with self.microphone as source:
            print("🎙️ Calibrating microphone for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Microphone calibrated")
        
        # Configure recognizer for better wake word detection
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
    
    def find_wake_word_category(self, text):
        """Find which category of wake word was detected"""
        text_lower = text.lower().strip()
        
        for category, words in self.wake_words.items():
            for wake_word in words:
                if wake_word in text_lower:
                    return category, wake_word
        
        return None, None
    
    def get_response_for_category(self, category):
        """Get appropriate response based on wake word category"""
        if category in self.responses:
            return random.choice(self.responses[category])
        else:
            return random.choice(self.responses["primary"])
    
    def fuzzy_match_wake_word(self, text):
        """Check for partial matches of wake words"""
        text_lower = text.lower().strip()
        
        # Remove common filler words that might interfere
        filler_words = ["um", "uh", "like", "you know", "so", "well"]
        for filler in filler_words:
            text_lower = text_lower.replace(filler, "")
        
        # Check for partial matches
        for wake_word in self.all_wake_words:
            # Simple word-based matching
            wake_words_parts = wake_word.split()
            text_parts = text_lower.split()
            
            # Check if most wake word parts are in the text
            matches = sum(1 for part in wake_words_parts if part in text_parts)
            match_ratio = matches / len(wake_words_parts)
            
            if match_ratio >= self.partial_match_threshold:
                return True, wake_word
        
        return False, None
    
    def listen_for_wake_word(self):
        """Enhanced wake word detection with multiple phrases"""
        print("🎤 JARVIS Enhanced Wake Word Detection Active")
        print("💡 Available wake phrases:")
        
        # Display available wake words by category
        for category, words in self.wake_words.items():
            print(f"   {category.title()}: {', '.join(words[:3])}{'...' if len(words) > 3 else ''}")
        
        print("🔊 Listening for activation...")
        
        self.listening = True
        consecutive_timeouts = 0
        
        while self.listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1.5, phrase_time_limit=4)
                
                try:
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio, language='en-US').lower()
                    
                    if text.strip():  # Only process non-empty text
                        print(f"🔊 Heard: '{text}'")
                        consecutive_timeouts = 0
                        
                        # Check for exact wake word matches first
                        category, matched_word = self.find_wake_word_category(text)
                        
                        if category:
                            print(f"✅ Wake word detected: '{matched_word}' (Category: {category})")
                            response = self.get_response_for_category(category)
                            speak(response)
                            return True, category, matched_word
                        
                        # Check for fuzzy matches if no exact match
                        fuzzy_match, fuzzy_word = self.fuzzy_match_wake_word(text)
                        if fuzzy_match:
                            print(f"✅ Fuzzy wake word match: '{fuzzy_word}'")
                            response = random.choice(self.responses["primary"])
                            speak(response)
                            return True, "fuzzy", fuzzy_word
                        
                        # Check for contextual activation (questions/commands that imply JARVIS)
                        contextual_triggers = [
                            "what time is it",
                            "what's the weather",
                            "open",
                            "search for",
                            "play",
                            "turn on",
                            "turn off"
                        ]
                        
                        if any(trigger in text for trigger in contextual_triggers):
                            print(f"🎯 Contextual activation detected: '{text}'")
                            speak("I heard a command, Sir. Activating JARVIS.")
                            return True, "contextual", text
                        
                except sr.UnknownValueError:
                    # No clear speech detected, continue listening
                    pass
                except sr.RequestError as e:
                    print(f"❌ Speech recognition error: {e}")
                    time.sleep(1)
                    
            except sr.WaitTimeoutError:
                # Timeout, continue listening
                consecutive_timeouts += 1
                if consecutive_timeouts > 20:  # Show status every 20 timeouts (~30 seconds)
                    print("🎤 Still listening for wake words...")
                    consecutive_timeouts = 0
                pass
            except KeyboardInterrupt:
                print("\n⏹️ Wake word detection stopped")
                self.listening = False
                return False, None, None
        
        return False, None, None
    
    def test_wake_words(self):
        """Test wake word recognition without full activation"""
        print("🧪 WAKE WORD TESTING MODE")
        print("Say any wake word to test detection...")
        print("Press Ctrl+C to stop testing")
        
        while True:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=4)
                
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"🔊 Heard: '{text}'")
                    
                    category, matched_word = self.find_wake_word_category(text)
                    if category:
                        print(f"   ✅ MATCH: '{matched_word}' (Category: {category})")
                    else:
                        fuzzy_match, fuzzy_word = self.fuzzy_match_wake_word(text)
                        if fuzzy_match:
                            print(f"   🎯 FUZZY MATCH: '{fuzzy_word}'")
                        else:
                            print("   ❌ No wake word detected")
                    
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"❌ Recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                pass
            except KeyboardInterrupt:
                print("\n✅ Wake word testing stopped")
                break
    
    def stop_listening(self):
        """Stop wake word detection"""
        self.listening = False

def voice_activate_jarvis():
    """Enhanced voice activation with multiple wake words"""
    print("="*70)
    print("🤖 JARVIS ENHANCED VOICE ACTIVATION SYSTEM")
    print("="*70)
    
    try:
        # Initialize enhanced wake word detector
        wake_detector = JARVISWakeWord()
        
        # Ask user for mode
        print("\n🎯 Select Mode:")
        print("1. Normal activation (default)")
        print("2. Test wake words")
        
        try:
            choice = input("Enter choice (1-2): ").strip()
        except:
            choice = "1"
        
        if choice == "2":
            wake_detector.test_wake_words()
            return
        
        # Start listening for wake word
        activated, category, matched_word = wake_detector.listen_for_wake_word()
        
        if activated:
            print("🚀 Starting JARVIS...")
            print(f"🎯 Activated by: {matched_word} ({category})")
            speak("JARVIS systems activating, Sir.")
            
            # Import and run main JARVIS
            try:
                from main import main
                main()
            except ImportError:
                # Fallback to master_jarvis if main doesn't exist
                from master_jarvis import main
                main()
        else:
            print("👋 Voice activation cancelled")
    
    except Exception as e:
        print(f"❌ Voice activation error: {e}")
        print("💡 Try running 'python master_jarvis.py' directly")

# Additional wake word patterns for advanced detection
ADVANCED_PATTERNS = {
    # Natural language wake patterns
    "natural": [
        r".*jarvis.*can you.*",
        r".*jarvis.*please.*",
        r".*jarvis.*help.*",
        r".*jarvis.*what.*",
        r".*jarvis.*how.*",
        r".*jarvis.*when.*",
        r".*jarvis.*where.*",
        r".*jarvis.*why.*"
    ],
    
    # Command patterns
    "commands": [
        r".*jarvis.*open.*",
        r".*jarvis.*search.*",
        r".*jarvis.*play.*",
        r".*jarvis.*show.*",
        r".*jarvis.*tell.*",
        r".*jarvis.*find.*"
    ]
}

def advanced_pattern_match(text):
    """Advanced pattern matching for wake word detection"""
    text_lower = text.lower()
    
    for category, patterns in ADVANCED_PATTERNS.items():
        for pattern in patterns:
            if re.match(pattern, text_lower):
                return True, category, pattern
    
    return False, None, None

if __name__ == "__main__":
    voice_activate_jarvis()
