import speech_recognition as sr
import pyttsx3
import pyjokes
import webbrowser
import sympy as sp
from llama_cpp import Llama
import time
import re
import threading

# === Initialize speech engine with robust setup ===
def initialize_speech_engine():
    engine = pyttsx3.init()
    
    # Configure engine properties
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)  # Use first available voice
    
    engine.setProperty('rate', 180)  # Speaking speed
    engine.setProperty('volume', 1.0)  # Maximum volume
    
    # Test the engine
    try:
        engine.say(" ")
        engine.runAndWait()
        engine.say("✅ Speech engine initialized successfully")
        return engine
    except Exception as e:
        print(f"❌ Speech engine error: {e}")
        # Try alternative initialization
        try:
            engine = pyttsx3.init(driverName='sapi5')
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 1.0)
            print("✅ Speech engine reinitialized with sapi5")
            return engine
        except:
            print("❌ Failed to initialize speech engine")
            return None

# Initialize speech engine
engine = initialize_speech_engine()

# === Initialize speech recognizer ===
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.pause_threshold = 0.8
recognizer.dynamic_energy_threshold = True

# === Load Gemma model ===
model_path = r"C:\Users\Krish Sharma\.lmstudio\models\MaziyarPanahi\gemma-2-2b-it-GGUF\gemma-2-2b-it.Q5_K_S.gguf"
llm = None
try:
    llm = Llama(model_path=model_path, n_ctx=2048, verbose=False)
    print("✅ Gemma model loaded successfully")
except Exception as e:
    print(f"❌ Error loading Gemma model: {e}")
    print("ℹ️ Continuing without Gemma functionality")

# === Robust Speak Function ===
def speak(text, wait=True):
    """
    Robust text-to-speech function with error handling and confirmation
    """
    if not engine:
        print(f"❌ SPEECH ENGINE NOT AVAILABLE: {text}")
        return
        
    if not text or text.strip() == "":
        return
        
    print(f"🗣️ JARVIS: {text}")
    
    try:
        # Clear any pending speech
        engine.stop()
        
        # Speak the text
        engine.say(text)
        
        if wait:
            engine.runAndWait()
            print("✅ Speech completed")
        else:
            # Run in thread for non-blocking speech
            def speak_thread():
                try:
                    engine.runAndWait()
                    print("✅ Speech completed")
                except Exception as e:
                    print(f"❌ Speech thread error: {e}")
            
            thread = threading.Thread(target=speak_thread)
            thread.daemon = True
            thread.start()
            
    except RuntimeError:
        # Engine might be busy, try again
        try:
            time.sleep(0.1)
            engine.say(text)
            engine.runAndWait()
            print("✅ Speech completed after retry")
        except Exception as e:
            print(f"❌ Speech error after retry: {e}")
    except Exception as e:
        print(f"❌ Speech error: {e}")

# === Test Speech Function ===
def test_speech():
    """Test if speech is working"""
    print("🔊 Testing speech synthesis...")
    test_phrases = [
        "Hello sir, Jarvis is ready",
        "Testing one two three",
        "Speech system is working"
    ]
    
    for phrase in test_phrases:
        print(f"Testing: {phrase}")
        speak(phrase)
        time.sleep(1)

# === Solve Math ===
def solve_math_expression(expression):
    try:
        # Clean the expression
        expression = expression.lower()
        # Remove common voice command words
        math_keywords = ['calculate', 'compute', 'what is', 'solve', 'math', 'mathematics', 'how much is']
        for keyword in math_keywords:
            expression = expression.replace(keyword, '')
        
        # Replace words with operators
        expression = expression.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('x', '*')
        expression = expression.replace('divided by', '/').replace('divide by', '/')
        expression = expression.replace('to the power of', '**').replace('power', '**')
        
        # Remove non-math characters
        expression = re.sub(r'[^\d\+\-\*\/\.\(\)\s]', '', expression).strip()
        
        if not expression:
            return None
            
        print(f"🧮 Solving math: {expression}")
        expr = sp.sympify(expression)
        result = sp.simplify(expr)
        return str(result)
    except Exception as e:
        print(f"❌ Math solving error: {e}")
        return None

# === Ask Gemma ===
def ask_gemma(question):
    if llm is None:
        speak("Gemma model is not available. Please check the model path.")
        return
        
    print(f"❓ USER QUESTION: {question}")
    try:
        # Simple prompt format
        prompt = f"Q: {question}\nA:"
        output = llm(prompt=prompt, max_tokens=150, stop=["\n\n", "Q:"], echo=False)
        response = output["choices"][0]["text"].strip()
        
        # Clean response
        if response.startswith("A:"):
            response = response[2:].strip()
        
        engine.say(f"🤖 GEMMA: {response}")
        
        # Limit response length for speech
        if len(response) > 200:
            short_response = response[:200] + "..."
            speak(short_response)
        else:
            speak(response)
        
    except Exception as e:
        error_msg = f"Error asking Gemma: {e}"
        print(error_msg)
        speak("Sorry, I encountered an error while processing your question.")

