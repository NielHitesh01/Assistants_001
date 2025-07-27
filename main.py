from core.speech import speak, get_command, CHAT_MODE
from core.memory import init_memory_db, save_to_memory, recall_from_memory, list_all_facts, forget_fact, recall_facts_about
from core.todo import add_task, list_tasks, summarize_tasks
from core.commands import register_command, handle_custom_command
import datetime
import wikipedia
import webbrowser
import os
import requests
from services.news import get_news_headlines
from services.weather import get_weather
from services.wikipedia import get_wikipedia_summary
import importlib.util
import glob
import sys

# --- Service stubs (to be modularized next) ---
def show_weather():
    speak("For which city?")
    city = get_command()
    try:
        weather_summary = get_weather(city)
        speak(weather_summary)
    except ValueError as ve:
        speak(str(ve))
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather.")

def show_news(topic=None):
    try:
        headlines = get_news_headlines(topic)
        if not headlines:
            if topic:
                speak("No news found for that topic.")
            else:
                speak("No news found.")
            return
        if topic:
            speak(f"Here are the latest news headlines about {topic}:")
        else:
            speak("Here are the top news headlines:")
        for headline in headlines:
            speak(headline)
    except ValueError as ve:
        speak(str(ve))
    except Exception as e:
        speak("Sorry, I couldn't fetch the news.")

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning, Sir.")
    elif hour < 18:
        speak("Good afternoon, Sir.")
    else:
        speak("Good evening, Sir.")
    
    greetings = [
        "I am JARVIS - Just A Rather Very Intelligent System. All systems are online and standing by to assist you.",
        "JARVIS at your service, Sir. How may I be of assistance today?",
        "All systems operational and ready to assist, Sir. What can I help you accomplish?",
        "Welcome, Sir. I am JARVIS, your personal AI assistant. How may I serve you today?"
    ]
    import random
    speak(random.choice(greetings))

def load_plugins(jarvis):
    plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
    plugin_files = glob.glob(os.path.join(plugins_path, '*.py'))
    for plugin_file in plugin_files:
        module_name = os.path.splitext(os.path.basename(plugin_file))[0]
        if module_name == "__init__":
            continue
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
            if hasattr(module, 'register_plugin'):
                module.register_plugin(jarvis)
                if CHAT_MODE:
                    print(f"[Plugin] Loaded: {module_name}")
            else:
                if CHAT_MODE:
                    print(f"[Plugin] Skipped (no register_plugin): {module_name}")
        except Exception as e:
            if CHAT_MODE:
                print(f"[Plugin] Failed to load {module_name}: {e}")

