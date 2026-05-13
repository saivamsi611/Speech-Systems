from faster_whisper import WhisperModel
import numpy as np

print("Loading Faster Whisper Model...")

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

print("Faster Whisper Loaded Successfully")

def transcribe(audio_data, sample_rate):

    try:

        # =========================
        # PREPARE AUDIO
        # =========================

        audio_data = audio_data.astype(np.float32)

        audio_data = audio_data.flatten()

        # =========================
        # TRANSCRIBE
        # =========================

        segments, info = model.transcribe(
            audio_data,
            language="en"
        )

        text = ""

        for segment in segments:
            text += segment.text

        return text.strip()

    except Exception as e:

        print(f"Transcription Error: {e}")

        return ""