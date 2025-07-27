"""
JARVIS Voice Activation Guide
Complete guide for voice-activating JARVIS
"""

def show_voice_activation_guide():
    """Display comprehensive voice activation guide"""
    
    print("="*70)
    print("🎙️ JARVIS VOICE ACTIVATION GUIDE")
    print("="*70)
    
    print("\n🚀 METHOD 1: Quick Start (Recommended)")
    print("   Command: python main.py")
    print("   • JARVIS starts immediately and greets you")
    print("   • Ready for voice commands right away")
    print("   • Full JARVIS experience with all features")
    
    print("\n🎤 METHOD 2: Wake Word Activation")
    print("   Command: python wake_word.py")
    print("   • Listens continuously for 'Hey JARVIS'")
    print("   • Say 'Hey JARVIS' to activate")
    print("   • JARVIS responds and starts full program")
    
    print("\n⚡ METHOD 3: Quick Voice Activator")
    print("   Command: python voice_activate.py")
    print("   • Immediate voice mode activation")
    print("   • Basic commands available instantly")
    print("   • Say 'start main program' for full experience")
    
    print("\n🖱️ METHOD 4: Windows Batch File")
    print("   Double-click: start_jarvis.bat")
    print("   • Easy Windows activation")
    print("   • No command line needed")
    print("   • Automatically starts wake word detection")
    
    print("\n🔊 WAKE WORDS YOU CAN USE:")
    wake_words = [
        "• 'Hey JARVIS'",
        "• 'JARVIS'", 
        "• 'Hello JARVIS'",
        "• 'OK JARVIS'"
    ]
    for word in wake_words:
        print(f"   {word}")
    
    print("\n🗣️ VOICE COMMANDS AFTER ACTIVATION:")
    commands = [
        "• 'What's your status?' - System status",
        "• 'What time is it?' - Current time",
        "• 'Tell me a joke' - Entertainment",
        "• 'Switch to voice mode' - Ensure voice input",
        "• 'Enable wake word mode' - Continuous listening",
        "• 'Help' - Command assistance",
        "• 'Exit' - End session"
    ]
    for cmd in commands:
        print(f"   {cmd}")
    
    print("\n⚙️ VOICE ACTIVATION SETUP:")
    print("   1. Ensure microphone is connected and working")
    print("   2. Check audio input levels in Windows")
    print("   3. Test with: python -c \"from core.speech import test_microphone; test_microphone()\"")
    print("   4. Run any activation method above")
    print("   5. Speak clearly and wait for JARVIS response")
    
    print("\n🔧 TROUBLESHOOTING:")
    print("   • If no response: Check microphone connection")
    print("   • If recognition fails: Speak louder and clearer")
    print("   • If activation doesn't work: Try 'python main.py' directly")
    print("   • For persistent issues: Test with 'python speech_test.py'")
    
    print("\n💡 ADVANCED WAKE WORD FEATURES:")
    print("   • Ambient noise adjustment")
    print("   • Multiple wake word variations")
    print("   • Continuous background listening")
    print("   • Automatic activation and response")
    print("   • Integration with full JARVIS system")
    
    print("\n🎯 RECOMMENDED USAGE:")
    print("   1. For daily use: python main.py (fastest)")
    print("   2. For hands-free: python wake_word.py")
    print("   3. For quick tests: python voice_activate.py")
    print("   4. For convenience: start_jarvis.bat")
    
    print("\n" + "="*70)
    print("🤖 JARVIS VOICE ACTIVATION READY!")
    print("Choose your preferred method and start talking!")
    print("="*70)

if __name__ == "__main__":
    show_voice_activation_guide()
    
    print("\n🎙️ Testing voice synthesis...")
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from core.speech import speak
        speak("Voice activation guide complete, Sir. Choose your preferred activation method and let's begin.")
    except Exception as e:
        print(f"Voice test: {e}")
    
    print("\n🚀 Ready to activate JARVIS? Choose your method!")
