import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import openai
import sqlite3
import os
import subprocess
import smtplib
import time
import random
import requests

# Initialize the speech engine
engine = pyttsx3.init()
openai.api_key = 'your_openai_api_key'  # Replace with your OpenAI key

custom_commands = {}

CHAT_MODE = True  # Set to True for chat (text) mode, False for audio mode

def register_command(phrase, function):
    custom_commands[phrase] = function

def handle_custom_command(command):
    for phrase, func in custom_commands.items():
        if phrase in command:
            func()
            return True
    return False

def open_github():
    speak("Opening GitHub.")
    webbrowser.open("https://github.com")

def open_google():
    speak("Opening Google.")
    webbrowser.open("https://www.google.com")

def open_gmail():
    speak("Opening Gmail.")
    webbrowser.open("https://mail.google.com")

def open_notepad():
    speak("Opening Notepad.")
    os.system('notepad.exe')

def open_calculator():
    speak("Opening Calculator.")
    os.system('calc.exe')

def open_vscode():
    speak("Opening VS Code.")
    os.system('code')

def volume_mute():
    speak("Muting volume.")
    os.system('nircmd.exe mutesysvolume 1')

def volume_up():
    speak("Increasing volume.")
    os.system('nircmd.exe changesysvolume 20000')

def volume_down():
    speak("Decreasing volume.")
    os.system('nircmd.exe changesysvolume -20000')

def take_screenshot():
    import pyautogui
    filename = f'screenshot_{int(time.time())}.png'
    pyautogui.screenshot(filename)
    speak(f"Screenshot saved as {filename}.")

def lock_computer():
    speak("Locking computer.")
    os.system('rundll32.exe user32.dll,LockWorkStation')

def shutdown_computer():
    speak("Shutting down computer.")
    os.system('shutdown /s /t 1')

def restart_computer():
    speak("Restarting computer.")
    os.system('shutdown /r /t 1')

def tell_joke():
    jokes = [
        "Why did the computer show up at work late? It had a hard drive!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the developer go broke? Because he used up all his cache!"
    ]
    speak(random.choice(jokes))

def motivational_quote():
    quotes = [
        "Success is not the key to happiness. Happiness is the key to success.",
        "The only way to do great work is to love what you do.",
        "Don’t watch the clock; do what it does. Keep going."
    ]
    speak(random.choice(quotes))

def set_timer():
    speak("For how many seconds should I set the timer?")
    try:
        seconds = int(take_command())
        speak(f"Setting a timer for {seconds} seconds.")
        time.sleep(seconds)
        speak("Time's up!")
    except ValueError:
        speak("Sorry, I didn't get the number.")

def show_weather():
    speak("For which city?")
    city = take_command()
    api_key = 'your_openweathermap_api_key'  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
        else:
            speak("City not found.")
    except Exception:
        speak("Sorry, I couldn't fetch the weather.")

def show_news(topic=None):
    api_key = 'your_newsapi_key'  # Replace with your NewsAPI key
    if api_key == 'your_newsapi_key':
        speak("NewsAPI key is missing. Please set your NewsAPI key in the code.")
        return
    if topic:
        url = f'https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&language=en&apiKey={api_key}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])[:5]
        if not articles:
            speak("No news found for that topic.")
            return
        if topic:
            speak(f"Here are the latest news headlines about {topic}:")
        else:
            speak("Here are the top news headlines:")
        for article in articles:
            speak(article['title'])
    except Exception:
        speak("Sorry, I couldn't fetch the news.")

def calculate():
    speak("What calculation should I perform?")
    expr = take_command()
    try:
        result = eval(expr, {"__builtins__": {}})
        speak(f"The result is {result}")
    except Exception as e:
        speak("Sorry, I couldn't perform the calculation.")
        print(f"Error: {e}")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    if CHAT_MODE:
        return input("Command: ").lower()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"User said: {command}")
    except Exception:
        speak("Sorry, I didn't catch that.")
        return "none"
    return command.lower()
