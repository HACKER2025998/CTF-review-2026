#!/usr/bin/env python3
from pathlib import Path
raw=bytes.fromhex(Path('pieces_jointes/calldata.txt').read_text().strip()[2:])
args=raw[4:]
off=int.from_bytes(args[64:96],'big')
n=int.from_bytes(args[off:off+32],'big')
print(args[off+32:off+32+n].decode())
