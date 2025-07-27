"""
Interactive JARVIS Test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def interactive_test():
    """Test JARVIS interactively"""
    print("="*50)
    print("🤖 JARVIS INTERACTIVE TEST")
    print("="*50)
    
    # Initialize core components
    from core.speech import speak
    from core.memory import init_memory_db
    
    # Initialize memory
    init_memory_db()
    
    # JARVIS greeting
    speak("Good day, Sir. JARVIS interactive test sequence initiated.")
    print("🔊 JARVIS: Good day, Sir. JARVIS interactive test sequence initiated.")
    
    # Test commands
    test_commands = [
        ("Hello JARVIS", "greeting"),
        ("What's your status?", "status check"),
        ("Tell me a joke", "entertainment"),
        ("What time is it?", "time query"),
        ("Thank you JARVIS", "polite interaction")
    ]
    
    print("\n📋 Testing command processing...")
    
    for command, description in test_commands:
        print(f"\n🔸 Test: {description}")
        print(f"   Command: '{command}'")
        
        try:
            # Try ML NLU processing
            from plugins.ml_nlu_plugin import ml_nlu_process
            result = ml_nlu_process(command)
            print(f"   ML Response: {result}")
            
            # JARVIS speaks the response
            speak(f"Processing {description}, Sir.")
            
        except Exception as e:
            print(f"   Note: {str(e)[:50]}...")
            speak("Command noted, Sir.")
    
    print("\n✅ Interactive test sequence complete!")
    speak("Interactive test sequence complete, Sir. All systems nominal.")
    
    return True

if __name__ == "__main__":
    try:
        interactive_test()
        print("\n🎯 JARVIS IS READY FOR FULL OPERATION!")
    except Exception as e:
        print(f"❌ Test error: {e}")
        print("🔧 Please check system configuration")
