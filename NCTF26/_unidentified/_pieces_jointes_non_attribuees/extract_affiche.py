#!/usr/bin/env python3
"""
NCTF26 stego — Tisserands Dapaong.
Message caché dans le LSB du CANAL ROUGE de affiche.png.
Format : uint32 big-endian (longueur) puis N octets UTF-8.
On teste les deux ordres de bits (MSB-first / LSB-first) et on garde le bon.
Usage : python3 extract_affiche.py affiche.png
"""
import sys
from PIL import Image

path = sys.argv[1] if len(sys.argv) > 1 else "affiche.png"
img = Image.open(path).convert("RGB")
reds = [px[0] for px in img.getdata()]          # canal rouge, ordre des pixels
lsbs = [r & 1 for r in reds]

def bits_to_bytes(bits, msb_first=True):
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        chunk = bits[i:i+8]
        if not msb_first:
            chunk = chunk[::-1]
        byte = 0
        for b in chunk:
            byte = (byte << 1) | b
        out.append(byte)
    return bytes(out)

for msb in (True, False):
    data = bits_to_bytes(lsbs, msb_first=msb)
    if len(data) < 4:
        continue
    n = int.from_bytes(data[:4], "big")
    if 0 < n <= len(data) - 4:
        msg = data[4:4+n]
        try:
            txt = msg.decode("utf-8")
        except UnicodeDecodeError:
            txt = msg.decode("utf-8", "replace")
        print(f"[bits {'MSB' if msb else 'LSB'}-first] longueur={n}")
        print("message:", txt)
        if "NCTF{" in txt or txt.isprintable():
            print(">>> FLAG probable :", txt)
            break
