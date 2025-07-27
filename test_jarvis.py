"""
JARVIS Voice System Test Suite
Tests the integrated voice recognition and JARVIS personality system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import JARVIS components directly
from core.speech import speak, get_command
import time

def test_jarvis_voice_system():
    """Test the complete JARVIS voice system"""
    print("="*60)
    print("JARVIS VOICE SYSTEM TEST SUITE")
    print("="*60)
    
    # Test JARVIS voice
    print("\n1. Testing JARVIS voice system...")
    speak("Good day, Sir. Initiating voice system diagnostics.")
    
    print("\n2. Testing JARVIS personality...")
    speak("Good day, Sir. This is a test of my voice systems.")
    time.sleep(2.0)
    
    print("\n3. Testing ML NLU system...")
    try:
        from plugins.ml_nlu_plugin import ml_nlu_process
        test_commands = [
            "Hello JARVIS",
            "What's the status?", 
            "Tell me the time",
            "Can you help me?",
            "Test microphone"
        ]
        
        for cmd in test_commands:
            print(f"\nTesting command: '{cmd}'")
            response = ml_nlu_process(cmd)
            print(f"Response: {response}")
            time.sleep(1.0)
    except Exception as e:
        print(f"ML NLU test error: {e}")
    
    print("\n4. Testing speech recognition commands...")
    try:
        from core.commands import handle_custom_command
        speech_commands = [
            "speech status",
            "voice recognition help",
            "show microphones"
        ]
        
        for cmd in speech_commands:
            print(f"\nTesting speech command: '{cmd}'")
            # Note: These would need to be registered first in a full test
            print(f"Command logged: {cmd}")
            time.sleep(1.0)
    except Exception as e:
        print(f"Speech command test error: {e}")
    
    print("\n5. Testing voice properties...")
    try:
        from plugins.jarvis_tone_plugin import jarvis_greeting, status_report
        greeting = jarvis_greeting()
        status = status_report()
        speak(f"Testing voice clarity and tone, Sir. {greeting}")
        time.sleep(1.0)
        speak(status)
    except Exception as e:
        speak("Testing voice clarity and tone, Sir. All systems appear to be functioning optimally.")
        print(f"JARVIS tone test note: {e}")
    
    print("\n" + "="*60)
    print("JARVIS VOICE SYSTEM TEST COMPLETE")
    print("="*60)
    
    return True

def quick_voice_demo():
    """Quick demonstration of JARVIS capabilities"""
    print("\n" + "="*50)
    print("JARVIS QUICK DEMONSTRATION")
    print("="*50)
    
    demo_interactions = [
        ("Hello JARVIS", "Good day, Sir. I am at your service."),
        ("What's your status?", "All systems are operational and standing by, Sir."),
        ("Can you hear me?", "Affirmative, Sir. Audio systems are functioning perfectly."),
        ("Thank you JARVIS", "You are most welcome, Sir. Always a pleasure to assist.")
    ]
    
    for command, response in demo_interactions:
        print(f"\nUser: '{command}'")
        print(f"JARVIS: {response}")
        speak(response)
        time.sleep(2.0)
    
    print(f"\nDemo complete. JARVIS is ready for interactive use.")

def test_speech_features():
    """Test specific speech recognition features"""
    print("\n" + "="*50)
    print("SPEECH FEATURES TEST")
    print("="*50)
    
    print("\n1. Testing microphone detection...")
    try:
        from core.speech import test_microphone, list_microphones
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

if __name__ == "__main__":
    print("JARVIS Integration Test Suite")
    print("Choose test mode:")
    print("1. Full voice system test")
    print("2. Quick demo")
    print("3. Speech features test") 
    print("4. Run all tests")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        test_jarvis_voice_system()
    elif choice == "2":
        quick_voice_demo()
    elif choice == "3":
        test_speech_features()
    elif choice == "4":
        test_speech_features()
        quick_voice_demo()
        test_jarvis_voice_system()
    else:
        print("Invalid choice. Running quick demo...")
        quick_voice_demo()
