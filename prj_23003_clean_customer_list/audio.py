from pydub import AudioSegment

# Load the M4A file
audio = AudioSegment.from_file("input.m4a", format="m4a")

# Export as WAV
audio.export("output.wav", format="wav")
