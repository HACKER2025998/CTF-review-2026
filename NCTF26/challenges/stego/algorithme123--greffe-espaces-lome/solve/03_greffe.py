#!/usr/bin/env python3
from pathlib import Path
lines=Path('pieces_jointes/arrete-greffe-lome.txt').read_bytes().splitlines()
bits=''.join('1' if x.endswith(bytes([9])) else '0' if x.endswith(b' ') else '' for x in lines)
print('bits:',len(bits))
assert len(bits)%8==0
print(bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8)).decode())
