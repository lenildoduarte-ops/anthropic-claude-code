import numpy as np, wave, sys
SR=48000; BPM=140; B=60/BPM; DUR=float(sys.argv[2]) if len(sys.argv)>2 else 46.0
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def t(n): return np.arange(n)/SR
def add(sig,at,pan=0.0,g=1.0):
    i=int(at*SR); 
    if i>=N: return
    s=sig[:N-i]*g; L[i:i+len(s)]+=s*(1-max(0,pan)); R[i:i+len(s)]+=s*(1+min(0,pan))
def lp(x,a):  # one-pole lowpass, a in (0,1)
    y=np.empty_like(x); acc=0.0
    for k in range(len(x)): acc+=a*(x[k]-acc); y[k]=acc
    return y
def hp(x,a): return x-lp(x,a)
def note(n): return 440*2**((n-69)/12)
# drums
def kick():
    n=int(.45*SR); tt=t(n); f=45+110*np.exp(-tt*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.tanh(2.2*np.sin(ph)*np.exp(-tt*7))*0.95
def clap():
    n=int(.25*SR); tt=t(n); nz=rng.standard_normal(n)
    env=np.exp(-tt*22)+0.6*np.exp(-np.maximum(tt-.012,0)*30)*(tt>.012)+0.5*np.exp(-np.maximum(tt-.024,0)*26)*(tt>.024)
    return hp(lp(nz,.35),.08)*env*0.55
def hat(d=.04,g=.22):
    n=int(d*SR); return hp(rng.standard_normal(n),.6)*np.exp(-t(n)/(d/4))*g
def b808(m,d,glide_from=None):
    n=int(d*SR); tt=t(n); f=np.full(n,note(m))
    if glide_from: f=note(m)+(note(glide_from)-note(m))*np.exp(-tt*18)
    ph=2*np.pi*np.cumsum(f)/SR; env=np.minimum(1,tt/.005)*np.exp(-tt*1.6)
    return np.tanh(3*np.sin(ph)*env)*0.55
def bell(m,d=.28):
    n=int(d*SR); tt=t(n); f1=note(m); f2=f1*1.48
    s=np.sign(np.sin(2*np.pi*f1*tt))+np.sign(np.sin(2*np.pi*f2*tt))
    return lp(hp(s,.05),.25)*np.exp(-tt*9)*0.16
def pad(ms,d):
    n=int(d*SR); tt=t(n); s=np.zeros(n)
    for m in ms:
        for det in (-0.12,0,0.11): s+=2*((tt*note(m)*2**(det/12))%1)-1
    s=lp(s/ (3*len(ms)),.03)
    env=np.minimum(1,tt/.4)*np.minimum(1,(d-tt)/.3)
    return s*env*0.5
def noise_rise(d):
    n=int(d*SR); tt=t(n); x=rng.standard_normal(n); out=np.zeros(n); acc=0
    for k in range(n):
        a=0.01+0.6*(tt[k]/d)**2; acc+=a*(x[k]-acc); out[k]=acc
    return out*(tt/d)**1.5*0.5
def whoosh(d=.45):
    n=int(d*SR); tt=t(n); x=rng.standard_normal(n); out=np.zeros(n); acc=0
    for k in range(n):
        a=0.04+0.5*np.sin(np.pi*tt[k]/d)**2; acc+=a*(x[k]-acc); out[k]=acc
    return out*np.sin(np.pi*tt/d)**2*0.6
def impact():
    n=int(1.6*SR); tt=t(n); f=30+60*np.exp(-tt*6)
    return (np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*2.2))*0.8+lp(rng.standard_normal(n),.05)*np.exp(-tt*4)*0.4)
DROP=8*B
chords=[[57,60,64],[53,57,60],[50,53,57],[52,56,59]]  # Am F Dm E
roots=[33,29,26,28]
bars=int(DUR/(4*B))+1
# intro pad + riser
add(pad([57,60,64,69],DROP),0,0,0.9); add(noise_rise(DROP),0,0,0.9)
for k in range(8): add(hat(.03,.12),k*B)
add(impact(),DROP,0,1.0)
end_full=float(sys.argv[3]) if len(sys.argv)>3 else DUR-2*4*B
mel=[69,None,72,69, 76,None,74,72, 69,None,72,74, 71,None,68,None]
for bar in range(2,bars):
    t0=bar*4*B
    if t0>=DUR: break
    c=(bar-2)%4
    add(pad(chords[c]+[chords[c][0]+12],4*B),t0,0,0.55)
    if t0>=end_full:  # outro: pad only + sparse kick
        add(kick(),t0); continue
    # kick pattern (trap): 1, 2.75, 3.5
    for kb in (0,1.75,2.5): add(kick(),t0+kb*B)
    for cb in (1,3): add(clap(),t0+cb*B,0,1.0)
    # 808
    add(b808(roots[c],1.6*B, glide_from=roots[c]+12 if bar%2 else None),t0,0,1.0)
    add(b808(roots[c],1.2*B),t0+1.75*B,0,0.9); add(b808(roots[c]+7,1.0*B),t0+2.5*B,0,0.8)
    # hats 1/8 with 1/32 rolls on beat 4 every other bar
    for h in range(8):
        pan=0.25 if h%2 else -0.25
        add(hat(),t0+h*B/2,pan)
    if bar%2==1:
        for r in range(8): add(hat(.02,.13+r*0.01),t0+3*B+r*B/8,0.2)
    # cowbell melody (phonk) from bar 4
    if bar>=4:
        for i,m in enumerate(mel):
            if m: add(bell(m+ (0 if c<2 else -2)),t0+i*B/4,0.15*((-1)**i),1.0)
# transition sfx times passed via argv[1] file
try:
    for line in open(sys.argv[1]):
        tt_,kind=line.split()
        tt_=float(tt_)
        if kind=='whoosh': add(whoosh(),tt_-0.22,0,0.9)
        if kind=='impact': add(impact(),tt_,0,0.7)
except FileNotFoundError: pass
# simple sidechain on everything except kick isn't separated; apply gentle master glue
mx=np.max(np.abs(np.concatenate([L,R])))
L=np.tanh(1.4*L/mx)*0.89; R=np.tanh(1.4*R/mx)*0.89
fade=int(1.2*SR); env=np.ones(N); env[-fade:]=np.linspace(1,0,fade)
st=(np.stack([L*env,R*env],1)*32767).astype(np.int16)
w=wave.open(sys.argv[4] if len(sys.argv)>4 else 'music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
print("ok",DUR)
