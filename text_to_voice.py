import sounddevice as sd
import numpy as np
from ollama import chat
from fastrtc import get_tts_model

# Load TTS model
tts_model = get_tts_model()  # kokoro

def main():
    while True:
        user_input = input("You: ")
        if not user_input.strip():
            print("Exiting...")
            break

        # Send input to Ollama
        response = chat(
            model="class_murmur",  # your local model
            messages=[{"role": "user", "content": user_input}]
        )
        response_text = response["message"]["content"]
        print(f"Ollama: {response_text}")

                # Convert text reply to audio and play (fixed)
        for sample_rate, audio_array in tts_model.stream_tts_sync(response_text):
            sd.play(audio_array, samplerate=sample_rate)
            sd.wait()
            
if __name__ == "__main__":
    main()