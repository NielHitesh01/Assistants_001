# JARVIS Troubleshooting Guide

## Common Issues:

### 1. PyAudio Installation Error
**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt install portaudio19-dev
pip install pyaudio
```

### 2. Whisper Model Download Issues
- Ensure stable internet connection
- Models download automatically on first use
- Large model is ~1.5GB, be patient

### 3. Microphone Not Detected
- Check microphone permissions
- Restart JARVIS after connecting microphone
- Run: `python -m speech_recognition` to test

### 4. Voice Output Not Working
- Check TTS engine installation: `pip install pyttsx3`
- Verify audio drivers are working
- Test with: `python -c "import pyttsx3; pyttsx3.speak('test')"`

### 5. Wake Word Not Detected
- Speak clearly and close to microphone
- Enable debug mode to see what's being heard
- Adjust microphone sensitivity in settings