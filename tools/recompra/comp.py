import subprocess,sys
cuts=[1.209,3.827,8.70,12.082,15.0]; Z=[1.0,1.1,1.0,1.12,1.0,1.1]; d=0.25
expr=str(Z[0])
for c,a,b in zip(cuts,Z,Z[1:]):
    s=f"(clip((t-{c})/{d},0,1))"; expr=f"({expr}+({b}-{a})*{s}*{s}*(3-2*{s}))"
frames=sys.argv[1]; out=sys.argv[2]; dur=sys.argv[3] if len(sys.argv)>3 else None
fc=(f"[0:v]crop=1080:1100:0:400,curves=master='0/0 0.5/0.5 0.8/0.76 1/0.9',eq=contrast=1.06:saturation=1.05,"
    f"scale=w='trunc(1080*{expr}/2)*2':h='trunc(1100*{expr}/2)*2':eval=frame,crop=1080:960:'(iw-1080)*0.36':'(ih-960)*0.45',setsar=1[bot];"
    f"color=c=0x0b1120:s=1080x1920:r=30[cv];[cv][bot]overlay=0:960:shortest=1[c];[c][1:v]overlay=0:0:eof_action=pass,format=yuv420p[v];[0:a]loudnorm=I=-14:TP=-1.5[a]")
cmd=["ffmpeg","-v","error","-y","-i","base.mov","-framerate","30","-i",f"{frames}/f%05d.png","-filter_complex",fc,"-map","[v]","-map","[a]"]
if dur: cmd+=["-t",dur]
cmd+=["-c:v","libx264","-crf","18","-preset","slow","-c:a","aac","-b:a","192k","-movflags","+faststart",out]
subprocess.run(cmd,check=True)
