import os

import librosa
import numpy as np


class VoiceVerification:
    def __init__(self, audio_data_dir):
        self.audio_data_dir = audio_data_dir
        self.reference_audio = None
        self.reference_features = None
        self.load_reference_audio()

    def load_reference_audio(self):
        reference_audio_path = os.path.join(self.audio_data_dir, 'C:/Users/diego/OneDrive/Desktop/Projects/Python Proyects/UadeO/1er B/recorded_audio.wav')
        self.reference_audio, _ = librosa.load(reference_audio_path, sr=None)
        self.reference_features = self.extract_features(self.reference_audio)

    def extract_features(self, audio_data):
        return np.mean(librosa.feature.mfcc(y=audio_data, sr=8000, n_mfcc=50).T, axis=0)

    def verify_speaker(self, audio_path, threshold=100):
        input_audio, _ = librosa.load(audio_path, sr=None)
        input_features = self.extract_features(input_audio)
        distance = np.linalg.norm(input_features - self.reference_features)
        return distance < threshold

if __name__ == "__main__":
     audio_data_dir = 'audio_data/'
     voice_verifier = VoiceVerification(audio_data_dir)

     print("Verifying speakers:")
     for file in os.listdir(audio_data_dir):
         if file.endswith(".wav"):   
             audio_path = os.path.join(audio_data_dir, file)
             is_speaker_verified = voice_verifier.verify_speaker(audio_path)
             print(f"{file}: {'Verified' if is_speaker_verified else 'Not Verified'}")
