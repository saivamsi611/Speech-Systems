import noisereduce as nr
import numpy as np

def reduce_noise(audio_data, sample_rate):
    reduced = nr.reduce_noise(
        y=audio_data.flatten(),
        sr=sample_rate
    )

    return reduced