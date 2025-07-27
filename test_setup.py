"""
JARVIS Setup Test - Check if all dependencies work
"""

def test_dependencies():
    print("🔍 Testing JARVIS dependencies...\n")
    
    # Test 1: Basic Python modules
    try:
        import sys, os, time, threading, webbrowser
        print("✅ Core Python modules: OK")
    except Exception as e:
        print(f"❌ Core modules error: {e}")
    
    # Test 2: Text-to-Speech
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("✅ Text-to-Speech (pyttsx3): OK")
        
        # Test voice output
        engine.say("Testing voice output")
        engine.runAndWait()
        print("✅ Voice output: Working")
    except Exception as e:
        print(f"❌ TTS error: {e}")
    
    # Test 3: NumPy
    try:
        import numpy as np
        print("✅ NumPy: OK")
    except Exception as e:
        print(f"❌ NumPy error: {e}")
    
    # Test 4: Audio recording
    try:
        import sounddevice as sd
        import soundfile as sf
        print("✅ Audio processing: OK")
        
        # Test microphone
        print("🎙️ Testing microphone (3 seconds)...")
        audio = sd.rec(int(3 * 16000), samplerate=16000, channels=1)
        sd.wait()
        print("✅ Microphone recording: OK")
    except Exception as e:
        print(f"❌ Audio error: {e}")
    
    # Test 5: Whisper AI
    try:
        import whisper
        print("✅ Whisper AI: OK")
        
        print("🧠 Loading Whisper model (this may take a moment)...")
        model = whisper.load_model("base")  # Use base instead of large for testing
        print("✅ Whisper model loaded: OK")
    except Exception as e:
        print(f"❌ Whisper error: {e}")
    
    # Test 6: Fuzzy matching
    try:
        from fuzzywuzzy import fuzz
        print("✅ Fuzzy matching: OK")
    except Exception as e:
        print(f"❌ Fuzzy matching error: {e}")
    
    print("\n🎯 Dependency test complete!")
    print("If all tests passed, JARVIS should work!")

if __name__ == "__main__":
    test_dependencies()