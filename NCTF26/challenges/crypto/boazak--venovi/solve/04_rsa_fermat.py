#!/usr/bin/env python3
from pathlib import Path
import re
from math import isqrt
src=Path('pieces_jointes/challenge.txt').read_text()
params=dict(re.findall(r'^([nec])\s*=\s*(\d+)',src,re.M))
n,e,c=[int(params[k]) for k in 'nec']
a=isqrt(n)+(isqrt(n)**2<n)
for tries in range(1000000):
    diff=a*a-n; b=isqrt(diff)
    if b*b==diff:break
    a+=1
else:raise RuntimeError('No Fermat factors within limit')
p,q=a-b,a+b
assert p*q==n
d=pow(e,-1,(p-1)*(q-1))
msg=pow(c,d,n)
print(msg.to_bytes((msg.bit_length()+7)//8,'big').decode())
print('distance:',q-p,'iterations:',tries)
