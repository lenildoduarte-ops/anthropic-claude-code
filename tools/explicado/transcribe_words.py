import sys, numpy as np, subprocess
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout,np.int16).astype(np.float32)/32768
segs,_=m.transcribe(a,language="pt",word_timestamps=True)
for s in segs:
    print(f"[{s.start:5.2f}-{s.end:5.2f}] {s.text.strip()}")
    print("   "+" ".join(f"{w.word.strip()}@{w.start:.2f}" for w in s.words))
