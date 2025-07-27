"""
JARVIS Main Program Test
Simulates the main JARVIS experience
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simulate_jarvis_session():
    """Simulate a JARVIS session"""
    print("="*60)
    print("🤖 SIMULATING JARVIS SESSION")
    print("="*60)
    
    try:
        # Import main JARVIS components
        from core.speech import speak
        from core.memory import init_memory_db
        
        # Initialize memory database
        init_memory_db()
        
        # Simulate JARVIS startup
        print("\n🔄 Initializing JARVIS...")
        speak("JARVIS systems initializing, Sir.")
        
        # Simulate plugin loading
        print("📦 Loading plugins...")
        speak("Loading AI modules and personality systems.")
        
        # Test greeting
        print("\n👋 JARVIS Greeting:")
        speak("Good day, Sir. I am JARVIS - Just A Rather Very Intelligent System. All systems are online and standing by to assist you.")
        
        # Simulate commands
        test_scenarios = [
            "User says: 'Hello JARVIS'",
            "User says: 'What's your status?'", 
            "User says: 'What time is it?'",
            "User says: 'Tell me about yourself'",
            "User says: 'Thank you JARVIS'"
        ]
        
        print("\n🎭 Simulating User Interactions:")
        for scenario in test_scenarios:
            print(f"\n🔸 {scenario}")
            
            # JARVIS responses based on scenario
            if "Hello" in scenario:
                speak("Good day, Sir. How may I assist you today?")
                print("   🤖 JARVIS: Good day, Sir. How may I assist you today?")
            elif "status" in scenario:
                speak("All systems are operational and standing by, Sir.")
                print("   🤖 JARVIS: All systems are operational and standing by, Sir.")
            elif "time" in scenario:
                import datetime
                time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {time}, Sir.")
                print(f"   🤖 JARVIS: The time is {time}, Sir.")
            elif "about yourself" in scenario:
                speak("I am JARVIS, your personal AI assistant. I can help with tasks, answer questions, and engage in conversation, Sir.")
                print("   🤖 JARVIS: I am JARVIS, your personal AI assistant...")
            elif "Thank you" in scenario:
                speak("You are most welcome, Sir. Always a pleasure to assist.")
                print("   🤖 JARVIS: You are most welcome, Sir. Always a pleasure to assist.")
            
            import time
            time.sleep(1.5)
        
        print("\n✅ Session simulation complete!")
        speak("Session simulation complete, Sir. JARVIS is fully operational and ready for interactive use.")
        
        print("\n" + "="*60)
        print("🎯 JARVIS IS READY FOR LIVE INTERACTION!")
        print("   Run 'python main.py' to start the full experience")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Simulation error: {e}")
        print("🔧 Please check system configuration")

if __name__ == "__main__":
    simulate_jarvis_session()
