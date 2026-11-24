import numpy as np, wave, sys
def rd(p):
    w=wave.open(p); n=w.getnframes(); x=np.frombuffer(w.readframes(n),np.int16).reshape(-1,w.getnchannels()).astype(np.float32)/32768; return x
SR=48000; m=rd(sys.argv[1]); o=rd(sys.argv[2]); N=min(len(m),len(o)); m=m[:N]; o=o[:N]
t=np.arange(N)/SR
W=[(11.70,13.35),(21.45,25.05),(32.50,99)]
def win_env(W,r=0.15):
    e=np.zeros(N)
    for a,b in W: e=np.maximum(e,np.clip(np.minimum((t-a)/r+1,(b-t)/r+1),0,1))
    return e
sp=win_env(W)
music_g=1.0-0.82*sp            # music ducks to 18%
orig_g=0.16+0.84*sp            # ambient low, voice full
# normalise voice level inside windows
vo=o*orig_g[:,None]
rms_v=np.sqrt(np.mean((o[sp>0.9])**2))+1e-9
vo=vo*(0.24/rms_v)  # target speech rms
out=m*music_g[:,None]*0.9+vo
out=np.tanh(out*1.1)/np.tanh(1.1)
pk=np.max(np.abs(out)); out=out/pk*0.97
w=wave.open(sys.argv[3],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
print("rms_v",rms_v)
