import subprocess, os
V=os.path.dirname(os.path.abspath(__file__)); SRC=f"{V}/src/v.MOV"
G=("curves=master='0/0.03 0.25/0.36 0.5/0.60 0.75/0.81 1/0.94',eq=contrast=1.07:saturation=1.12,"
   "colorbalance=rs=-0.03:bs=0.04:rm=0.03:bm=-0.02,unsharp=5:5:0.6,vignette=PI/5")
# start,end,speed, base crop (w,h,x,y) , zoom expr in t (output seconds), label
BASE=(830,1476,40,250)
WAIST=(620,1102,150,520)
SEG=[(0.0,0.9,1.0,BASE,"1+0.08*t/0.9","abre"),
     (0.9,1.8,0.4,BASE,"1+0.16*exp(-t*3)","faixa girando slow"),
     (4.6,5.8,2.0,(900,1600,0,200),"1.0","rapido"),
     (5.8,6.8,0.5,(900,1600,0,200),"1+0.06*t/2","kimono slow zoom in"),
     (7.0,9.6,2.5,BASE,"1.12-0.12*t/1.04","gola rapido zoom out"),
     (10.0,14.6,3.0,BASE,"1+0.15*t/1.53","amarrando rapido zoom in"),
     (14.6,15.8,0.5,WAIST,"1+0.1*t/2.4","faixa preta slow close"),
     (16.0,19.0,2.0,BASE,"1.15-0.15*t/1.5","pronto zoom out"),
     (19.0,21.5,1.0,BASE,"1.2-0.2*t/2.5","final zoom out")]
for i,(a,b,sp,(w,h,x,y),z,_) in enumerate(SEG):
    f=[f"crop={w}:{h}:{x}:{y}"]
    if sp<1: f.append(f"minterpolate=fps={30/sp:.2f}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
    f+= [f"setpts=(PTS-STARTPTS)/{sp}","fps=30",
         f"scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':eval=frame:flags=bicubic","crop=1080:1920",G,"format=yuv420p"]
    dur=(b-a)/sp
    # audio: tempo-adjust; slow-mo gets pitched-down, quieter ambience
    if sp>=1:
        at=[]; r=sp
        while r>2: at.append("atempo=2"); r/=2
        at.append(f"atempo={r}"); af=",".join(at)
    else:
        af="asetrate=48000*%s,aresample=48000,volume=0.7"%sp
    af+=f",aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{dur:.3f},afade=t=in:d=0.02,afade=t=out:st={dur-0.03:.3f}:d=0.03"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(b-a),"-i",SRC,"-vf",",".join(f),"-af",af,
       "-t",f"{dur:.3f}","-c:v","libx264","-crf","15","-preset","fast","-c:a","pcm_s16le",f"{V}/seg/s{i}.mov"],check=True)
    print(i,round(dur,2),flush=True)
n=len(SEG); inp=[]
for i in range(n): inp+=["-i",f"{V}/seg/s{i}.mov"]
fc="".join(f"[{i}:v][{i}:a]" for i in range(n))+f"concat=n={n}:v=1:a=1[v][a];[a]loudnorm=I=-14:TP=-1.5[ao];[v]fade=t=out:st=14.3:d=0.4,format=yuv420p[vo]"
out="/home/user/anthropic-claude-code/output/ritual_faixa_15s.mp4"
subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",fc,"-map","[vo]","-map","[ao]","-t","14.7",
  "-c:v","libx264","-crf","18","-preset","slow","-c:a","aac","-b:a","192k","-movflags","+faststart",out],check=True)
