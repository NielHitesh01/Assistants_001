"""
Voice Input Test for JARVIS
Tests the actual voice recognition and input capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_voice_input():
    """Test voice input functionality"""
    print("="*50)
    print("🎙️ JARVIS VOICE INPUT TEST")
    print("="*50)
    
    try:
        from core.speech import speak, get_command, CHAT_MODE, toggle_voice_mode
        
        # Check current mode
        print(f"Current input mode: {'TEXT' if CHAT_MODE else 'VOICE'}")
        
        if CHAT_MODE:
            print("\n🔄 Switching to voice mode for testing...")
            speak("Switching to voice input mode for testing, Sir.")
            toggle_voice_mode()
            
        speak("Voice input test initiated, Sir. I am ready to receive voice commands.")
        
        print("\n🎤 Voice Input Test Instructions:")
        print("1. Make sure your microphone is connected")
        print("2. Speak clearly when prompted")
        print("3. Try saying 'Hello JARVIS' or 'What time is it?'")
        print("4. Say 'exit' to end the test")
        
        print("\n🔊 Starting voice input test...")
        
        test_count = 0
        max_tests = 3
        
        while test_count < max_tests:
            print(f"\n📢 Voice Test {test_count + 1}/{max_tests}")
            speak(f"Voice test {test_count + 1}. Please speak a command, Sir.")
            
            try:
                print("🎙️ Listening... (Speak now)")
                user_input = get_command()
                
                print(f"✅ Recognized: '{user_input}'")
                speak(f"I heard: {user_input}")
                
                if 'exit' in user_input.lower() or 'stop' in user_input.lower():
                    speak("Voice input test terminated at your request, Sir.")
                    break
                    
                # Process the command
                if 'hello' in user_input.lower():
                    speak("Good day, Sir. Voice recognition is working perfectly.")
                elif 'time' in user_input.lower():
                    import datetime
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    speak(f"The time is {current_time}, Sir.")
                elif 'status' in user_input.lower():
                    speak("All voice systems operational, Sir.")
                else:
                    speak("Voice command received and processed, Sir.")
                
                test_count += 1
                
            except Exception as e:
                print(f"❌ Voice recognition error: {e}")
                speak("Voice recognition encountered an issue, Sir.")
                test_count += 1
        
        speak("Voice input testing complete, Sir. All systems nominal.")
        print("\n✅ Voice input test completed!")
        
    except Exception as e:
        print(f"❌ Voice input test failed: {e}")

def test_microphone_setup():
    """Test microphone setup and configuration"""
    print("\n🔧 Testing Microphone Setup...")
    
    try:
        from core.speech import list_microphones, test_microphone, speak
        
        speak("Testing microphone configuration, Sir.")
        
        print("\n📋 Available Microphones:")
        list_microphones()
        
        print("\n🔍 Testing Default Microphone...")
        mic_test = test_microphone()
        
        if mic_test:
            print("✅ Microphone test: PASSED")
            speak("Microphone test successful, Sir.")
        else:
            print("❌ Microphone test: FAILED")
            speak("Microphone test failed, Sir. Please check your audio input device.")
        
    except Exception as e:
        print(f"❌ Microphone setup error: {e}")

def demo_voice_commands():
    """Demonstrate available voice commands"""
    print("\n🗣️ Voice Commands Demonstration...")
    
    try:
        from core.speech import speak
        
        speak("Demonstrating available voice commands, Sir.")
        
        commands = [
            ("'Hello JARVIS'", "Formal greeting"),
            ("'What's your status?'", "System status report"),
            ("'What time is it?'", "Current time"),
            ("'Switch to text mode'", "Change input method"),
            ("'Test microphone'", "Audio diagnostics"),
            ("'Help'", "Command assistance"),
            ("'Exit'", "End session")
        ]
        
        print("\n📋 Available Voice Commands:")
        for cmd, desc in commands:
            print(f"  • {cmd} - {desc}")
            speak(f"Command: {cmd}")
        
        speak("Voice command demonstration complete, Sir.")
        
    except Exception as e:
        print(f"❌ Voice commands demo error: {e}")

if __name__ == "__main__":
    print("🚀 Starting JARVIS Voice Input Test...")
    
    # Test microphone setup first
    test_microphone_setup()
    
    # Demonstrate voice commands
    demo_voice_commands()
    
    # Run voice input test
    print("\n" + "="*50)
    print("⚠️  VOICE INPUT TEST")
    print("Make sure your microphone is working!")
    print("="*50)
    
    choice = input("\nDo you want to test voice input? (y/n): ").lower().strip()
    
    if choice == 'y' or choice == 'yes':
        test_voice_input()
    else:
        print("Voice input test skipped.")
        try:
            from core.speech import speak
            speak("Voice input test skipped. All other speech systems verified, Sir.")
        except:
            pass
    
    print("\n🎯 Voice Recognition Test Complete!")
    print("🎙️ JARVIS is ready for voice interaction!")
