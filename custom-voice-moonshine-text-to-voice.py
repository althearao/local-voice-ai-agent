import sounddevice as sd
import numpy as np
from ollama import chat
from fastrtc import get_stt_model
from TTS.api import TTS

stt_model = get_stt_model(model="moonshine/base")

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

REFERENCE_AUDIO = "reference_voice.wav" # replace with your own reference audio file for voice cloning
MIC_SAMPLE_RATE = 16000
TTS_SAMPLE_RATE = 22050 


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
        samplerate=MIC_SAMPLE_RATE,
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

    # Convert to int16 for Moonshine
    audio_int16 = (audio * 32767).astype(np.int16)
    audio_int16 = np.expand_dims(audio_int16, axis=0)

    return (MIC_SAMPLE_RATE, audio_int16)


def main():
    print(" Custom Voice Assistant Ready.")
    print("Say 'exit' to quit.\n")

    while True:
        audio = record_audio()
        if audio is None:
            continue

        user_text = stt_model.stt(audio)
        print("You:", user_text)

        if not user_text.strip():
            print("Didn't catch that.")
            continue

        if user_text.lower() in ["exit", "quit", "stop"]:
            break

        response = chat(
            model="jokebot",
            messages=[{"role": "user", "content": user_text}],
        )

        reply = response["message"]["content"]

        wav = tts.tts(
            text=reply,
            speaker_wav=REFERENCE_AUDIO,
            language="en",
        )

        sd.play(wav, samplerate=TTS_SAMPLE_RATE)
        print("Bot:", reply)
        sd.wait()


if __name__ == "__main__":
    main()