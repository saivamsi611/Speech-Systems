# Speech-Systems 🎤

Real-Time AI Speech-to-Text system using Faster Whisper for ultra-low latency transcription.

This project demonstrates how modern AI speech systems work using:
- Faster Whisper
- Live microphone streaming
- Queue-based audio pipelines
- Voice Activity Detection (VAD)
- Multithreading
- Low-latency inference

The application works completely offline after the initial model download.

---

# 🚀 Features

## ✅ Real-Time Speech Recognition
Convert live microphone speech into text in real time.

---

## ✅ Ultra-Low Latency
Optimized for fast streaming transcription using:
- small audio chunks
- queue processing
- multithreading

Approximate latency:
- 200ms–800ms depending on model size and hardware.

---

## ✅ Offline Capability
No internet connection required after downloading the model.

Everything runs locally.

---

## ✅ Faster Whisper Integration
Uses:
- faster-whisper
- ctranslate2

for optimized CPU/GPU inference.

---

## ✅ Voice Activity Detection (VAD)
Filters:
- silence
- pauses
- background noise

for cleaner speech recognition.

---

## ✅ Transcript Saving
Automatically saves all recognized speech into:

```text
transcription.txt
```

---

## ✅ GPU Support
Optional CUDA acceleration for NVIDIA GPUs.

---

# 🛠️ Installation

## Step 1: Clone Repository

```bash
git clone https://github.com/saivamsi611/Speech-Systems.git
cd Speech-Systems
```

---

## Step 2: Create Virtual Environment (Optional)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

---

# 📦 requirements.txt

```txt
faster-whisper
sounddevice
numpy
ctranslate2
av
```

---

# 🎯 Usage

Run the application:

```bash
python app.py
```

---

# 🖥️ Example Output

```text
=== Fast Live Speech-to-Text Started ===

Speak into your microphone...

You said: Hello
You said: This is real time speech recognition
You said: Faster Whisper is working
```

---

# ⚡ Model Options

You can change the model size inside the code.

| Model | Speed | Accuracy |
|---|---|---|
| tiny | Fastest | Basic |
| base | Fast | Good |
| small | Balanced | Better |
| medium | Slower | High |
| large-v3 | Slowest | Best |

---

# ⚡ GPU Acceleration

For NVIDIA GPU users:

```python
stt = FastSpeechToText(
    model_size="base",
    device="cuda",
    compute_type="float16"
)
```

CUDA improves:
- inference speed
- latency
- throughput

---

# 🔧 Optimization Tips

# For Minimum Latency

Use smaller models:

```python
model_size="tiny"
```

Reduce chunk duration:

```python
self.chunk_duration = 1
```

Reduce block size:

```python
blocksize=3200
```

Use int8 inference:

```python
compute_type="int8"
```

---

# For Maximum Accuracy

Use larger models:

```python
model_size="medium"
```

Increase beam size:

```python
beam_size=5
```

Higher beam size:
- improves accuracy
- increases latency

---

# 🧠 How The Pipeline Works

```text
Microphone
    ↓
Audio Callback
    ↓
Audio Buffer
    ↓
Queue
    ↓
Voice Activity Detection
    ↓
Faster Whisper Model
    ↓
Speech Transcription
    ↓
Console Output + Transcript File
```

---

# 📊 Technical Details

| Component | Description |
|---|---|
| Audio Stream | 16kHz mono |
| Processing | Queue-based |
| Concurrency | Multithreading |
| STT Engine | Faster Whisper |
| VAD | Enabled |
| Inference | int8 CPU optimized |

---

# 🧵 Threading Architecture

Two separate threads are used.

## 1. Audio Thread
Handles:
- microphone capture
- audio buffering

---

## 2. Processing Thread
Handles:
- Whisper inference
- transcription generation

This prevents:
- microphone lag
- blocking
- audio overflow

---

# 🔇 Noise Handling

The project uses Voice Activity Detection:

```python
vad_filter=True
```

This helps:
- remove silence
- reduce unwanted audio
- improve transcription quality

---

# 🐛 Troubleshooting

## "No module named faster_whisper"

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## "Could not find microphone"

Check:
- microphone connection
- default input device

Windows:

```text
Settings → Sound → Input
```

---

## High CPU Usage

Solutions:
- use tiny/base model
- use int8 inference
- increase chunk_duration

---

# 📚 Learning Concepts Covered

This project helps understand:

- Real-time AI pipelines
- Speech-to-Text systems
- Whisper architecture
- Audio streaming
- Queue systems
- Multithreading
- Latency optimization
- Voice Activity Detection
- Real-time inference

---

# 🚀 Future Improvements

Possible upgrades:
- Text-to-Speech (TTS)
- AI chatbot integration
- Streaming partial transcription
- WebSocket support
- Speaker diarization
- Noise suppression
- Wake-word detection
- Live subtitle UI
- GPU streaming inference

