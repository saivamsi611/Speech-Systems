import sounddevice as sd
import queue

# =========================
# AUDIO SETTINGS
# =========================

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 2

audio_queue = queue.Queue()

# =========================
# AUDIO CALLBACK
# =========================

def callback(indata, frames, time, status):

    if status:
        print(status)

    audio_queue.put(indata.copy())

# =========================
# START RECORDING
# =========================

def start_recording():

    stream = sd.InputStream(

        samplerate=SAMPLE_RATE,

        channels=CHANNELS,

        dtype='float32',

        callback=callback,

        blocksize=int(
            SAMPLE_RATE * CHUNK_DURATION
        )
    )

    stream.start()

    return stream