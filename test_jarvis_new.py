"""
JARVIS Voice System Test Suite
Tests the integrated voice recognition and JARVIS personality system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import JARVIS components directly
from core.speech import speak, get_command, test_microphone, list_microphones
import time

def test_jarvis_voice_system():
    """Test the complete JARVIS voice system"""
    print("="*60)
    print("JARVIS VOICE SYSTEM TEST SUITE")
    print("="*60)
    
    # Test JARVIS voice
    print("\n1. Testing JARVIS voice system...")
    speak("Good day, Sir. Initiating voice system diagnostics.")
    time.sleep(1)
    
    print("\n2. Testing JARVIS personality...")
    speak("I am JARVIS, your AI assistant. All systems are operational and standing by.")
    time.sleep(1)
    
    print("\n3. Testing ML NLU system...")
    try:
        from plugins.ml_nlu_plugin import handle_nlu
        test_commands = [
            "Hello JARVIS",
            "What's the status?", 
            "Tell me the time",
            "Can you help me?"
        ]
        
        for cmd in test_commands:
            print(f"\nTesting command: '{cmd}'")
            response = handle_nlu(cmd)
            print(f"ML Response: {response}")
            time.sleep(0.5)
    except Exception as e:
        print(f"ML NLU test error: {e}")
    
    print("\n4. Testing JARVIS tone...")
    try:
        from plugins.jarvis_tone_plugin import jarvis_greeting, status_report
        greeting = jarvis_greeting()
        status = status_report()
        speak(greeting)
        time.sleep(0.5)
        speak(status)
    except Exception as e:
        print(f"JARVIS tone test error: {e}")
    
    print("\n5. Testing voice properties...")
    speak("Testing voice clarity and tone, Sir. All systems appear to be functioning optimally.")
    
    print("\n" + "="*60)
    print("JARVIS VOICE SYSTEM TEST COMPLETE")
    print("="*60)
    
    return True

def quick_voice_demo():
    """Quick demonstration of JARVIS capabilities"""
    print("\n" + "="*50)
    print("JARVIS QUICK DEMONSTRATION")
    print("="*50)
    
    demo_responses = [
        ("Hello JARVIS", "Good day, Sir. I am at your service."),
        ("What's your status?", "All systems are operational and standing by, Sir."),
        ("Can you hear me?", "Affirmative, Sir. Audio systems are functioning perfectly."),
        ("Thank you JARVIS", "You are most welcome, Sir. Always a pleasure to assist.")
    ]
    
    for command, response in demo_responses:
        print(f"\nUser: '{command}'")
        print(f"JARVIS: {response}")
        speak(response)
        time.sleep(1)
    
    print(f"\nDemo complete. JARVIS is ready for interactive use.")

def test_speech_features():
    """Test specific speech recognition features"""
    print("\n" + "="*50)
    print("SPEECH FEATURES TEST")
    print("="*50)
    
    print("\n1. Testing microphone detection...")
    try:
        list_microphones()
    except Exception as e:
        print(f"Microphone listing error: {e}")
    
    print("\n2. Testing microphone functionality...")
    try:
        test_result = test_microphone()
        print(f"Microphone test result: {'PASSED' if test_result else 'FAILED'}")
    except Exception as e:
        print(f"Microphone test error: {e}")
    
    print("\n3. Testing voice mode toggle...")
    try:
        from core.speech import CHAT_MODE
        print(f"Current mode: {'TEXT' if CHAT_MODE else 'VOICE'}")
    except Exception as e:
        print(f"Voice mode test error: {e}")
    
    speak("Speech recognition systems are operational, Sir.")
    print("\nSpeech features test complete.")

def simple_jarvis_test():
    """Simple test just for voice synthesis"""
    print("Simple JARVIS Voice Test")
    print("="*30)
    
    jarvis_phrases = [
        "Good day, Sir. I am JARVIS.",
        "All systems are operational and standing by.",
        "How may I assist you today, Sir?",
        "Voice recognition systems are online.",
        "Ready to receive commands, Sir."
    ]
    
    for phrase in jarvis_phrases:
        print(f"JARVIS: {phrase}")
        speak(phrase)
        time.sleep(1)
    
    print("\nSimple voice test complete.")

if __name__ == "__main__":
    print("JARVIS Integration Test Suite")
    print("Choose test mode:")
    print("1. Full voice system test")
    print("2. Quick demo")
    print("3. Speech features test") 
    print("4. Simple voice test")
    print("5. Run all tests")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        test_jarvis_voice_system()
    elif choice == "2":
        quick_voice_demo()
    elif choice == "3":
        test_speech_features()
    elif choice == "4":
        simple_jarvis_test()
    elif choice == "5":
        test_speech_features()
        quick_voice_demo()
        test_jarvis_voice_system()
    else:
        print("Invalid choice. Running simple voice test...")
        simple_jarvis_test()
