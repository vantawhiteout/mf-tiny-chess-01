import json,os,sys,urllib.request
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit()
def post(p,d):
 with urllib.request.urlopen(urllib.request.Request(U+p,data=json.dumps(d).encode()),timeout=30) as r:return json.load(r)
FN=" pnbrqk";KN=[33,31,18,14,-14,-18,-31,-33];KG=[1,-1,16,-16,15,17,-15,-17];BD=[15,17,-15,-17];RD=[1,-1,16,-16]
I=32000
def nm(s):return "abcdefgh"[s&7]+str((s>>4)+1)
def so(t):return (int(t[1])-1)*16+"abcdefgh".index(t[0])
KNA=[];KGA=[];PA=[[],[]]
for s in range(128):
 KNA.append([t for t in (s+d for d in KN)if not t&0x88]);KGA.append([t for t in (s+d for d in KG)if not t&0x88])
 for c in (0,1):PA[c].append([t for t in (s+(16 if c==0 else -16)+d for d in (-1,1))if not t&0x88])
z=123456789
def nx():
 global z;z^=z<<13;z&=0xffffffff;z^=z>>17;z^=z<<5;z&=0xffffffff;return z
Z=[[nx() for _ in range(128)]for _ in range(13)];ZS=nx();ZC=[nx()for _ in range(16)];ZE=[nx()for _ in range(8)]
D="000000006846482/0022442//101111/.001101..00/002/.0///22/00000000&*.-4*/)+-52140/-4245853/1132411/0112110//11112/.-/001//)/,././/.0+..-00.1//241-/233232000132200011221100111121101100120.0////./232341232244542301221341//02220/../0100/-.//000.-///010,//0110...0214333/.00/423//012434..//0100/.//0000/0/00010.01011000//1/..-,11/-.0120/000../20//01////.../.-0..--.-///--./.000,-/11/21-1.2100000000;;:898:<665443552210001111000000000000001111100000000000,./...,*.0.0/./-//110//-/011111//012110//00110//-//00//-.-////-,///00///000/0/0/00000000011111000011010//011100///000//.///0//0/111111101111001000000000001000000010000/00000/0/0000///0/0000/0//1122111/1234220/013321101234342/2132221/.101110//.///..../-0./-+.///10//11112111111133101222220/012211//011110/./01100/-.//.//-"
V=[(ord(c)-48)*16 for c in D]
MG=[0,82,337,365,477,1025,0];EG=[0,94,281,297,512,936,0];PH=[0,0,1,1,2,4,0]
PM=[[0]*128 for _ in range(13)];PE=[[0]*128 for _ in range(13)]
for t in range(1,7):
 for i in range(64):
  r=i//8;q=(7-r)*16+i%8;m=V[(t-1)*64+i];e=V[384+(t-1)*64+i]
  PM[t+6][q]=m;PE[t+6][q]=e;u=q^112;PM[-t+6][u]=m;PE[-t+6][u]=e
SQ=[-1]*128
for r in range(8):
 for f in range(8):SQ[r*16+f]=r*8+f
PS=[[0]*64,[0]*64]
for q in range(64):
 f=q&7;r=q>>3;m=sum(1<<(r*8+j)for j in(f-1,f,f+1)if 0<=j<8)
 PS[0][q]=m&~((1<<((r+1)*8))-1);PS[1][q]=m&((1<<(r*8))-1)
