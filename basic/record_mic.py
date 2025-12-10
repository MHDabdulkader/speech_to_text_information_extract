import sounddevice as sd
from scipy.io.wavfile import write
import  numpy as np

sample_rate = 44100 # CD-quality


# record until user stop
input("Please Enter to start record! ")
print("🎤 Recording... Press to Enter to stop recording")


sd.default.samplerate = sample_rate
sd.default.channels = 2
recording = []

with sd.InputStream(callback=lambda indata, frames, times,status: recording.append(indata.copy())):
    input()

audio = np.concatenate(recording, axis=0)

write("recorder.wav", sample_rate, audio)
print("✔️ saved as recording.wav")
