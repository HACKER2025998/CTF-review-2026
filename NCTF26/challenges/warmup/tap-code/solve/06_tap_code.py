#!/usr/bin/env python3
from pathlib import Path
a='ABCDEFGHIKLMNOPQRSTUVWXYZ'
print(''.join(a[(int(x[0])-1)*5+int(x[1])-1] for x in Path('pieces_jointes/taps.txt').read_text().split()))
