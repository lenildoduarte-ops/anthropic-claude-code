import subprocess, json
SEG=[(0.75,2.20),(5.45,8.45),(9.15,18.35),(19.10,25.55)]
XF=0.12; SP=1.1
# word list (corrected transcript), source times
W=[("Essa",0.80),("é",1.14),("a",1.24),("data",1.36),("de",1.40),("pedido,",1.62),
("porque",5.50),("a",6.16),("gente",6.26),("consegue,",6.50),("com",7.78),
("essa",9.46),("data",9.72),("de",9.92),("pedido,",10.16),("entender",10.80),("a",11.34),("periodicidade",12.26),("que",12.78),("aquele",12.92),("cliente",13.12),("compra,",13.54),
("quanto",14.58),("tempo",14.72),("faz",14.92),("que",15.12),("ele",15.24),("já",15.40),("comprou,",15.58),("pra",16.42),("gente",16.68),("fazer",17.02),("uma",17.34),("nova",17.50),("abordagem",17.68),("pra",18.02),("ele.",18.20),
("É",19.18),("muito",19.40),("bom",19.64),("a",19.80),("gente",19.82),("atender",20.04),("o",20.32),("lead,",20.46),("qualificar",20.58),("e",21.26),("tornar",21.46),("ele",21.70),("cliente,",21.94),
("mas",22.30),("a",22.42),("gente",22.46),("também",22.72),("tem",23.02),("que",23.20),("cuidar",23.40),("da",23.80),("nossa",24.20),("base.",24.80)]
def m(t):
    acc=0
    for i,(a,b) in enumerate(SEG):
        if a-0.05<=t<=b+0.05: return (acc+t-a)/SP
        acc+=(b-a)-XF
    raise Exception(t)
out=[[w,round(m(t),3)] for w,t in W]
json.dump(out,open('words_out.json','w'),ensure_ascii=False)
cuts=[];acc=0
for a,b in SEG[:-1]: acc+=(b-a)-XF; cuts.append(round(acc/SP,3))
print("cuts(out):",cuts)
inp=[];fc=[]
for i,(a,b) in enumerate(SEG):
    inp+=["-ss",str(a),"-t",str(b-a),"-i","src.mp4"]
v="[0:v]";au="[0:a]";off=0
for i in range(1,len(SEG)):
    off+=SEG[i-1][1]-SEG[i-1][0]-XF
    fc.append(f"{v}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[v{i}]");fc.append(f"{au}[{i}:a]acrossfade=d={XF}[a{i}]")
    v=f"[v{i}]";au=f"[a{i}]"
fc.append(f"{v}setpts=PTS/{SP},fps=30[vo];{au}atempo={SP}[ao]")
subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",";".join(fc),"-map","[vo]","-map","[ao]","-c:v","libx264","-crf","14","-preset","fast","-c:a","pcm_s16le","base.mov"],check=True)
