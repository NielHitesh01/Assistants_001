"""
JARVIS Setup Script
Run this script to set up your JARVIS assistant
"""

import os
import sys

def setup_jarvis():
    print("🤖 JARVIS Setup Assistant")
    print("=" * 50)
    
    # Check if config.py exists
    if not os.path.exists('config.py'):
        print("❌ config.py not found!")
        return False
    
    print("✅ Configuration file found")
    
    # Check if we're in chat mode or voice mode
    try:
        from config import CHAT_MODE
        if CHAT_MODE:
            print("📝 Running in CHAT MODE (text-based)")
        else:
            print("🎤 Running in VOICE MODE (speech-based)")
    except ImportError:
        print("⚠️  Could not import configuration")
    
    # Check API keys
    print("\n🔑 Checking API Keys...")
    try:
        from config import WEATHER_API_KEY, NEWSAPI_KEY
        
        if WEATHER_API_KEY == 'your_openweathermap_api_key':
            print("⚠️  Weather API key not configured")
            print("   Get a free key from: https://openweathermap.org/api")
        else:
            print("✅ Weather API key configured")
            
        if NEWSAPI_KEY == 'your_newsapi_key':
            print("⚠️  News API key not configured")
            print("   Get a free key from: https://newsapi.org/")
        else:
            print("✅ News API key configured")
            
    except ImportError:
        print("❌ Could not check API keys")
    
    # Check database
    print("\n💾 Checking Database...")
    if os.path.exists('jarvis_memory.db'):
        print("✅ Memory database exists")
    else:
        print("ℹ️  Memory database will be created on first run")
    
    # List available plugins
    print("\n🔌 Available Plugins:")
    plugin_dir = 'plugins'
    if os.path.exists(plugin_dir):
        plugins = [f for f in os.listdir(plugin_dir) if f.endswith('.py') and f != '__init__.py']
        for plugin in plugins:
            print(f"   • {plugin}")
    
    print("\n🚀 Setup Complete!")
    print("Run 'python main.py' to start JARVIS")
    print("\nBasic Commands to Try:")
    print("  • 'weather in London'")
    print("  • 'tell me a joke'")
    print("  • 'add task buy groceries'")
    print("  • 'what time is it'")
    print("  • 'help'")
    print("  • 'stop' or 'exit' to quit")
    
    return True

if __name__ == "__main__":
    setup_jarvis()
