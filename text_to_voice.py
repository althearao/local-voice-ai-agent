import sounddevice as sd
import numpy as np
from ollama import chat
from fastrtc import get_tts_model, KokoroTTSOptions

# Load TTS model
tts_model = get_tts_model()  # kokoro

# For different voice, uncomment and modify the options below (next 5 lines)
# options = KokoroTTSOptions(
#     voice="af_nicole",
#     speed=1,
#     lang="en-us"
# )


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
        # Note: To use different voice options, pass the 'options' parameter in stream_tts_sync
        for sample_rate, audio_array in tts_model.stream_tts_sync(response_text):
            sd.play(audio_array, samplerate=sample_rate)
            sd.wait()
            
if __name__ == "__main__":
    main()