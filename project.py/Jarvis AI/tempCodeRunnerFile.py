import speech_recognition as sr
import asyncio
import edge_tts
import pyjokes
import webbrowser
import sympy as sp
from llama_cpp import Llama
import time
import re
import os
import playsound

# === Global Config ===
VOICE_NAME = "en-IN-AaravNeural"  # You can change to "en-US-GuyNeural" or others

# === Speak Function using edge-tts ===
async def speak_async(text):
    """Asynchronous text-to-speech using Edge TTS."""
    if not text:
        return
    print(f"🗣️ JARVIS: {text}")
    try:
        file = "voice_output.mp3"
        tts = edge_tts.Communicate(text, VOICE_NAME)
        await tts.save(file)
        playsound.playsound(file)
        os.remove(file)
        time.sleep(0.3)
    except Exception as e:
        print(f"❌ TTS error: {e}")

def speak(text):
    """Synchronous wrapper for async TTS."""
    asyncio.run(speak_async(text))

# === Initialize Speech Recognizer ===
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.pause_threshold = 0.8
recognizer.dynamic_energy_threshold = True

# === Load Gemma Model ===
model_path = r"C:\Users\Krish Sharma\.lmstudio\models\MaziyarPanahi\gemma-2-2b-it-GGUF\gemma-2-2b-it.Q5_K_S.gguf"
llm = None
try:
    llm = Llama(model_path=model_path, n_ctx=2048, verbose=False)
    print("✅ Gemma model loaded successfully")
except Exception as e:
    print(f"❌ Error loading Gemma model: {e}")
    print("ℹ️ Continuing without Gemma functionality")

# === Math Solver ===
def solve_math_expression(expression):
    try:
        expression = expression.lower()
        for kw in ['calculate', 'compute', 'what is', 'solve', 'math', 'mathematics', 'how much is']:
            expression = expression.replace(kw, '')
        expression = expression.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('x', '*')
        expression = expression.replace('divided by', '/').replace('divide by', '/')
        expression = expression.replace('to the power of', '**').replace('power', '**')
        expression = re.sub(r'[^\d\+\-\*\/\.\(\)\s]', '', expression).strip()
        if not expression:
            return None
        print(f"🧮 Solving math: {expression}")
        result = sp.simplify(sp.sympify(expression))
        return str(result)
    except Exception as e:
        print(f"❌ Math error: {e}")
        return None

# === Ask Gemma ===
def ask_gemma(question):
    if llm is None:
        speak("Gemma model is not available")
        return
    print(f"❓ USER QUESTION: {question}")
    try:
        prompt = f"Q: {question}\nA:"
        output = llm(prompt=prompt, max_tokens=150, stop=["\n\n", "Q:"], echo=False)
        response = output["choices"][0]["text"].strip()
        if response.startswith("A:"):
            response = response[2:].strip()
        if len(response) > 200:
            response = response[:200] + "..."
        speak(response)
    except Exception as e:
        print(f"❌ Gemma error: {e}")
        speak("Sorry, I encountered an error while processing your question")

# === Listen for Command ===
def listen_for_command(timeout=8, prompt_listening=False):
    with sr.Microphone() as source:
        try:
            if prompt_listening:
                speak("Listening for your command")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=6)
            command = recognizer.recognize_google(audio).lower()
            print(f"👤 USER: {command}")
            return command
        except sr.WaitTimeoutError:
            speak("I didn't hear anything")
            return None
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that")
            return None
        except Exception as e:
            print(f"❌ Listening error: {e}")
            return None

# === Command Handler ===
def handle_command(text):
    if not text:
        return False
    text = text.lower()
    print(f"🔧 Processing command: {text}")

    # Exit
    if any(w in text for w in ["stop", "exit", "quit", "goodbye", "shut down"]):
        speak("Goodbye sir! Jarvis signing off")
        return True

    # Math
    if any(k in text for k in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided', 'calculate', 'what is']):
        result = solve_math_expression(text)
        if result:
            speak(f"The result is {result}")
            return False

    # Jokes
    if any(w in text for w in ["joke", "funny", "make me laugh"]):
        joke = pyjokes.get_joke()
        speak(joke)
        return False

    # Websites
    if "youtube" in text:
        speak("Opening YouTube for you sir")
        webbrowser.open("https://www.youtube.com")
    elif "linkedin" in text:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif "google" in text:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    # Greetings
    elif any(w in text for w in ["hello", "hi", "hey"]):
        speak("Hello sir! Jarvis at your service. How can I assist you today?")
    elif "how are you" in text:
        speak("I'm functioning perfectly sir! Ready to assist you with whatever you need")

    # Time & Date
    elif "time" in text:
        speak(f"The current time is {time.strftime('%I:%M %p')}")
    elif "date" in text:
        speak(f"Today is {time.strftime('%A, %B %d, %Y')}")

    # Help
    elif any(w in text for w in ["help", "capabilities", "what can you do"]):
        speak("I can solve math problems, tell jokes, open websites, and answer your questions using Gemma. I'm your personal assistant Jarvis.")

    # Thank you
    elif any(w in text for w in ["thank", "thanks"]):
        speak("You're welcome sir! Always happy to help")

    else:
        # Fallback to Gemma AI
        speak("Let me think about that for you sir")
        ask_gemma(text)

    return False

# === Continuous Conversation ===
def continuous_conversation():
    speak("I'm listening sir. What can I help you with?")
    while True:
        command = listen_for_command(timeout=10, prompt_listening=True)
        if command:
            if handle_command(command):
                return True
            speak("Is there anything else I can help you with sir?")
        else:
            speak("Are you still there sir? Say stop if you're done, or give me another command")
            response = listen_for_command(timeout=5)
            if response and any(w in response for w in ["stop", "exit", "quit", "no", "that's all"]):
                speak("Okay sir, going back to sleep. Say Jarvis when you need me")
                return False
            elif response:
                if handle_command(response):
                    return True

# === Main Loop ===
def main():
    speak("Jarvis is now online and fully operational. Say Jarvis to begin")
    activation_word = "jarvis"
    while True:
        try:
            with sr.Microphone() as source:
                print("👂 Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                try:
                    speech = recognizer.recognize_google(audio).lower()
                    print(f"👤 USER: {speech}")
                    if activation_word in speech:
                        speak("Yes sir? Jarvis ready for your command")
                        if continuous_conversation():
                            break
                except sr.UnknownValueError:
                    continue
        except sr.WaitTimeoutError:
            continue
        except KeyboardInterrupt:
            speak("Jarvis shutting down. Goodbye sir!")
            break
        except Exception as e:
            print(f"🔴 Main loop error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
