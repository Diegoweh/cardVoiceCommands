import io
import os
import wave

import numpy as np
import pyaudio
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums, types


class SpeechToText:
    def __init__(self, credentials_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = speech_v1.SpeechClient()

    def record_audio(self, duration=5, filename="recorded_audio.wav", channels=1, rate=44100, chunk=1024, format=pyaudio.paInt16):
        audio = pyaudio.PyAudio()

        stream = audio.open(format=format, channels=channels,
                            rate=rate, input=True,
                            frames_per_buffer=chunk)

        print("Grabando...")
        frames = []

        for i in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        print("Grabación Finalizada")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f"Audio saved as '{filename}'.")        


    def transcribe_audio(self, audio_file_path, language_code='es-ES'):
        with io.open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=language_code,
        )

        response = self.client.recognize(config=config, audio=audio)

        transcripts = []
        for result in response.results:
            transcripts.append(result.alternatives[0].transcript)

        return transcripts
    
    def analyze_audio_for_menu_option(self, audio_file_path, menu_options):
        with io.open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code='es-ES',
        )

        response = self.client.recognize(config=config, audio=audio)

        for result in response.results:
            transcript = result.alternatives[0].transcript.lower()
            for option in menu_options:
                if option in transcript:
                    return option

        return None   
       
    

if __name__ == "__main__":
    credentials_path = "C:/Users/diego/OneDrive/Desktop/librerias/lofty-tea-415604-8ecaca3e531b.json"
    audio_filename = "recorded_audio.wav"

    speech_to_text = SpeechToText(credentials_path)

    # Grabar audio desde el micrófono
    speech_to_text.record_audio(duration=5, filename=audio_filename)    

   
        # Transcribir el audio grabado si el hablante es válido
    transcripts = speech_to_text.transcribe_audio(audio_filename)    

    for transcript in transcripts:
        print("Transcript:", transcript)

         
