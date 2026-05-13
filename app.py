import time
import numpy as np

from audio.recorder import (
    start_recording,
    audio_queue,
    SAMPLE_RATE
)

from stt.whisper_engine import transcribe

# IMPORT WHOLE MODULE
import tts.speaker as speaker

print("Loading AI Voice Assistant...")

# =========================
# START MICROPHONE
# =========================

stream = start_recording()

print("\n=====================================================")
print("Assistant Started & Listening!")
print("Ensure your microphone is connected.")
print("Speak something clearly...")
print("=====================================================\n")

# Configurable Volume Threshold to filter background noise
# (0.015 is a good default; raise it if your environment is loud, lower it if you speak softly)
VOLUME_THRESHOLD = 0.015

try:

    while True:

        # =========================
        # PAUSE WHILE SPEAKING
        # =========================

        if speaker.speaking:
            time.sleep(0.1)
            continue

        # =========================
        # CHECK AUDIO QUEUE
        # =========================

        if not audio_queue.empty():

            # Prevent backlog: if there are multiple chunks queued (e.g., Whisper took too long),
            # discard the oldest chunks to ensure the system stays real-time!
            backlog_size = audio_queue.qsize()
            if backlog_size > 2:
                print(f"\n[System] Slow processing detected ({backlog_size} chunks). Draining queue to keep real-time...")
                while audio_queue.qsize() > 1:
                    try:
                        audio_queue.get_nowait()
                    except:
                        pass

            audio_chunk = audio_queue.get()

            # =========================
            # VOLUME THRESHOLD
            # =========================
            # Calculate RMS amplitude to check if there is actual voice
            rms = np.sqrt(np.mean(audio_chunk**2))
            
            # Print continuous mic volume indicator to help user debug input
            print(f"\rListening... (Mic Volume: {rms:.4f})", end="", flush=True)

            if rms < VOLUME_THRESHOLD:
                # It is silence or low ambient noise, skip transcription entirely!
                continue

            print("\n[System] Processing speech...")

            # =========================
            # SPEECH TO TEXT
            # =========================

            text = transcribe(
                audio_chunk,
                SAMPLE_RATE
            )

            text = text.strip()

            # =========================
            # IGNORE SMALL NOISES
            # =========================

            if len(text) > 2:

                print(f"You Said: {text}")

                # =========================
                # AI RESPONSE
                # =========================

                response = f"You said {text}"

                print(f"Assistant: {response}")

                # =========================
                # TEXT TO SPEECH
                # =========================

                speaker.speak(response)
                
                # =========================
                # PREVENT SELF-ECHO LOOP
                # =========================
                # While speaking, the mic continues to record.
                # Drain the queue entirely to clear out the sound of the Assistant's own voice.
                time.sleep(0.1) # Tiny settle delay
                while not audio_queue.empty():
                    try:
                        audio_queue.get_nowait()
                    except:
                        pass
                
                print("\nReady for next command...")

        # =========================
        # SMALL DELAY
        # =========================

        time.sleep(0.01)

except KeyboardInterrupt:

    print("\nStopping Assistant...")

    stream.stop()