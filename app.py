

import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import queue
import threading
import sys

class FastSpeechToText:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        print(f"Loading {model_size} model... This may take a moment.")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("Model loaded successfully!")
        
        # Audio settings
        self.sample_rate = 16000  # Whisper expects 16kHz
        self.chunk_duration = 3  # Process every 3 seconds
        self.audio_queue = queue.Queue()
        self.is_running = False
        
        # Buffer for audio
        self.audio_buffer = []
        
        # Transcription settings
        self.transcript_file = "transcription.txt"
        with open(self.transcript_file, "w") as f:
            f.write("")  # Clear file on startup
        print(f"Transcription will be saved to: {self.transcript_file}")
        
    def audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        if status:
            print(f"Audio status: {status}", file=sys.stderr)
        
        # Convert to mono and append to buffer
        audio_chunk = indata[:, 0].copy()
        self.audio_buffer.extend(audio_chunk)
        
        # If buffer has enough data, queue it for processing
        samples_needed = int(self.chunk_duration * self.sample_rate)
        if len(self.audio_buffer) >= samples_needed:
            audio_data = np.array(self.audio_buffer[:samples_needed], dtype=np.float32)
            self.audio_queue.put(audio_data)
            self.audio_buffer = self.audio_buffer[samples_needed:]
    
    def process_audio(self):
        """Process audio from queue"""
        while self.is_running:
            try:
                audio_data = self.audio_queue.get(timeout=1)
                

                # Transcribe with faster-whisper
                # Use keywords for context instead of a full sentence to prevent the model from repeating it
                initial_prompt = "live captioning, conversation, accurate, English, clear_speech, no_hallucinations, AI, machine_learning, sequence-to-sequence, Whisper, token, context"
                
                segments, info = self.model.transcribe(
                    audio_data,
                    beam_size=5, # Higher accuracy
                    language="en",
                    initial_prompt=initial_prompt,
                    condition_on_previous_text=False, # distinct chunks, prevents looping
                    vad_filter=True,
                    vad_parameters=dict(
                        threshold=0.5,
                        min_speech_duration_ms=250,
                        min_silence_duration_ms=500
                    )
                )
                
                # Print results
                text_parts = []
                for segment in segments:
                    text_parts.append(segment.text.strip())
                
                if text_parts:
                    full_text = " ".join(text_parts)
                    
                    # Filter out hallucinations (if it repeats the prompt or previous text)
                    if full_text and len(full_text) > 2:
                        # Check if it's just repeating keywords from our prompt
                        if "live captioning" in full_text.lower() and "conversation" in full_text.lower():
                            continue
                            
                        print(f"You said: {full_text}")
                        sys.stdout.flush()
                        
                        # Save to file
                        with open(self.transcript_file, "a") as f:
                            f.write(full_text + " ")
                        
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing audio: {e}", file=sys.stderr)
    
    def start(self):
        """Start live speech recognition"""
        self.is_running = True
        
        # Start processing thread
        processing_thread = threading.Thread(target=self.process_audio)
        processing_thread.daemon = True
        processing_thread.start()
        
        print("\n=== Fast Live Speech-to-Text Started ===")
        print(f"Using model: faster-whisper (small)")
        print(f"Sample rate: {self.sample_rate} Hz")
        print(f"Processing chunks: {self.chunk_duration} seconds")
        print("\nSpeak into your microphone. Press Ctrl+C to stop.\n")
        
        try:
            # Start audio stream
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=self.audio_callback,
                blocksize=int(self.sample_rate * 0.2)  # 200ms blocks (prevents overflow)
            ):
                while self.is_running:
                    threading.Event().wait(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop speech recognition"""
        print("\n\nStopping speech recognition...")
        self.is_running = False
        print("Stopped.")

if __name__ == "__main__":
    # Options: tiny (fastest), base, small, medium, large-v3 (most accurate)
    # For minimum latency, use "tiny" or "base"
    # Switched to 'small' for better accuracy with technical terms
    stt = FastSpeechToText(model_size="small", device="cpu", compute_type="int8")
    stt.start()
