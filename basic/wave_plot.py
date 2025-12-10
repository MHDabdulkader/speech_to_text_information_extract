import wave
import numpy as np
import matplotlib.pyplot as plt
audio_object = wave.open("C:/Users/Abdul_Kader/voice recog/basic/harvard.wav", "rb")


total_audio = audio_object.getnframes() / audio_object.getframerate()

print("Total audio length ", total_audio)
channel = audio_object.getnchannels()
sample_freq = audio_object.getframerate()
n_sample = audio_object.getnframes()
# sampleWidth = audio_object.getsampwidth()

frames = audio_object.readframes(-1)

audio_object.close()

total_audio =   n_sample/sample_freq

signal_array = np.frombuffer(frames, dtype=np.int16)

if channel == 2:
    signal_array = signal_array.reshape(-1, 2)
    signal_array = signal_array[:, 0]

times = np.linspace(0, total_audio, num=n_sample)

plt.figure(figsize=(15,5))
plt.plot(times, signal_array)
plt.title("Audio plot")
plt.xlabel("Times (s)")
plt.ylabel("Signal wave")
plt.xlim(0, total_audio)
plt.show()