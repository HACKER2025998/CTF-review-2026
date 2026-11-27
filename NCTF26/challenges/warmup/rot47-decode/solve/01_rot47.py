#!/usr/bin/env python3
from pathlib import Path
s=Path('pieces_jointes/secret(1).txt').read_text()
print(''.join(chr(33+(ord(x)-33+47)%94) if 33<=ord(x)<=126 else x for x in s))
