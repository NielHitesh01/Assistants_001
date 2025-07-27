"""
JARVIS Configuration File
Modify these settings to customize your JARVIS
"""

# Voice Settings
VOICE_RATE = 220  # Speech rate (words per minute)
VOICE_VOLUME = 0.9  # Volume level (0.0 to 1.0)

# Whisper Model Settings
WHISPER_MODEL = "large"  # Options: tiny, base, small, medium, large
WAKE_WORD_DURATION = 3   # Seconds to listen for wake words
COMMAND_DURATION = 5     # Seconds to listen for commands

# Wake Words
WAKE_WORDS = [
    "jarvis", "hey jarvis", "hello jarvis", 
    "ok jarvis", "computer", "jarvis please"
]

# API Keys (Optional)
OPENAI_API_KEY = "your_openai_api_key_here"

# Debug Mode
DEBUG_MODE = True  # Set to False for production

# Audio Settings
SAMPLE_RATE = 16000  # Audio sample rate for Whisper
ENERGY_THRESHOLD = 300  # Microphone sensitivity
PAUSE_THRESHOLD = 0.4   # Pause detection threshold

# OpenWeatherMap API Configuration
# Get your free API key from: https://openweathermap.org/api
WEATHER_API_KEY = 'your_openweathermap_api_key'

# NewsAPI Configuration  
# Get your free API key from: https://newsapi.org/
NEWSAPI_KEY = 'your_newsapi_key'

# OpenAI API Configuration (optional, for advanced features)
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY = 'your_openai_api_key'

# Voice Settings
CHAT_MODE = True  # Set to True for text mode, False for voice mode
USE_VOSK = False  # Set to True to use Vosk for offline speech recognition

# Voice Settings for TTS
VOICE_RATE = 200  # Speech rate
VOICE_VOLUME = 0.9  # Speech volume (0.0 to 1.0)
