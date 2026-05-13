import pyttsx3

speaking = False

def speak(text):

    global speaking

    try:

        speaking = True

        # Initialize the engine locally inside the call to prevent persistent COM issues on Windows
        engine = pyttsx3.init()
        
        # Explicitly set properties
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0) # Ensure volume is maximum

        engine.say(text)

        engine.runAndWait()
        
        # Properly release Resources
        del engine

    except Exception as e:

        print(f"TTS Error: {e}")

    finally:

        speaking = False


def stop_speaking():

    global speaking

    speaking = False