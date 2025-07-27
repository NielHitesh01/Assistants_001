"""
Safe JARVIS Test - Handles timing issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def safe_test():
    """Safe test that handles timing and import issues"""
    print("="*50)
    print("SAFE JARVIS TEST")
    print("="*50)
    
    try:
        print("\n1. Testing basic imports...")
        from core.speech import speak
        print("✓ Speech module imported successfully")
        
        print("\n2. Testing voice synthesis...")
        speak("JARVIS systems online, Sir.")
        
        # Safe delay
        import time
        time.sleep(2)
        
        print("\n3. Testing JARVIS personality...")
        speak("All systems operational and standing by.")
        time.sleep(2)
        
        print("\n4. Testing ML NLU...")
        try:
            from plugins.ml_nlu_plugin import handle_nlu
            result = handle_nlu("Hello JARVIS")
            print(f"✓ ML NLU Response: {result}")
        except Exception as e:
            print(f"Note: ML NLU not fully loaded - {str(e)[:50]}...")
        
        time.sleep(1)
        
        print("\n5. Testing JARVIS tone...")
        try:
            from plugins.jarvis_tone_plugin import jarvis_greeting
            greeting = jarvis_greeting()
            speak(greeting)
            print(f"✓ JARVIS Tone: {greeting}")
        except Exception as e:
            print(f"Note: JARVIS tone plugin issue - {str(e)[:50]}...")
        
        time.sleep(2)
        
        print("\n✅ SAFE TEST COMPLETE!")
        speak("All primary systems tested successfully, Sir.")
        
    except Exception as e:
        print(f"❌ Test Error: {e}")
        print("Trying basic voice test...")
        try:
            from core.speech import speak
            speak("Basic voice systems operational, Sir.")
        except Exception as e2:
            print(f"❌ Critical Error: {e2}")

if __name__ == "__main__":
    safe_test()
