# 🤖 JARVIS - Personal AI Assistant

A modular, extensible voice assistant built in Python, inspired by the famous AI from Iron Man. JARVIS can help you with weather updates, news, task management, jokes, definitions, and much more!

## 🚀 Features

### ✅ Core Features (Working)
- **🎤 Speech Recognition & Synthesis** - Voice and text interaction modes
- **🧠 Memory System** - Remembers facts and information using SQLite
- **📝 Task Management** - Add, list, and summarize tasks
- **🔌 Plugin System** - Easily extensible with custom plugins
- **🌤️ Weather Updates** - Get weather information for any city
- **📰 News Headlines** - Stay updated with latest news
- **📚 Wikipedia Integration** - Search and get summaries
- **📖 Dictionary** - Get word definitions
- **😄 Jokes** - Entertainment with built-in jokes
- **⏰ Time & Date** - Current time and date information
- **🌐 Web Integration** - Open popular websites

### 🔧 Natural Language Processing
- **Simple NLU** - Intent recognition and slot extraction
- **Command Understanding** - Processes natural language commands
- **Context Awareness** - Understands context for better responses

## 📁 Project Structure

```
Jarvis/
├── main.py                 # Main application entry point
├── jarvis.py              # Legacy file (can be removed)
├── config.py              # Configuration settings
├── setup.py               # Setup and status checker
├── requirements.txt       # Python dependencies
├── jarvis_memory.db       # SQLite database for memory
├── core/                  # Core functionality
│   ├── speech.py          # Speech recognition and synthesis
│   ├── memory.py          # Memory management
│   ├── todo.py            # Task management
│   └── commands.py        # Command handling
├── services/              # External service integrations
│   ├── weather.py         # Weather API integration
│   ├── news.py            # News API integration
│   └── wikipedia.py       # Wikipedia integration
└── plugins/               # Extensible plugins
    ├── joke_plugin.py     # Joke functionality
    ├── dictionary_plugin.py # Dictionary definitions
    ├── simple_nlu_plugin.py # Natural language understanding
    └── example_plugin.py  # Template for new plugins
```

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit `config.py` and add your API keys:

```python
# Get free API key from: https://openweathermap.org/api
WEATHER_API_KEY = 'your_actual_api_key_here'

# Get free API key from: https://newsapi.org/
NEWSAPI_KEY = 'your_actual_api_key_here'
```

### 3. Run Setup Check
```bash
python setup.py
```

### 4. Start JARVIS
```bash
python main.py
```

## 🎯 Usage Examples

### Basic Commands
- `"what time is it"` - Get current time
- `"what's the date"` - Get current date
- `"help"` - List available commands
- `"stop"` or `"exit"` - Quit JARVIS

### Weather
- `"weather in London"`
- `"temperature in New York"`
- `"forecast for Tokyo"`

### News
- `"latest news"`
- `"news about technology"`
- `"headlines about sports"`

### Tasks
- `"add task buy groceries"`
- `"remind me to call mom"`
- `"list tasks"`
- `"summarize tasks"`

### Information
- `"tell me about Einstein"` (Wikipedia)
- `"define artificial intelligence"`
- `"what is Python"`

### Entertainment
- `"tell me a joke"`
- `"make me laugh"`

### Web Navigation
- `"open YouTube"`
- `"open Google"`
- `"open Gmail"`
- `"open GitHub"`

### Memory
- `"remember that my birthday is January 1st"`
- `"what do you know about my birthday"`
- `"list all facts"`

## ⚙️ Configuration Options

In `config.py`:

```python
# Mode Settings
CHAT_MODE = True          # True for text, False for voice
USE_VOSK = False         # True for offline speech recognition

# Voice Settings
VOICE_RATE = 200         # Speech rate
VOICE_VOLUME = 0.9       # Speech volume (0.0 to 1.0)

# API Keys
WEATHER_API_KEY = 'your_key'
NEWSAPI_KEY = 'your_key'
OPENAI_API_KEY = 'your_key'  # Optional for future features
```

## 🔌 Plugin Development

Create custom plugins by following this template:

```python
# plugins/my_plugin.py
def register_plugin(jarvis):
    def my_function():
        jarvis['speak']("Hello from my plugin!")
    
    jarvis['register_command']('my command', my_function)
```

Available jarvis functions:
- `jarvis['speak'](text)` - Make JARVIS speak
- `jarvis['get_command']()` - Get user input
- `jarvis['register_command'](phrase, function)` - Register new commands

## 🛠️ Current Status & Next Steps

### ✅ Completed
1. **Core Architecture** - Modular design with plugins
2. **Speech System** - Both voice and text modes
3. **Memory System** - SQLite-based persistent memory
4. **Task Management** - Add, list, summarize tasks
5. **Service Integrations** - Weather, News, Wikipedia, Dictionary
6. **Natural Language Processing** - Simple intent recognition
7. **Plugin System** - Extensible architecture
8. **Configuration System** - Easy setup and customization

### 🚧 To Complete (Next Steps)
1. **API Keys Setup** - Add your weather and news API keys
2. **Voice Mode Testing** - Test microphone functionality
3. **Advanced NLP** - Optional spaCy integration for better understanding
4. **More Plugins** - Add calendar, email, calculator plugins
5. **GUI Interface** - Optional desktop interface
6. **Mobile App** - Future mobile companion app

### 🎯 How to Complete Setup
1. **Get API Keys** (Free):
   - Weather: https://openweathermap.org/api
   - News: https://newsapi.org/
   
2. **Update config.py** with your API keys

3. **Test Basic Functionality**:
   ```bash
   python main.py
   ```

4. **Try These Commands**:
   - `"tell me a joke"`
   - `"what time is it"`
   - `"add task test JARVIS"`
   - `"define python"`

## 🐛 Troubleshooting

### Common Issues
1. **spaCy Errors** - The simple NLU plugin works without spaCy
2. **API Key Errors** - Make sure to update config.py with real API keys
3. **Microphone Issues** - Set CHAT_MODE = True for text-only mode
4. **Import Errors** - Ensure all requirements are installed

### Getting Help
- Check the console output for error messages
- Run `python setup.py` to verify configuration
- Ensure all dependencies are installed
- Check that API keys are correctly set in config.py

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by the JARVIS AI from Marvel's Iron Man
- Built with Python and various open source libraries
- Weather data from OpenWeatherMap
- News data from NewsAPI
- Dictionary definitions from Free Dictionary API

---

**Ready to get started?** Run `python setup.py` to check your configuration, then `python main.py` to start your personal AI assistant! 🚀
