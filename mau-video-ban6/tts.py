import json,re,difflib,sys,numpy as np,soundfile as sf,scipy.signal as sg
from korvatts import TTS
from faster_whisper import WhisperModel
SP=float(sys.argv[1]) if len(sys.argv)>1 else 1.12
tts=TTS();wm=WhisperModel("small",device="cpu",compute_type="int8")
sc=json.load(open('sc.json',encoding='utf-8'))
def norm(t): return re.sub(r'[^\wà-ỹ ]','',re.sub(r'[\d]+',' ',t.lower())).replace('mít tơ','mr')
res=[]
for si,sents in enumerate(sc):
  for ti,s in enumerate(sents):
    best=None
    for steps,sp in ((20,SP),(24,SP-0.05),(20,SP+0.03)):
        w,d=tts.synthesize(s,voice="hoang_nam",lang="vi",total_steps=steps,speed=sp);w=np.asarray(w,dtype=np.float32).reshape(-1)
        a16=sg.resample_poly(w,160,441).astype(np.float32)
        got=' '.join(x.text for x in wm.transcribe(a16,language="vi")[0])
        r=difflib.SequenceMatcher(None,norm(s),norm(got)).ratio()
        if best is None or r>best[0]+0.02: best=(r,w,got)
        if r>=0.92: break
    print(si,ti,round(best[0],2),round(len(best[1])/44100,2),'|',best[2][:70],flush=True)
    res.append((si,best[1]))
sr=44100;GS=0.18;GC=0.35;lead=0.3
parts=[np.zeros(int(sr*lead),dtype=np.float32)];t=lead;tm=[];prev=None
for si,w in res:
    if prev is not None:
        g=GC if si!=prev else GS;parts.append(np.zeros(int(sr*g),dtype=np.float32));t+=g
    tm.append([si,round(t,2),round(t+len(w)/sr,2)]);parts.append(w);t+=len(w)/sr;prev=si
a=np.concatenate(parts+[np.zeros(int(sr*0.4),dtype=np.float32)]);a=a/(np.abs(a).max() or 1)*0.92
sf.write('voice.wav',a,sr);json.dump(tm,open('tm.json','w'));print('TOTAL',round(len(a)/sr,2))
