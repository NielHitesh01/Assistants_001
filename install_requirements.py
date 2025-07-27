"""
JARVIS Installation Script
Automatically installs all required dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed: {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install: {package}")
        return False

def main():
    """Install all JARVIS requirements"""
    print("="*60)
    print("🚀 JARVIS AI ASSISTANT - DEPENDENCY INSTALLER")
    print("="*60)
    
    # Core requirements
    core_packages = [
        "pyttsx3>=2.90",
        "speechrecognition>=3.10.0", 
        "requests>=2.31.0",
        "pyaudio>=0.2.11"
    ]
    
    # Whisper AI packages (recommended)
    whisper_packages = [
        "openai-whisper>=20231117",
        "sounddevice>=0.4.6",
        "soundfile>=0.12.1", 
        "numpy>=1.24.0"
    ]
    
    # Advanced text processing
    advanced_packages = [
        "fuzzywuzzy>=0.18.0",
        "python-levenshtein>=0.21.1"
    ]
    
    # Optional AI packages
    ai_packages = [
        "openai>=1.0.0"
    ]
    
    print("📦 Installing core packages...")
    for package in core_packages:
        install_package(package)
    
    print("\n🧠 Installing Whisper AI packages...")
    for package in whisper_packages:
        install_package(package)
    
    print("\n🎯 Installing advanced text processing...")
    for package in advanced_packages:
        install_package(package)
    
    print("\n🤖 Installing optional AI packages...")
    user_choice = input("Install OpenAI integration? (y/n): ").lower()
    if user_choice == 'y':
        for package in ai_packages:
            install_package(package)
    
    print("\n✅ Installation complete!")
    print("🚀 You can now run: python master_jarvis_backup.py")

if __name__ == "__main__":
    main()