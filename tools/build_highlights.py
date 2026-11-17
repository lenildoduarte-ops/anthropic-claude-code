# Monta os clipes do highlight de jiu-jitsu (corte, velocidade, zoom punch, color grade).
# Uso: coloque o video original em src/video.MOV ao lado deste script e rode: python3 build_highlights.py
# Depois concatene clips/c*.mp4 com ffmpeg -f concat.
import subprocess, sys, os
S=os.path.dirname(os.path.abspath(__file__)); SRC=f"{S}/src/video.MOV"
# start, end, speed, cx, zoom, punch(sec into output clip or None), flash
SEG=[
 (151.2,152.6,0.4,0.32,1.5,0.9,False),   # hook: scramble slowmo
 (27.0,33.0,1.5,0.42,1.5,None,True),     # face-off & grips
 (56.0,59.0,2.0,0.35,1.4,None,True),
 (59.0,62.0,0.5,0.35,1.4,2.8,False),     # scramble slowmo
 (85.0,95.0,2.5,0.45,1.5,None,True),     # grind
 (98.0,99.5,1.0,0.35,1.5,None,True),
 (99.5,101.5,0.5,0.35,1.5,0.6,False),    # standing pass slowmo
 (101.5,104.0,1.0,0.35,1.5,None,False),
 (104.0,118.0,3.0,0.42,1.5,None,True),
 (120.0,123.1,1.0,0.38,1.5,0.4,True),
 (150.0,151.4,1.0,0.32,1.5,None,True),
 (151.4,152.4,0.4,0.32,1.5,0.8,False),
 (152.4,154.2,1.5,0.35,1.5,None,False),
 (154.2,155.6,0.5,0.40,1.5,0.3,False),
 (180.0,200.0,4.0,0.47,1.5,None,True),
 (206.0,209.4,1.0,0.50,1.25,0.5,True),
 (209.4,211.6,0.5,0.45,1.25,1.2,False),
 (211.6,213.4,1.2,0.40,1.3,None,False),
 (213.4,216.0,1.0,0.35,1.4,None,False),
 (228.0,231.0,2.0,0.33,1.5,None,True),
 (274.0,278.0,1.0,0.38,1.5,None,True),
 (278.0,280.0,0.6,0.42,1.5,0.2,False),
 (286.0,291.0,2.0,0.44,1.5,None,True),
]
GRADE=("huesaturation=hue=0:saturation=-0.35:intensity=0:colors=b+c:strength=1,"
       "eq=contrast=1.12:brightness=-0.02:saturation=0.95:gamma=0.97,"
       "colorbalance=rs=-0.06:bs=0.05:rh=0.06:gh=0.02:bh=-0.05,"
       "curves=master='0/0.03 0.25/0.20 0.5/0.5 0.75/0.80 1/0.97',"
       "unsharp=5:5:0.6,vignette=PI/4.5")
only = [int(a) for a in sys.argv[1:]]
for i,(a,b,sp,cx,z,punch,flash) in enumerate(SEG):
    if only and i not in only: continue
    w=int(1080/z)//2*2; h=int(1920/z)//2*2
    x=max(0,min(1080-w,int(cx*1080-w/2))); y=max(0,min(1920-h,int(0.52*1920-h/2)))
    f=[f"crop={w}:{h}:{x}:{y}"]
    if sp<1:
        f.append(f"minterpolate=fps={30/sp:.3f}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
        f.append(f"setpts=PTS*{30/(30/sp)/sp:.4f}")  # identity-length fix below
    f[-1:] = f[-1:] if sp>=1 else [f"setpts=(PTS-STARTPTS)/{sp}"]
    if sp>=1: f.append(f"setpts=(PTS-STARTPTS)/{sp}")
    f.append("fps=30")
    if punch is not None:
        zz=f"(1+0.14*if(gte(t,{punch}),exp(-(t-{punch})*4),0))"
        f.append(f"scale=w='trunc(1080*{zz}/2)*2':h='trunc(1920*{zz}/2)*2':eval=frame:flags=bicubic,crop=1080:1920")
    else:
        f.append("scale=1080:1920:flags=lanczos")
    f.append(GRADE)
    if flash: f.append("fade=in:st=0:d=0.15:color=white")
    f.append("format=yuv420p")
    vf=",".join(f)
    out=f"{S}/clips/c{i:02d}.mp4"
    cmd=["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(b-a),"-i",SRC,"-an","-vf",vf,
         "-c:v","libx264","-preset","medium","-crf","16","-r","30",out]
    subprocess.run(cmd,check=True); print(i,"ok",flush=True)
