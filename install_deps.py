"""Quick dependency installer for JARVIS"""

import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed")
        return True
    except:
        print(f"❌ {package} failed")
        return False

packages = ["speechrecognition", "pyttsx3", "pyaudio", "requests"]
print("📦 Installing JARVIS dependencies...")

for pkg in packages:
    install_package(pkg)

print("🎤 JARVIS is ready!")