# === Listen for command ===
def listen_for_command(timeout=8, prompt_listening=False):
    with sr.Microphone() as source:
        try:
            if prompt_listening:
                print("🎤 Listening for your command...")
            else:
                engine.say("🎤 Listening sir...")
                
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=6)
            command = recognizer.recognize_google(audio).lower()
            print(f"📝 Heard: {command}")
            return command
        except sr.WaitTimeoutError:
            if prompt_listening:
                print("⏰ No command detected")
                speak("I didn't hear anything.")
            return None
        except sr.UnknownValueError:
            if prompt_listening:
                print("❓ Could not understand audio")
                speak("Sorry, I didn't catch that.")
            return None
        except Exception as e:
            print(f"❌ Listening error: {e}")
            return None

# === Command handler ===
def handle_command(text):
    if not text:
        return False
        
    text = text.lower()
    print(f"🔧 Processing command: {text}")

    # Check for exit commands first
    if any(word in text for word in ["stop", "exit", "quit", "goodbye", "shut down"]):
        speak("Goodbye sir! Jarvis signing off.")
        return True  # Signal to exit

    # Check for math expressions
    math_indicators = ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided by', 'calculate', 'compute', 'what is', 'how much is']
    if any(indicator in text for indicator in math_indicators):
        result = solve_math_expression(text)
        if result:
            speak(f"The result is {result}")
            return False

    # Handle specific commands
    if any(word in text for word in ["joke", "funny", "make me laugh"]):
        joke = pyjokes.get_joke()
        print(f"😂 {joke}")
        speak(joke)

    elif any(word in text for word in ["sing", "song", "music"]):
        speak("Here's a little tune for you! Dum dum da da... I'm your helpful assistant Jarvis!")

    elif "youtube" in text:
        speak("Opening YouTube for you sir")
        webbrowser.open("https://www.youtube.com")

    elif "linkedin" in text:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    elif "google" in text:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif any(word in text for word in ["what can you do", "help", "capabilities"]):
        speak("I can solve math problems, tell jokes, open websites like YouTube and Google, and answer your questions using AI. I'm your personal assistant Jarvis!")

    elif any(word in text for word in ["thank", "thanks"]):
        speak("You're welcome sir! Always happy to help.")

    elif any(word in text for word in ["hello", "hi", "hey"]):
        speak("Hello sir! Jarvis at your service. How can I assist you today?")

    elif any(word in text for word in ["how are you", "how you doing"]):
        speak("I'm functioning perfectly sir! Ready to assist you with whatever you need.")

    elif "time" in text:
        current_time = time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "date" in text:
        current_date = time.strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}")

    else:
        # For any other query, try using Gemma
        if llm is not None:
            speak("Let me think about that for you sir.")
            ask_gemma(text)
        else:
            speak(f"You said: {text}. I can help with math, jokes, opening websites, or answering questions.")
    
    return False  # Continue conversation

# === Continuous Conversation Mode ===
def continuous_conversation():
    """After wake word, stay in conversation mode until user says to stop"""
    speak("I'm listening sir. What can I help you with?")
    conversation_active = True
    
    while conversation_active:
        # Listen for command in conversation mode
        command = listen_for_command(timeout=10, prompt_listening=True)
        
        if command:
            # Handle the command and check if we should exit
            should_exit = handle_command(command)
            if should_exit:
                return True  # Exit completely
            
            # After handling command, ask if user needs more help
            time.sleep(0.5)  # Small pause before next prompt
            speak("Is there anything else I can help you with sir?")
        else:
            # If no command after prompt, ask if user is done
            speak("Are you still there sir? Say stop if you're done, or give me another command.")
            response = listen_for_command(timeout=5)
            if response and any(word in response for word in ["stop", "exit", "quit", "no", "that's all"]):
                speak("Okay sir, going back to sleep. Say Jarvis when you need me.")
                return False
            elif response:
                # Handle the new command
                should_exit = handle_command(response)
                if should_exit:
                    return True

# === Main Loop ===
def main():
    # Test speech first
    if engine:
        test_speech()
    else:
        print("❌ Cannot start without speech engine")
        return
        
    speak("Jarvis is now online and fully operational. Say Jarvis to begin.")
    print("🔊 System ready. Say 'Jarvis' to activate...")
    
    activation_word = "jarvis"
    
    while True:
        try:
            # Listen for activation word
            with sr.Microphone() as source:
                print("👂 Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                
                try:
                    speech = recognizer.recognize_google(audio).lower()
                    print(f"👂 Heard: {speech}")
                    
                    if activation_word in speech:
                        speak("Yes sir? Jarvis ready for your command.")
                        
                        # Enter continuous conversation mode
                        should_exit = continuous_conversation()
                        if should_exit:
                            break
                            
                except sr.UnknownValueError:
                    # No understandable speech, continue listening
                    continue
                    
        except sr.WaitTimeoutError:
            # No speech detected, continue listening
            continue
        except KeyboardInterrupt:
            speak("Jarvis shutting down. Goodbye sir!")
            break
        except Exception as e:
            print(f"🔴 Main loop error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()