import subprocess, os
R=os.path.dirname(os.path.abspath(__file__))
# file, start, dur, extra filter
SEG=[("6963",0.8,2.4,"hflip"),
     ("6957",0.0,3.0,""),
     ("6959",0.0,3.5,""),
     ("6958",0.0,3.0,""),
     ("6963",9.5,4.5,"hflip"),
     ("6957",7.0,3.5,""),
     ("6960",2.5,2.3,""),
     ("6960",7.0,3.0,""),
     ("6963",16.5,3.5,"hflip")]
TR=["slideleft","zoomin","wipeup","slideright","smoothleft","circleopen","slideup","fadewhite"]
T=0.22
G="eq=contrast=1.08:saturation=1.18:gamma=0.98,colorbalance=rh=0.03:bh=-0.03,unsharp=5:5:0.5"
for i,(f,s,d,x) in enumerate(SEG):
    vf=",".join(v for v in [x,"scale=1080:1920:force_original_aspect_ratio=increase","crop=1080:1920","fps=30",G,"format=yuv420p"] if v)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(s),"-t",str(d),"-i",f"{R}/src/{f}.MOV","-vf",vf,
      "-af","aresample=48000,aformat=channel_layouts=stereo","-c:v","libx264","-crf","17","-preset","fast","-c:a","aac","-b:a","192k",f"{R}/seg/s{i}.mp4"],check=True)
inp=[]; 
for i in range(len(SEG)): inp+=["-i",f"{R}/seg/s{i}.mp4"]
fc=[]; off=0; vl="[0:v]"; al="[0:a]"
for i in range(1,len(SEG)):
    off+=SEG[i-1][2]-T
    fc.append(f"{vl}[{i}:v]xfade=transition={TR[i-1]}:duration={T}:offset={off:.3f}[v{i}]")
    fc.append(f"{al}[{i}:a]acrossfade=d={T}[a{i}]")
    vl=f"[v{i}]"; al=f"[a{i}]"
    off=off  # offset accumulates in output time
fc.append(f"{al}loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={off+SEG[-1][2]-0.6:.2f}:d=0.6[aout]")
fc.append(f"{vl}fade=t=out:st={off+SEG[-1][2]-0.4:.2f}:d=0.4:color=white,format=yuv420p[vout]")
out="/home/user/anthropic-claude-code/output/rotina_cortes_30s.mp4"
subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",";".join(fc),"-map","[vout]","-map","[aout]",
  "-c:v","libx264","-crf","19","-preset","slow","-profile:v","high","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",out],check=True)
print("done")
