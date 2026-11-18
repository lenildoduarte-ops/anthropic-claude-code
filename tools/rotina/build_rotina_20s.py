import subprocess, os
R=os.path.dirname(os.path.abspath(__file__))
SEG=[("6963",0.8,1.8,"hflip"),("6957",0.5,1.5,""),("6959",0.0,1.8,""),("6958",0.5,1.5,""),
     ("6963",11.4,1.8,"hflip"),("6957",7.5,1.5,""),("6960",3.0,1.5,""),("6959",1.8,1.6,""),
     ("6960",8.5,1.5,""),("6963",13.3,1.5,"hflip"),("6960",12.0,1.5,""),("6963",17.5,2.5,"hflip")]
G="eq=contrast=1.08:saturation=1.18:gamma=0.98,colorbalance=rh=0.03:bh=-0.03,unsharp=5:5:0.5"
for i,(f,s,d,x) in enumerate(SEG):
    vf=",".join(v for v in [x,"scale=1080:1920:force_original_aspect_ratio=increase","crop=1080:1920","fps=30",G,"format=yuv420p"] if v)
    af=f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.015,afade=t=out:st={d-0.02}:d=0.02"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(s),"-t",str(d),"-i",f"{R}/src/{f}.MOV","-vf",vf,"-af",af,
      "-c:v","libx264","-crf","16","-preset","fast","-c:a","pcm_s16le",f"{R}/seg20/s{i:02d}.mov"],check=True)
inp=[]; 
for i in range(len(SEG)): inp+=["-i",f"{R}/seg20/s{i:02d}.mov"]
n=len(SEG); tot=sum(s[2] for s in SEG)
fc="".join(f"[{i}:v][{i}:a]" for i in range(n))+f"concat=n={n}:v=1:a=1[cv][ca];"
fc+=f"[ca]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={tot-0.3:.2f}:d=0.3[aout];"
fc+=f"[{n}:v]format=rgba,fade=in:st=0:d=0.1:alpha=1,fade=out:st=1.6:d=0.2:alpha=1,setpts=PTS-STARTPTS[t];"
fc+="[cv][t]overlay=0:0:eof_action=pass:enable='lt(t,1.8)',format=yuv420p[vout]"
out="/home/user/anthropic-claude-code/output/rotina_cortes_20s.mp4"
subprocess.run(["ffmpeg","-v","error","-y",*inp,"-loop","1","-t","1.8","-i",f"{R}/hook.png","-filter_complex",fc,"-map","[vout]","-map","[aout]",
  "-c:v","libx264","-crf","18","-preset","slow","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",out],check=True)
print("done",tot)