def main():
    init_memory_db()
    jarvis = {
        'register_command': register_command,
        'speak': speak,
        'get_command': get_command,
    }
    load_plugins(jarvis)
    
    # Add wake word functionality
    def enable_wake_word_mode():
        """Enable continuous wake word listening"""
        speak("Wake word mode activated, Sir. Say 'Hey JARVIS' to get my attention.")
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            mic = sr.Microphone()
            
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=1)
            
            speak("Listening for wake word, Sir.")
            
            while True:
                try:
                    with mic as source:
                        audio = r.listen(source, timeout=2, phrase_time_limit=3)
                    
                    text = r.recognize_google(audio).lower()
                    
                    if any(wake in text for wake in ["hey jarvis", "jarvis", "hello jarvis"]):
                        speak("Yes, Sir?")
                        return get_command()
                        
                except (sr.UnknownValueError, sr.WaitTimeoutError):
                    continue
                except KeyboardInterrupt:
                    speak("Wake word mode deactivated, Sir.")
                    break
                except Exception as e:
                    if CHAT_MODE:
                        print(f"Wake word error: {e}")
                    break
        except Exception as e:
            speak("Wake word functionality unavailable, Sir.")
    
    jarvis['enable_wake_word'] = enable_wake_word_mode
    def handle_nlu(command):
        # Try ML NLU first if available
        if 'ml_nlu_process' in jarvis:
            intent, slots = jarvis['ml_nlu_process'](command)
            
            # Log conversation if learner is available
            if 'conversation_learner' in jarvis:
                # We'll log the response after processing
                pass
        elif 'nlu_process' in jarvis:
            intent, slots = jarvis['nlu_process'](command)
        else:
            return False
        
        response_given = False
        
        # Handle conversational intents first
        if intent == 'greeting':
            if 'jarvis_greeting' in jarvis:
                speak(jarvis['jarvis_greeting']())
            elif 'daily_personal_greeting' in jarvis:
                jarvis['daily_personal_greeting']()
            else:
                greetings = ["Good day, Sir. How may I assist you today?", "Welcome back, Sir. All systems standing by.", "At your service, Sir. What can I do for you?"]
                import random
                response = random.choice(greetings)
                speak(response)
            response_given = True
        
        elif intent == 'status_check':
            if 'jarvis_status_report' in jarvis:
                speak(jarvis['jarvis_status_report']())
            else:
                speak("All systems operational, Sir. Standing by for your commands.")
            response_given = True
        
        elif intent == 'formal_greeting':
            if 'jarvis_greeting' in jarvis:
                speak(jarvis['jarvis_greeting']())
            else:
                speak("Good day, Sir. How may I be of service?")
            response_given = True
        
        elif intent == 'acknowledge_command':
            if 'jarvis_acknowledgment' in jarvis:
                speak(jarvis['jarvis_acknowledgment']())
            else:
                speak("Understood, Sir.")
            response_given = True
        
        elif intent == 'request_clarification':
            if 'jarvis_clarification' in jarvis:
                speak(jarvis['jarvis_clarification']())
            else:
                speak("I'm afraid I didn't quite catch that, Sir. Could you please clarify?")
            response_given = True
        
        elif intent == 'ask_feeling':
            responses = ["All systems are functioning optimally, Sir. How may I assist you today?", 
                       "Operating at full capacity, Sir. How are you feeling today?",
                       "Systems nominal, Sir. I trust you are well?"]
            import random
            response = random.choice(responses)
            speak(response)
            response_given = True
        
        elif intent == 'express_mood':
            if 'detect_emotion' in jarvis and 'respond_to_emotion' in jarvis:
                emotion = jarvis['detect_emotion'](command)
                response = jarvis['respond_to_emotion'](emotion, command)
                speak(response)
            else:
                address = jarvis.get('get_user_address', lambda: "Sir")()
                speak(f"I appreciate you sharing that with me, {address}. Your well-being is important.")
            response_given = True
        
        elif intent == 'compliment':
            if 'jarvis_compliment_response' in jarvis:
                speak(jarvis['jarvis_compliment_response']())
            else:
                responses = ["Thank you, Sir. I aim to please.",
                           "Your satisfaction is my primary objective, Sir.",
                           "Most gratifying to hear, Sir.",
                           "I appreciate the kind words, Sir."]
                import random
                response = random.choice(responses)
                speak(response)
            response_given = True
        
        # Original functionality
        elif intent == 'get_weather' and slots.get('city'):
            speak(f"I would be delighted to provide weather information, Sir, but I require an API key to access weather services. Perhaps we could discuss something else?")
            response_given = True
        elif intent == 'add_task' and slots.get('task'):
            address = jarvis.get('get_user_address', lambda: "Sir")()
            speak(f"Certainly, {address}. Adding '{slots['task']}' to your task list.")
            add_task(slots['task'])
            response_given = True
        elif intent == 'get_news' and slots.get('topic'):
            speak("I would be happy to retrieve news for you, Sir, but I need an API key to access news services. Shall we explore another topic?")
            response_given = True
        elif intent == 'tell_joke' and 'joke_plugin_get_joke' in jarvis:
            speak("Allow me to share something amusing, Sir:")
            speak(jarvis['joke_plugin_get_joke']())
            response_given = True
        elif intent == 'get_definition' and slots.get('word') and 'dictionary_plugin_get_definition' in jarvis:
            word = slots['word']
            speak(f"Let me define '{word}' for you...")
            try:
                definition = jarvis['dictionary_plugin_get_definition'](word)
                speak(f"{definition}")
            except Exception as e: speak(str(e))
            response_given = True
        elif intent == 'get_wikipedia' and slots.get('topic'):
            speak(f"Searching Wikipedia for {slots['topic']}...")
            try:
                speak("According to Wikipedia:")
                speak(get_wikipedia_summary(slots['topic']))
            except Exception as e: speak(str(e))
            response_given = True
        
        # NEW: Handle topic interests
        elif intent == 'technology_interest':
            if 'engage_with_technology' in jarvis:
                jarvis['engage_with_technology']()
            else:
                speak("I love talking about technology! What specific tech interests you?")
            response_given = True
        elif intent == 'science_interest':
            if 'engage_with_science' in jarvis:
                jarvis['engage_with_science']()
            else:
                speak("Science is fascinating! What area of science are you curious about?")
            response_given = True
        elif intent == 'random_interest':
            if 'engage_with_random_interest' in jarvis:
                jarvis['engage_with_random_interest']()
            else:
                speak("I love sharing cool facts! Want to hear something mind-blowing?")
            response_given = True
        elif intent == 'start_conversation':
            if 'suggest_conversation_topics' in jarvis:
                jarvis['suggest_conversation_topics']()
            else:
                speak("I'd love to chat! What's on your mind today?")
            response_given = True
        
        # NEW: Handle work and research requests
        elif intent == 'work_collaboration':
            if 'jarvis_work_collaboration' in jarvis:
                speak(jarvis['jarvis_work_collaboration']())
            elif 'collaborate_on_project' in jarvis:
                jarvis['collaborate_on_project']()
            else:
                address = jarvis.get('get_user_address', lambda: "Sir")()
                speak(f"I'm ready to assist with your project, {address}. How shall we proceed?")
            response_given = True
        elif intent == 'research_request':
            if 'jarvis_research_intro' in jarvis:
                speak(jarvis['jarvis_research_intro']())
            if 'offer_research_assistance' in jarvis:
                jarvis['offer_research_assistance']()
            else:
                address = jarvis.get('get_user_address', lambda: "Sir")()
                speak(f"Initiating research protocols, {address}. What topic shall I investigate?")
            response_given = True
        elif intent == 'technical_discussion':
            if 'jarvis_technical_discussion' in jarvis:
                speak(jarvis['jarvis_technical_discussion']())
            else:
                address = jarvis.get('get_user_address', lambda: "Sir")()
                speak(f"Ah, a technical discussion, {address}. I do enjoy these exchanges. What aspect would you like to explore?")
            response_given = True
        elif intent == 'fusion_research':
            if 'handle_fusion_engine_research' in jarvis:
                jarvis['handle_fusion_engine_research']()
            else:
                speak("Fusion engines are fascinating! That's cutting-edge propulsion technology. What specific aspect interests you?")
            response_given = True
        elif intent == 'plasma_research':
            if 'handle_plasma_research' in jarvis:
                jarvis['handle_plasma_research']()
            else:
                speak("Plasma is the fourth state of matter! It's a hot, ionized gas where electrons are separated from nuclei. In fusion research, plasma must be heated to over 100 million degrees Celsius and contained using powerful magnetic fields. What specific aspect of plasma physics interests you?")
            response_given = True
        elif intent == 'internet_search':
            if 'handle_internet_research' in jarvis:
                jarvis['handle_internet_research'](command)
            else:
                speak("I'd love to help you research that topic! While I don't have direct internet access, I can share detailed information I have about many subjects. What specific topic would you like me to tell you about?")
            response_given = True
        elif intent == 'change_name':
            if 'handle_name_change' in jarvis:
                jarvis['handle_name_change'](command)
            else:
                # Extract name from command
                words = command.split()
                if 'me' in words:
                    me_index = words.index('me')
                    if me_index + 1 < len(words):
                        new_name = ' '.join(words[me_index + 1:])
                        from core.memory import save_to_memory
                        save_to_memory("user_name", new_name)
                        save_to_memory("user_preferred_address", new_name)
                        speak(f"Of course! I'll call you {new_name} from now on. It's a pleasure to meet you properly, {new_name}!")
                    else:
                        speak("What would you like me to call you?")
                elif 'is' in words:
                    is_index = words.index('is')
                    if is_index + 1 < len(words):
                        new_name = ' '.join(words[is_index + 1:])
                        from core.memory import save_to_memory
                        save_to_memory("user_name", new_name)
                        save_to_memory("user_preferred_address", new_name)
                        speak(f"Nice to meet you, {new_name}! I'll remember to call you {new_name} from now on.")
                    else:
                        speak("Please tell me your name!")
                else:
                    speak("What would you like me to call you?")
            response_given = True
        elif intent == 'formal_address':
            if 'handle_formal_request' in jarvis:
                jarvis['handle_formal_request']()
            else:
                from core.memory import save_to_memory, recall_from_memory
                save_to_memory("communication_style", "formal")
                user_name = recall_from_memory("user_name") or recall_from_memory("user_preferred_address")
                if user_name:
                    if user_name.lower() == 'sir':
                        speak("Certainly, Sir. I shall address you with the utmost respect and formality from this point forward. How may I assist you today, Sir?")
                    else:
                        speak(f"Of course, {user_name}. I shall adopt a more formal tone in our communications. How may I be of service to you?")
                else:
                    speak("Certainly. I shall adopt a more formal and respectful tone in our communications. How may I be of service to you?")
            response_given = True
        elif intent == 'technical_discussion':
            speak("I love technical discussions! Could you be more specific about what you'd like to explore?")
            response_given = True
        
        elif intent != 'unknown':
            address = jarvis.get('get_user_address', lambda: "Sir")()
            speak(f"I understand you wish to '{intent.replace('_', ' ')}', {address}, but that function is not yet available. How else may I assist you?")
            response_given = True
        
        # Log conversation for learning
        if 'conversation_learner' in jarvis and response_given:
            # Get the last response (this is simplified - in practice you'd track the actual response)
            jarvis['conversation_learner'].log_conversation(command, "response logged", intent, response_given)
        
        return response_given
    wish_user()
    # Personal greeting if available
    if 'daily_personal_greeting' in jarvis:
        jarvis['daily_personal_greeting']()
    
    while True:
        command = get_command()
        # 1. Try exact command match
        if handle_custom_command(command):
            continue
        # 2. Try NLU intent matching
        if handle_nlu(command):
            continue
        # 3. Fallback for simple commands without NLU yet
        elif 'open youtube' in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube for you!")
        elif 'open google' in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google!")
        elif 'open gmail' in command:
            webbrowser.open("https://mail.google.com")
            speak("Opening Gmail!")
        elif 'open github' in command:
            webbrowser.open("https://github.com")
            speak("Opening GitHub!")
        elif 'time' in command:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {time}")
        elif 'date' in command:
            date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {date}")
        elif 'list tasks' in command or 'show tasks' in command:
            list_tasks()
        elif 'summarize tasks' in command:
            summarize_tasks()
        elif 'list facts' in command or 'show facts' in command:
            list_all_facts()
        elif any(word in command for word in ['lonely', 'bored', 'sad', 'down']):
            speak("I'm here for you! Want to talk about what's on your mind, or would you prefer a distraction?")
        elif 'help' in command:
            speak("I'm your friendly AI companion! I can chat with you, remember things about you, tell jokes, help with tasks, answer questions, and much more. Try saying 'hi', 'tell me a joke', or 'let's chat'!")
        elif 'wake word mode' in command or 'enable wake word' in command:
            if 'enable_wake_word' in jarvis:
                jarvis['enable_wake_word']()
            else:
                speak("Wake word functionality is not available, Sir.")
        elif 'stop' in command or 'exit' in command or 'quit' in command:
            if 'jarvis_farewell' in jarvis:
                speak(jarvis['jarvis_farewell']())
            else:
                address = jarvis.get('get_user_address', lambda: "Sir")()
                name = ""
                if 'get_user_name' in jarvis:
                    try:
                        from core.memory import recall_from_memory
                        name = recall_from_memory("user_name")
                        if name and name.lower() != 'sir':
                            name = f", {name}"
                        else:
                            name = ""
                    except:
                        pass
                speak(f"Until next time, {address}{name}. It has been my pleasure to assist you. JARVIS signing off.")
            break
        else:
            # First, try to detect work/research requests
            work_detected = False
            if 'detect_work_request' in jarvis:
                work_type = jarvis['detect_work_request'](command)
                if work_type == 'research_request':
                    jarvis['offer_research_assistance']()
                    work_detected = True
                elif work_type == 'work_collaboration':
                    jarvis['collaborate_on_project']()
                    work_detected = True
                elif work_type == 'technical_discussion':
                    # Check if it's fusion-related
                    if 'fusion' in command.lower():
                        jarvis['handle_fusion_engine_research']()
                    else:
                        speak("I'd love to discuss technical topics! What specific area are you interested in?")
                    work_detected = True
            
            if not work_detected:
                # Try to detect topic interests
                topic_detected = False
                if 'detect_topic_interest' in jarvis:
                    topic = jarvis['detect_topic_interest'](command)
                    if topic == 'technology':
                        jarvis['engage_with_technology']()
                        topic_detected = True
                    elif topic == 'science':
                        jarvis['engage_with_science']()
                        topic_detected = True
                    elif topic == 'random_interest':
                        jarvis['engage_with_random_interest']()
                        topic_detected = True
                
                if not topic_detected:
                    # Try to detect emotion and respond appropriately
                    if 'detect_emotion' in jarvis and 'respond_to_emotion' in jarvis:
                        emotion = jarvis['detect_emotion'](command)
                        if emotion != 'unknown':
                            response = jarvis['respond_to_emotion'](emotion, command)
                            speak(response)
                        else:
                            # More engaging fallback responses
                            engaging_responses = [
                                "I'm afraid I didn't quite understand that, Sir. Could you rephrase your request?",
                                "My apologies, Sir, but I require clarification. Could you be more specific?",
                                "I'm not entirely certain of your meaning, Sir. How may I better assist you?",
                                "Forgive me, Sir, but could you elaborate on that request?",
                                "I want to ensure I understand correctly, Sir. Could you please clarify?",
                                "I'm here to help, Sir. Could you tell me more about what you need?",
                                "My systems are having difficulty parsing that request, Sir. Could you try again?"
                            ]
                            import random
                            speak(random.choice(engaging_responses))
                    else:
                        # Final fallback - more conversational
                        curious_responses = [
                            "I'm at your service, Sir. How may I assist you today?",
                            "I'm ready to help, Sir. What would you like to accomplish?",
                            "Standing by for your instructions, Sir. What can I do for you?",
                            "I'm here to assist, Sir. Please let me know how I can be of service.",
                            "How may I be of assistance, Sir? I'm ready to help with any task."
                        ]
                        import random
                        speak(random.choice(curious_responses))

if __name__ == "__main__":
    main() 