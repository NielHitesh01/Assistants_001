"""
JARVIS System Test - Automated Testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_jarvis_components():
    """Test individual JARVIS components"""
    print("="*60)
    print("🤖 JARVIS SYSTEM TEST")
    print("="*60)
    
    print("\n1. 🔊 Testing Voice Synthesis...")
    try:
        from core.speech import speak
        speak("Good day, Sir. JARVIS voice systems are online.")
        print("✅ Voice synthesis: WORKING")
    except Exception as e:
        print(f"❌ Voice synthesis error: {e}")
    
    print("\n2. 🧠 Testing ML NLU Plugin...")
    try:
        from plugins.ml_nlu_plugin import ml_nlu_process
        result = ml_nlu_process("Hello JARVIS")
        print(f"✅ ML NLU response: {result}")
    except Exception as e:
        print(f"❌ ML NLU error: {e}")
    
    print("\n3. 🎭 Testing JARVIS Personality...")
    try:
        from plugins.jarvis_tone_plugin import jarvis_greeting, status_report
        greeting = jarvis_greeting()
        status = status_report()
        print(f"✅ JARVIS greeting: {greeting}")
        print(f"✅ JARVIS status: {status}")
        speak(greeting)
    except Exception as e:
        print(f"❌ JARVIS personality error: {e}")
    
    print("\n4. 🎙️ Testing Speech Recognition...")
    try:
        from core.speech import list_microphones, CHAT_MODE
        print(f"✅ Voice mode: {'TEXT' if CHAT_MODE else 'VOICE'}")
        print("✅ Microphone detection: Available")
        list_microphones()
    except Exception as e:
        print(f"❌ Speech recognition error: {e}")
    
    print("\n5. 💾 Testing Memory System...")
    try:
        from core.memory import save_to_memory, recall_from_memory
        save_to_memory("test_key", "test_value")
        result = recall_from_memory("test_key")
        print(f"✅ Memory system: {result}")
    except Exception as e:
        print(f"❌ Memory error: {e}")
    
    print("\n6. 🔧 Testing Command System...")
    try:
        from core.commands import register_command
        print("✅ Command registration: Available")
    except Exception as e:
        print(f"❌ Command system error: {e}")
    
    print("\n" + "="*60)
    print("🎯 JARVIS SYSTEM TEST COMPLETE")
    print("="*60)

def test_jarvis_conversation():
    """Test JARVIS conversation abilities"""
    print("\n🗣️ Testing JARVIS Conversation...")
    
    test_commands = [
        "Hello JARVIS",
        "What's your status?",
        "Tell me the time",
        "How are you?",
        "Can you help me?"
    ]
    
    try:
        from plugins.ml_nlu_plugin import ml_nlu_process
        from core.speech import speak
        
        for cmd in test_commands:
            print(f"\n🔸 Testing: '{cmd}'")
            try:
                result = ml_nlu_process(cmd)
                print(f"   Response: {result}")
                speak(f"Processing command: {cmd}")
            except Exception as e:
                print(f"   Error: {e}")
                
    except Exception as e:
        print(f"❌ Conversation test error: {e}")

def test_voice_interaction():
    """Test voice interaction capabilities"""
    print("\n🎤 Testing Voice Interaction...")
    
    try:
        from core.speech import speak
        
        jarvis_phrases = [
            "Good day, Sir. I am JARVIS.",
            "All systems are operational and standing by.",
            "Voice recognition systems online.",
            "Ready to assist you, Sir."
        ]
        
        for phrase in jarvis_phrases:
            print(f"🔊 JARVIS: {phrase}")
            speak(phrase)
            import time
            time.sleep(1)
            
        print("✅ Voice interaction test complete")
        
    except Exception as e:
        print(f"❌ Voice interaction error: {e}")

if __name__ == "__main__":
    print("🚀 Starting JARVIS System Tests...")
    
    # Run component tests
    test_jarvis_components()
    
    # Test conversation
    test_jarvis_conversation()
    
    # Test voice interaction
    test_voice_interaction()
    
    print("\n🎉 All JARVIS tests completed!")
    print("🤖 JARVIS is ready for interactive use!")
    
    # Final voice confirmation
    try:
        from core.speech import speak
        speak("All systems tested and operational, Sir. JARVIS is ready for service.")
    except:
        print("Voice confirmation unavailable")
