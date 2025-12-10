import wave

audio_object = wave.open("C:/Users/Abdul_Kader/voice recog/basic/harvard.wav", "rb")

print("Number of channel", audio_object.getnchannels())
print("parameters", audio_object.getparams())

total_audio = audio_object.getnframes() / audio_object.getframerate()

print("Total audio length ", total_audio)
framerate = audio_object.getframerate()
channel = audio_object.getnchannels()
sampleWidth = audio_object.getsampwidth()

frames = audio_object.readframes(-1)
print(type(frames), type(frames[0]))
print(len(frames))
audio_object.close()

audio_object_new = wave.open("C:/Users/Abdul_Kader/voice recog/basic/harvard_new.wav", "wb")

audio_object_new.setframerate(framerate)
audio_object_new.setnchannels(channel)
audio_object_new.setsampwidth(sampleWidth)

audio_object_new.writeframes(frames)

audio_object_new.close()