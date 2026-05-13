import webrtcvad

vad = webrtcvad.Vad(2)

def is_speech(frame, sample_rate=16000):
    return vad.is_speech(frame.tobytes(), sample_rate)