# Audio Recognition using Whispher
import openai
import pyaudio
import wave
import base64

# from keys import API_KEY

# Set up OpenAI authentication
openai.api_key = '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'

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024
RECORD_SECONDS = 7
WAVE_OUTPUT_FILENAME = "audio.wav"

# Set up audio input
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK_SIZE)


def Input():
    # Capture audio
    frames = []
    print("Listening...")
    for i in range(0, int(RATE / CHUNK_SIZE * RECORD_SECONDS)):
        data = stream.read(CHUNK_SIZE)
        frames.append(data)

    print("Recording complete.")

    # Save audio to file
    wave_file = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b"".join(frames))
    wave_file.close()

    # Convert audio to text using OpenAI module using the model "Whisper"
    with open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
        audio_content = base64.b64encode(audio_file.read()).decode("utf-8")

    audio_file = open("C:/Users/SaiSrujay/PycharmProjects/pythonProject4/audio.wav", "rb")
    print("Transcripting")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    return transcript['text']
