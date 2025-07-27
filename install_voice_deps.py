"""
JARVIS Voice Dependencies Installer
Installs all required packages for voice functionality
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install all voice dependencies"""
    print("🎤 JARVIS Voice Dependencies Installer")
    print("=" * 50)
    
    # Required packages for voice functionality
    packages = [
        "speechrecognition",
        "pyttsx3",
        "pyaudio",
        "requests",
        "openai",
    ]
    
    # Windows-specific packages
    if sys.platform == "win32":
        packages.extend([
            "pywin32",
            "comtypes"
        ])
    
    success_count = 0
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Installation Summary: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("🎉 All voice dependencies installed successfully!")
        print("🎤 JARVIS voice functionality is now ready!")
    else:
        print("⚠️ Some packages failed to install")
        print("💡 Try running as administrator or check your internet connection")
    
    # Test imports
    print("\n🧪 Testing imports...")
    try:
        import speech_recognition as sr
        print("✅ speech_recognition: OK")
    except ImportError:
        print("❌ speech_recognition: FAILED")
    
    try:
        import pyttsx3
        print("✅ pyttsx3: OK")
    except ImportError:
        print("❌ pyttsx3: FAILED")
    
    try:
        import pyaudio
        print("✅ pyaudio: OK")
    except ImportError:
        print("❌ pyaudio: FAILED")

if __name__ == "__main__":
    main()