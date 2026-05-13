from tts.speaker import stop_speaking

def handle_interrupt():
    print("User interrupted!")

    stop_speaking()