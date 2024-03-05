import os
import pyaudio
import wave
import json

# Record audio using PyAudio
def record_audio(file_name, duration=15):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    print("Recording...")

    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio to WAV file in the "Recordings" folder
    directory = "Recordings"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

# Convert audio to JSON
def audio_to_json(file_name):
    directory = "Recordings"
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # Create a dictionary to store audio data
    audio_dict = {
        'sample_rate': 44100,
        'channels': 1,
        'audio_data': audio_data.hex()
    }

    # Convert dictionary to JSON
    json_data = json.dumps(audio_dict)

    # Save JSON data to a file
    json_file_name = os.path.splitext(file_name)[0] + '.json'
    json_file_path = os.path.join(directory, json_file_name)
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_data)

# Example usage
record_audio('audio.wav')
audio_to_json('audio.wav')
