"""
Simple JARVIS Voice Activator
Quick voice activation script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_voice_activate():
    """Quick voice activation for JARVIS"""
    print("🎙️ JARVIS Quick Voice Activator")
    print("=" * 40)
    
    try:
        from core.speech import speak, get_command, CHAT_MODE, toggle_voice_mode
        
        # Ensure we're in voice mode
        if CHAT_MODE:
            print("🔄 Switching to voice mode...")
            toggle_voice_mode()
        
        # Voice activation greeting
        speak("JARVIS voice activation system online, Sir.")
        speak("How may I assist you today?")
        
        # Start listening for commands
        print("🎤 JARVIS is now listening for voice commands...")
        print("💡 Speak any command or say 'start main program' for full experience")
        
        while True:
            try:
                command = get_command()
                print(f"🔊 You said: '{command}'")
                
                if any(word in command.lower() for word in ['start main', 'full program', 'complete jarvis']):
                    speak("Starting complete JARVIS experience, Sir.")
                    from main import main
                    main()
                    break
                elif any(word in command.lower() for word in ['exit', 'stop', 'quit']):
                    speak("Voice activation session ended, Sir.")
                    break
                else:
                    # Simple responses for common commands
                    if 'hello' in command.lower():
                        speak("Good day, Sir. JARVIS at your service.")
                    elif 'time' in command.lower():
                        import datetime
                        current_time = datetime.datetime.now().strftime("%H:%M")
                        speak(f"The time is {current_time}, Sir.")
                    elif 'status' in command.lower():
                        speak("All systems operational, Sir.")
                    else:
                        speak("Command acknowledged, Sir. Say 'start main program' for full JARVIS experience.")
            
            except KeyboardInterrupt:
                speak("Voice activation terminated, Sir.")
                break
            except Exception as e:
                print(f"Command processing error: {e}")
                speak("Please repeat your command, Sir.")
    
    except Exception as e:
        print(f"❌ Voice activation error: {e}")
        print("💡 Try running 'python main.py' directly")

if __name__ == "__main__":
    quick_voice_activate()
