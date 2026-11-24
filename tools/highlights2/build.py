import subprocess, json, os, sys, numpy as np, wave
H=os.path.dirname(os.path.abspath(__file__)); B=60/140; T=0.2; FPS=30
SEG=json.load(open(f"{H}/plan.json"))
G="eq=contrast=1.08:saturation=1.12:gamma=0.98,colorbalance=rs=-0.03:bs=0.04:rh=0.04:bh=-0.03,unsharp=5:5:0.5,vignette=PI/5"
def zexpr(kind,d):
    if kind=="in": return f"(1+0.18*t/{d})"
    if kind=="out": return f"(1.22-0.22*t/{d})"
    if kind=="punch": return "(1+0.16*exp(-t*5))"
    return "1"
outs=[]
for i,s in enumerate(SEG):
    f,a,sp,beats=s["f"],s["a"],s["sp"],s["beats"]
    D=beats*B+(T if i<len(SEG)-1 else 0)
    src=D*sp
    z=zexpr(s.get("zoom",""),D)
    vf=[f"setpts=(PTS-STARTPTS)/{sp}","fps=30","scale=1080:1920:force_original_aspect_ratio=increase","crop=1080:1920"]
    if s.get("spin"):  # 360 spin over first 0.5s; zoom derived from angle so corners stay covered
        A="2*PI*(1-cos(PI*min(t/0.5,1)))/2"
        S=f"max((1080*abs(cos({A}))+1920*abs(sin({A})))/1080,(1080*abs(sin({A}))+1920*abs(cos({A})))/1920)*1.02*{z}"
        vf+=[f"scale=w='trunc(1080*{S}/2)*2':h='trunc(1920*{S}/2)*2':eval=frame",f"rotate=a='{A}':c=black","crop=1080:1920","tmix=frames=3:weights='1 1 1'"]
    else:
        vf+=[f"scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame","crop=1080:1920"]
    vf+=[G,"format=yuv420p"]
    at=[]; r=sp
    if sp<1: af="asetrate=48000*%s,aresample=48000"%sp
    else:
        while r>2: at.append("atempo=2"); r/=2
        at.append(f"atempo={r}"); af=",".join(at)
    af+=f",aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{D:.4f}"
    o=f"{H}/seg/s{i:02d}.mov"; outs.append((o,D))
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",f"{src+0.05:.4f}","-i",f"{H}/src/{f}.MOV","-vf",",".join(vf),"-af",af,
        "-t",f"{D:.4f}","-c:v","libx264","-crf","16","-preset","fast","-c:a","pcm_s16le",o],check=True)
    print(i,f,round(D,3),flush=True)
# compose with xfade
TR=[s.get("tr","fade") for s in SEG[1:]]
inp=[];fc=[];v="[0:v]";au="[0:a]";acc=0
for o,_ in outs: inp+=["-i",o]
for k in range(1,len(outs)):
    acc+=SEG[k-1]["beats"]*B
    fc.append(f"{v}[{k}:v]xfade=transition={TR[k-1]}:duration={T}:offset={acc:.4f}[v{k}]")
    fc.append(f"{au}[{k}:a]acrossfade=d={T}[a{k}]"); v=f"[v{k}]"; au=f"[a{k}]"
fc.append(f"{v}format=yuv420p[vo]")
subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",";".join(fc),"-map","[vo]","-map",au,"-c:v","libx264","-crf","15","-preset","fast","-c:a","pcm_s16le",f"{H}/edit.mov"],check=True)
tot=sum(s["beats"] for s in SEG)*B
json.dump({"total":tot,"cuts":[sum(s["beats"] for s in SEG[:k])*B for k in range(1,len(SEG))]},open(f"{H}/timing.json","w"))
print("total",tot)
