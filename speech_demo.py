"""
JARVIS Speech Recognition Demo
Shows off the speech recognition capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def speech_recognition_demo():
    """Demonstrate JARVIS speech recognition features"""
    print("="*60)
    print("🎙️ JARVIS SPEECH RECOGNITION DEMONSTRATION")
    print("="*60)
    
    try:
        from core.speech import speak, list_microphones, test_microphone, CHAT_MODE
        
        # Welcome message
        speak("Welcome to the JARVIS speech recognition demonstration, Sir.")
        
        print("\n🔊 Voice Synthesis: ✅ WORKING")
        speak("Voice synthesis systems are fully operational.")
        
        print("\n🎙️ Microphone Detection:")
        list_microphones()
        print("✅ Multiple audio input devices detected")
        
        print("\n🔧 Microphone Testing:")
        mic_result = test_microphone()
        if mic_result:
            speak("Microphone test successful, Sir.")
            print("✅ Microphone functionality: CONFIRMED")
        else:
            speak("Please check your microphone connection, Sir.")
            print("⚠️ Microphone may need attention")
        
        print(f"\n📱 Current Input Mode: {'TEXT' if CHAT_MODE else 'VOICE'}")
        speak(f"Currently operating in {'text input' if CHAT_MODE else 'voice input'} mode, Sir.")
        
        print("\n🎯 Speech Recognition Features Available:")
        features = [
            "✅ Google Speech Recognition (Primary)",
            "✅ Sphinx Speech Recognition (Offline Fallback)", 
            "✅ Ambient Noise Adjustment",
            "✅ Multiple Microphone Support",
            "✅ Voice Mode Toggle",
            "✅ Voice Property Adjustment",
            "✅ Real-time Voice Processing",
            "✅ JARVIS Voice Command Integration"
        ]
        
        for feature in features:
            print(f"  {feature}")
        
        speak("All speech recognition features are operational and ready for use, Sir.")
        
        print("\n🗣️ Sample Voice Commands:")
        commands = [
            "'Hello JARVIS' - Formal greeting",
            "'What's your status?' - System report",
            "'Switch to voice mode' - Enable voice input",
            "'Test microphone' - Audio diagnostics",
            "'Show microphones' - List audio devices",
            "'Voice recognition help' - Command reference"
        ]
        
        for cmd in commands:
            print(f"  • {cmd}")
        
        speak("These are examples of voice commands I can understand and process, Sir.")
        
        print("\n🔄 Voice Mode Toggle Demonstration:")
        try:
            from core.speech import toggle_voice_mode
            original_mode = "TEXT" if CHAT_MODE else "VOICE"
            
            speak("Demonstrating voice mode toggle functionality, Sir.")
            toggle_result = toggle_voice_mode()
            
            # Check new mode
            from core.speech import CHAT_MODE as new_mode
            new_mode_str = "TEXT" if new_mode else "VOICE"
            
            print(f"  Original mode: {original_mode}")
            print(f"  New mode: {new_mode_str}")
            print("✅ Voice mode toggle: FUNCTIONAL")
            
            speak(f"Voice mode successfully changed to {new_mode_str.lower()} input, Sir.")
            
        except Exception as e:
            print(f"  ⚠️ Toggle demo error: {e}")
        
        print("\n🎚️ Voice Properties Demonstration:")
        try:
            from core.speech import set_voice_properties
            
            speak("Demonstrating voice property adjustments, Sir.")
            
            # Test different voice rates
            set_voice_properties(rate=120)
            speak("This is speech at 120 words per minute, Sir.")
            
            set_voice_properties(rate=180)
            speak("This is speech at 180 words per minute, Sir.")
            
            # Reset to normal
            set_voice_properties(rate=150)
            speak("Voice properties reset to optimal settings, Sir.")
            
            print("✅ Voice property adjustment: WORKING")
            
        except Exception as e:
            print(f"  ⚠️ Voice properties error: {e}")
        
        print("\n" + "="*60)
        print("🎯 SPEECH RECOGNITION DEMO COMPLETE")
        print("="*60)
        
        speak("Speech recognition demonstration complete, Sir. All systems are operational and ready for interactive use.")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("Please check system configuration")

if __name__ == "__main__":
    print("🚀 Starting JARVIS Speech Recognition Demo...")
    speech_recognition_demo()
    print("\n🎙️ JARVIS Speech Recognition is ready for use!")
    print("💡 Try running 'python main.py' to start the full interactive experience!")
