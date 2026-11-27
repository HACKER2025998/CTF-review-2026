#!/usr/bin/env python3
from pathlib import Path
print(bytes(int(s,2) for s in Path('pieces_jointes/bits.txt').read_text().split()).decode())
