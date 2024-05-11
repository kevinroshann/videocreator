import pyttsx3
import wave
def text_to_audio(text, output_file, rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # Adjust the rate (words per minute)
    engine.save_to_file(text, output_file)
    engine.runAndWait()

text = "{}"
output_file = "{}.wav"  # Use .wav format for pyttsx3
text_to_audio(text, output_file, rate=150)  # Adjust the rate as needed (100 is slower)


def get_audio_duration(file_path):
    with wave.open(file_path, 'rb') as audio_file:
        frames = audio_file.getnframes()
        rate = audio_file.getframerate()
        duration = frames / float(rate)
        return duration

file_path = "{}.wav"  # Replace with your audio file path
duration = get_audio_duration(file_path)
# print(f"Audio duration: {duration} seconds")