CF=[15]*128;CF[0]=13;CF[7]=14;CF[112]=7;CF[119]=11;CF[4]=12;CF[116]=3
class P:
 def __init__(s,fen):
  a=fen.split();s.b=[0]*128;s.o=[set(),set()];s.k=[-1,-1]
  for i,row in enumerate(a[0].split("/")):
   f=0
   for c in row:
    if c.isdigit():f+=int(c)
    else:
     t=FN.index(c.lower());col=0 if c.isupper() else 1;q=(7-i)*16+f;p=t if col==0 else -t
     s.b[q]=p;s.o[col].add(q)
     if t==6:s.k[col]=q
     f+=1
  s.s=0 if a[1]=="w" else 1;s.c=sum({"K":1,"Q":2,"k":4,"q":8}.get(c,0)for c in a[2])
  s.e=so(a[3])if a[3]!="-"else -1;s.hf=int(a[4]);s.hist=[];s.h=s.key()
 def key(s):
  h=ZC[s.c]^(ZS if s.s else 0)^(ZE[s.e&7]if s.e>=0 else 0)
  for c in (0,1):
   for q in s.o[c]:h^=Z[s.b[q]+6][q]
  return h
 def at(s,q,by):
  b=s.b
  for t in PA[1-by][q]:
   if b[t]==(1 if by==0 else -1):return 1
  for t in KNA[q]:
   if b[t]==(2 if by==0 else -2):return 1
  for t in KGA[q]:
   if b[t]==(6 if by==0 else -6):return 1
  for ds,ty in ((BD,(3,5)),(RD,(4,5))):
   for d in ds:
    t=q+d
    while not t&0x88:
     v=b[t]
     if v:
      if (v>0)==(by==0)and abs(v)in ty:return 1
      break
     t+=d
  return 0
 def gen(s,caps=0):
  b=s.b;side=s.s;sg=1 if side==0 else -1;out=[]
  for f in s.o[side]:
   p=b[f];t=abs(p)
   if t==1:
    one=f+16*sg
    if not one&0x88 and not b[one] and not caps:
     if one>>4 in (0,7):
      for pr in (5,4,3,2):out.append(f|one<<7|pr<<14)
     else:
      out.append(f|one<<7);two=one+16*sg
      if f>>4==(1 if side==0 else 6)and not b[two]:out.append(f|two<<7|4<<17)
    for to in PA[side][f]:
     v=b[to]
     if (v*sg<0 and abs(v)<6)or to==s.e:
      fl=1<<17 if to==s.e else 0
      if to>>4 in (0,7):
       for pr in (5,4,3,2):out.append(f|to<<7|pr<<14|fl)
      else:out.append(f|to<<7|fl)
   elif t in (2,6):
    for to in (KNA[f]if t==2 else KGA[f]):
     v=b[to]
     if not v or(v*sg<0 and abs(v)<6):out.append(f|to<<7)
   else:
    for d in (BD if t==3 else RD if t==4 else BD+RD):
     to=f+d
     while not to&0x88:
      v=b[to]
      if not v:
       if not caps:out.append(f|to<<7)
      else:
       if v*sg<0 and abs(v)<6:out.append(f|to<<7)
       break
      to+=d
  if not caps and s.c:
   if side==0:
    if s.c&1 and not b[5]and not b[6]and not s.at(4,1)and not s.at(5,1)and not s.at(6,1):out.append(4|6<<7|2<<17)
    if s.c&2 and not b[1]and not b[2]and not b[3]and not s.at(4,1)and not s.at(3,1)and not s.at(2,1):out.append(4|2<<7|2<<17)
   else:
    if s.c&4 and not b[117]and not b[118]and not s.at(116,0)and not s.at(117,0)and not s.at(118,0):out.append(116|118<<7|2<<17)
    if s.c&8 and not b[113]and not b[114]and not b[115]and not s.at(116,0)and not s.at(115,0)and not s.at(114,0):out.append(116|114<<7|2<<17)
  return out
 def mv(s,m):
  f=m&127;to=m>>7&127;pr=m>>14&7;fl=m>>17;b=s.b;p=b[f];cap=b[to];side=s.s;nc=s.c&CF[f]&CF[to];ep0=s.e
  s.o[side].remove(f);s.o[side].add(to);b[f]=0;b[to]=p
  if pr:b[to]=pr if side==0 else -pr
  cf=-1;cc=0
  if fl&1:
   cf=to-16 if side==0 else to+16;cc=b[cf];b[cf]=0;s.o[1-side].discard(cf)
  rf=-1;rp=0
  if fl&2:
   if to==6:rf,rt=7,5
   elif to==2:rf,rt=0,3
   elif to==118:rf,rt=119,117
   else:rf,rt=112,115
   rp=b[rf];b[rf]=0;b[rt]=rp;s.o[side].remove(rf);s.o[side].add(rt)
  if abs(p)==6:s.k[side]=to
  s.c=nc;s.e=(f+to)//2 if fl&4 else -1;s.hf=0 if abs(p)==1 or cap or fl&1 else s.hf+1
  if cap:s.o[1-side].discard(to)
  h0=s.h;hh=s.h^Z[p+6][f]^Z[p+6][to]^ZS^ZC[s.c]^ZC[nc]^(Z[cap+6][to]if cap else 0)
  if ep0>=0:hh^=ZE[ep0&7]
  if fl&1:hh^=Z[cc+6][cf]
  if fl&2:hh^=Z[rp+6][rf]^Z[rp+6][(5 if to==6 else 3 if to==2 else 117 if to==118 else 115)]
  if fl&4:hh^=ZE[((f+to)//2)&7]
  s.h=hh;s.s=1-side;s.hist.append(hh)
  return(p,cap,nc,ep0,s.hf,cf,cc,rf,rp,h0)
 def um(s,m,u):
  f=m&127;to=m>>7&127;p,cap,c,ep,hf,cf,cc,rf,rp,h0=u;b=s.b;side=1-s.s
  b[f]=p;b[to]=cap;s.o[side].add(f);s.o[side].discard(to)
  if cap:s.o[1-side].add(to)
  if cf>=0:b[cf]=cc;s.o[1-side].add(cf)
  if rf>=0:
   rt=5 if to==6 else 3 if to==2 else 117 if to==118 else 115
   b[rf]=rp;b[rt]=0;s.o[side].add(rf);s.o[side].discard(rt)
  if abs(p)==6:s.k[side]=f
  s.c=c;s.e=ep;s.hf=hf;s.s=side;s.h=h0;s.hist.pop()
 def ev(s):
  b=s.b;mg=eg=ph=0;wp=bp=0
  for q in s.o[0]:
   p=b[q];t=p;mg+=MG[t]+PM[p+6][q];eg+=EG[t]+PE[p+6][q];ph+=PH[t]
   if t==1:wp|=1<<SQ[q]
  for q in s.o[1]:
   p=b[q];t=-p;mg-=MG[t]+PM[p+6][q];eg-=EG[t]+PE[p+6][q];ph+=PH[t]
   if t==1:bp|=1<<SQ[q]
  for c,my,op,sg in ((0,wp,bp,1),(1,bp,wp,-1)):
   pp=my
   while pp:
    bit=pp&-pp;pp^=bit;q=bit.bit_length()-1;r=q>>3
    if not op&PS[c][q]:
     aa=r if c==0 else 7-r;mg+=(8+aa*aa*2)*sg;eg+=(12+aa*aa*4)*sg
  if ph>24:ph=24
  v=(mg*ph+eg*(24-ph))//24
  return v+10 if s.s==0 else 10-v
class S:
 def __init__(s,p,n):s.p=p;s.n=n;s.c=0;s.tt={};s.hs={};s.k=[[0,0]for _ in range(80)]
 def order(s,ms,tm):
  b=s.p.b;k=s.k[min(79,len(s.p.hist))]
  def ky(m):
   if m==tm:return -1000000
   v=b[m>>7&127]
   if v or m>>14&7 or m>>17&1:return -10000-(abs(v)if v else 1)*16
   if m in k:return -5000
   return -s.hs.get(m&127|m>>7<<7,0)
  ms.sort(key=ky);return ms
 def qs(s,a,be,d):
  s.c+=1;p=s.p;k=p.h
  st=p.ev()
  if d<-7:return st
  chk=p.at(p.k[p.s],1-p.s)
  if not chk:
   if st>=be:return st
   if st>a:a=st
  best=-I if chk else st
  for m in s.order(p.gen(not chk),0):
   u=p.mv(m)
   if p.at(p.k[1-p.s],p.s):p.um(m,u);continue
   sc=-s.qs(-be,-a,d-1);p.um(m,u)
   if sc>best:best=sc
   if sc>a:a=sc
   if a>=be:break
  return best
 def se(s,a,be,d,ply,nul):
  s.c+=1;p=s.p
  if s.c>s.n:return 0
  k=p.h
  chk=p.at(p.k[p.s],1-p.s)
  if d<=0:return s.qs(a,be,0)
  en=s.tt.get(k);tm=en[3]if en else 0
  if en and en[0]>=d and ply:
   dd,sc,fl,_=en
   if fl==0:return sc
   if fl==1 and sc>=be:return sc
   if fl==2 and sc<=a:return sc
  if nul and not chk and d>=3 and ply:
   ep=p.e;nh=p.h^ZS^(ZE[ep&7]if ep>=0 else 0);p.h=nh;p.e=-1;p.s^=1
   sc=-s.se(-be,-be+1,d-3,ply+1,0)
   p.s^=1;p.e=ep;p.h=k
   if sc>=be:return be
  ms=s.order(p.gen(),tm);best=-I;bm=0;a0=a
  for i,m in enumerate(ms):
   quiet=not(p.b[m>>7&127]or m>>14&7 or m>>17&1)
   u=p.mv(m)
   if p.at(p.k[1-p.s],p.s):p.um(m,u);continue
   red=1 if d>=3 and quiet and not chk and 4<=i<10 else 2 if d>=3 and quiet and not chk and i>=10 else 0
   if i==0:sc=-s.se(-be,-a,d-1-red,ply+1,1)
   else:
    sc=-s.se(-a-1,-a,d-1-red,ply+1,1)
    if sc>a and red:sc=-s.se(-a-1,-a,d-1,ply+1,1)
    if a<sc<be:sc=-s.se(-be,-a,d-1,ply+1,1)
   p.um(m,u)
   if s.c>s.n:return 0
   if sc>best:best=sc;bm=m
   if sc>a:
    a=sc
    if quiet:
     kk=s.k[min(79,ply)]
     if m!=kk[0]:kk[1]=kk[0];kk[0]=m
   if a>=be:
    if quiet:s.hs[m&127|m>>7<<7]=s.hs.get(m&127|m>>7<<7,0)+d*d
    break
  if not bm:return 0 if not chk else ply-I
  fl=0 if a0<best<be else 1 if best>=be else 2
  s.tt[k]=(d,best,fl,bm)
  return best
 def best(s,legal):
  p=s.p;p.hist.append(p.h)
  ms=[so(m[:2])|so(m[2:4])<<7|("nbrq".index(m[4])+2 if len(m)>4 else 0)<<14 for m in legal]
  ms=s.order(ms,0);bm=ms[0];fin=0
  for d in range(1,40):
   a=-I;scores=[]
   for i,m in enumerate(ms):
    u=p.mv(m)
    if p.at(p.k[1-p.s],p.s):p.um(m,u);continue
    sc=-s.se(-I,-a,d-1,1,1)if i==0 else-s.se(-a-1,-a,d-1,1,1)
    if i and a<sc<I:sc=-s.se(-I,-a,d-1,1,1)
    p.um(m,u)
    if s.c>s.n:break
    scores.append((sc,m))
    if sc>a:a=sc;bm=m
   if s.c>s.n or not scores:break
   fin=bm;ms.sort(key=lambda m:-next((v for v,x in scores if x==m),-I))
  m=fin or bm;f=m&127;to=m>>7&127;pr=m>>14&7
  return nm(f)+nm(to)+("nbrq"[pr-2]if pr else"")
BUDGET=150000
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  se=S(P(g["fen"]),BUDGET);mv=se.best(g["legal_moves"])
  g=post("/move",{"game":g["game"],"move":mv})
