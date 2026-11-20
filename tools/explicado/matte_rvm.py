import sys, subprocess, numpy as np, onnxruntime as ort, time
src, out, model = sys.argv[1], sys.argv[2], sys.argv[3]
W,H=1080,1920
sess=ort.InferenceSession(model, providers=["CPUExecutionProvider"])
dec=subprocess.Popen(["ffmpeg","-v","error","-i",src,"-vf","fps=30","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","gray","-s",f"{W}x{H}","-r","30","-i","-","-c:v","ffv1",out],stdin=subprocess.PIPE)
rec=[np.zeros([1,1,1,1],np.float32)]*4; dr=np.array([0.25],np.float32); n=0; t0=time.time()
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    x=np.frombuffer(b,np.uint8).reshape(H,W,3).transpose(2,0,1)[None].astype(np.float32)/255
    fgr,pha,*rec=sess.run(None,{"src":x,"r1i":rec[0],"r2i":rec[1],"r3i":rec[2],"r4i":rec[3],"downsample_ratio":dr})
    enc.stdin.write((pha[0,0]*255).clip(0,255).astype(np.uint8).tobytes()); n+=1
    if n%100==0: print(n, f"{(time.time()-t0)/n:.2f}s/f", flush=True)
enc.stdin.close(); enc.wait(); print("frames",n)
