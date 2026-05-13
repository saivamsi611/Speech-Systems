# Real-Time AI Voice Assistant

A fully local, high-performance Voice Assistant built in Python. It utilizes modern Speech-To-Text (STT) via Faster Whisper and offline Text-To-Speech (TTS) via Pyttsx3, enhanced with intelligent audio-level filtering to run smoothly on standard CPUs without latency lag.

---

## 🚀 Core Features

*   **⚡ Real-Time Faster Whisper (STT):** Leverages `ctranslate2`-based Whisper models for extremely fast, local voice transcription.
*   **🔊 Local Speech Synthesis (TTS):** Instant, offline responses using Windows SAPI5 (`pyttsx3`).
*   **🛡️ Dynamic Noise Gate & Silence Skip:** Automatically analyzes real-time microphone RMS volume levels. Only transcribes audio that exceeds the configurable threshold (`0.015`), bypassing silent background audio entirely and freeing up crucial CPU cycles.
*   **🔕 Self-Echo Suppression:** Intelligent buffer clearing removes any audio captured while the assistant is speaking, eliminating feedback-triggered talking loops.
*   **🖥️ Real-Time Visualizer:** Continuously outputs a live decibel/volume meter in the terminal to allow instant microphone state confirmation.
*   **📦 Resilient Queue Management:** Automatically purges old queued frames if processing falls slightly behind, ensuring the system stays focused on the most recent user commands.

---

## 📁 Repository Architecture

```text
Aivoice/
│
├── app.py                 # Central loop, queue control, volume gating, orchestration
├── requirements.txt       # Python module dependencies
├── audio/
│   ├── recorder.py        # Non-blocking sounddevice microphone stream
│   ├── noise_filter.py    # Optional static noise gate utilities
│   └── vad.py             # Voice Activity Detection templates
├── stt/
│   └── whisper_engine.py  # Faster Whisper model initialization & transcription logic
└── tts/
    └── speaker.py         # Re-engineered offline Pyttsx3 speaker engine
```

---

## 🔧 Installation & Setup

### Prerequisites
*   **Python 3.9+** installed.
*   Valid active microphone and audio-out speakers connected.

### Setup Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/saivamsi611/Speech-Systems.git
   cd Speech-Systems
   ```

2. **Install System Dependencies (Optional/Recommended):**
   *If running on Windows, the `pyttsx3` engine uses built-in SAPI5. For Linux users, ensure you have `espeak` installed:*
   ```bash
   sudo apt-get install espeak  # Linux only
   ```

3. **Install Python Libraries:**
   It is recommended to use a Virtual Environment (`venv`).
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 How to Use

Launch the main script in unbuffered mode to see instant outputs:

```bash
python -u app.py
```

### Interactive Dashboard Example
Upon loading, the terminal actively monitors room noise levels:
```text
Loading Faster Whisper Model...
Faster Whisper Loaded Successfully
Loading AI Voice Assistant...

=====================================================
Assistant Started & Listening!
Ensure your microphone is connected.
Speak something clearly...
=====================================================

Listening... (Mic Volume: 0.0031)  # System waits silently, consuming minimal CPU
[System] Processing speech...
You Said: Hello assistant
Assistant: You said Hello assistant
Ready for next command...
```

### ⚙️ Customization
You can fine-tune the noise threshold directly inside `app.py` to fit your environment:
```python
# Change this value inside app.py
VOLUME_THRESHOLD = 0.015  # Raise if loud environment, lower if you speak softly
```

---

## 🛠️ Recent Optimization History
*   **Fixed SAPI5 Engine Lockups:** Restructured TTS initialization locally within functions to completely prevent Pyttsx3 drivers from locking up or dropping out on Windows platforms.
*   **Integrated RMS Gating:** Solved the infinite backlog problem by filtering silence on-the-fly before engaging CPU-heavy Whisper processing loops.
