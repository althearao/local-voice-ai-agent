import sounddevice as sd
import numpy as np
from ollama import chat
from fastrtc import get_stt_model, get_tts_model

# Load models
stt_model = get_stt_model(model="moonshine/base")
tts_model = get_tts_model(model="kokoro")

SAMPLE_RATE = 16000


def record_audio():
    print("\n Press ENTER to start recording...")
    input()
    print("Recording... Press ENTER to stop.")

    recording = True
    audio_chunks = []

    def callback(indata, frames, time, status):
        if recording:
            audio_chunks.append(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=callback,
    ):
        input()
        recording = False

    if not audio_chunks:
        return None

    audio = np.concatenate(audio_chunks, axis=0)

    if audio.ndim > 1:
        audio = audio[:, 0]

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    # Convert to int16 for STT
    audio_int16 = (audio * 32767).astype(np.int16)
    audio_int16 = np.expand_dims(audio_int16, axis=0)

    return (SAMPLE_RATE, audio_int16)


def main():
    print("Local Voice Assistant Ready. Say 'exit' to quit.")

    while True:
        audio = record_audio()

        if audio is None:
            continue

        user_text = stt_model.stt(audio)
        print("You:", user_text)

        if not user_text.strip():
            print("Didn't catch that. Try speaking louder.")
            continue

        if user_text.lower() in ["exit", "quit", "stop"]:
            break

        response = chat(
            model="jokebot", #Replace with your local model name
            messages=[{"role": "user", "content": user_text}],
        )

        reply = response["message"]["content"]
        print("Bot:", reply)

        for sample_rate, audio_array in tts_model.stream_tts_sync(reply):
            sd.play(audio_array, samplerate=sample_rate)
            sd.wait()


if __name__ == "__main__":
    main()