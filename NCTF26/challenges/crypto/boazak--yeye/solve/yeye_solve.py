#!/usr/bin/env python3
"""NCTF Yeye: SHA256 secret-prefix MAC length extension, requests low-rate."""
import hashlib, struct, requests, re, sys, time
from urllib.parse import quote_from_bytes
BASE=sys.argv[1].rstrip('/') if len(sys.argv)>1 else 'https://bwitph2ipsyqdnbr.t.ctf.tg'
S=requests.Session()
P=2**32-1
K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]
def pad(n): return b'\x80'+b'\x00'*((55-n)%64)+struct.pack('>Q',n*8)
def R(x,n):return ((x>>n)|(x<<(32-n)))&P
def compress(state,block):
 w=list(struct.unpack('>16I',block))
 for j in range(16,64):
  a,b=w[j-15],w[j-2]
  w.append((w[j-16]+(R(a,7)^R(a,18)^(a>>3))+w[j-7]+(R(b,17)^R(b,19)^(b>>10)))&P)
 a,b,c,d,e,f,g,h=state
 for j in range(64):
  t1=(h+(R(e,6)^R(e,11)^R(e,25))+((e&f)^(~e&g))+K[j]+w[j])&P
  t2=((R(a,2)^R(a,13)^R(a,22))+((a&b)^(a&c)^(b&c)))&P
  a,b,c,d,e,f,g,h=(t1+t2)&P,a,b,c,(d+t1)&P,e,f,g
 return [(x+y)&P for x,y in zip(state,(a,b,c,d,e,f,g,h))]
def extend(mac,original,extra,keylen):
 glue=pad(keylen+len(original))
 total=keylen+len(original)+len(glue)+len(extra)
 data=extra+pad(total)
 state=list(struct.unpack('>8I',bytes.fromhex(mac)))
 for j in range(0,len(data),64):state=compress(state,data[j:j+64])
 return original+glue+extra,b''.join(struct.pack('>I',v) for v in state).hex()
def call(q):
 try:
  r=S.get(BASE+'/pay?'+q,timeout=5)
  return r.status_code,r.text[:240]
 except Exception as ex:return 0,str(ex)
def main():
 try:
  j=S.get(BASE+'/challenge',timeout=8).json()
  msg=j['msg'].encode();mac=j['mac']
 except Exception as ex: print('Challenge unavailable:',ex);return
 print('challenge:',j,flush=True)
 # First test valid original signature with both URL-quoted message and hex-encoded message.
 modes=[('raw', lambda d:quote_from_bytes(d,safe='')),('hex',lambda d:d.hex())]
 for mode,encode in modes:
  for name in ('msg','data'):
   status,body=call(f'{name}={encode(msg)}&mac={mac}')
   print('BASELINE',mode,name,status,repr(body),flush=True)
 # Forge. The main candidate is a raw byte url-encoded `msg`; try hex too.
 for keylen in range(1,65):
  for extra in (b'&user=admin',):
   forged,newsig=extend(mac,msg,extra,keylen)
   for name,mode,encode in [('msg','raw',modes[0][1]),('msg','hex',modes[1][1]),('data','raw',modes[0][1]),('data','hex',modes[1][1])]:
    status,body=call(f'{name}={encode(forged)}&mac={newsig}')
    if 'NCTF{' in body:
     print('FLAG:',re.findall(r'NCTF\{[^}]+\}',body),flush=True);return
    if status !=403 or 'invalid mac' not in body.lower():
     print('UNUSUAL',keylen,name,mode,status,repr(body),flush=True)
   if keylen%8==0: print('Tried key lengths through',keylen,flush=True)
 print('No flag; check parameter format / secret length')
if __name__=='__main__':main()
