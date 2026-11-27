#!/usr/bin/env python3
# RxR CTF - "Three Locks"
# Pure python 3, no dependencies.  python3 chall.py > output.txt
import hashlib, json, os, random
from secret import FLAG   # bytes, RxR{...}

# ----------------------------------------------------------------- utils
def is_prime(n, k=40):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for _ in range(k):
        x = pow(random.randrange(2, n - 1), d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def get_prime(bits):
    while True:
        p = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(p): return p

def stream(key, n):
    out = b""
    ctr = 0
    while len(out) < n:
        out += hashlib.sha256(key + ctr.to_bytes(8, "big")).digest()
        ctr += 1
    return out[:n]

def xor(a, b): return bytes(x ^ y for x, y in zip(a, b))

# ----------------------------------------------------------------- lock 3: Wyrm-128
SBOX = [
    0x14, 0x45, 0x2f, 0x7e, 0x7c, 0x2d, 0x47, 0x16, 0xe3, 0xb2, 0xd8, 0x89, 0x8b, 0xda, 0xb0, 0xe1,
    0x57, 0x06, 0x6c, 0x3d, 0x3f, 0x6e, 0x04, 0x55, 0xa0, 0xf1, 0x9b, 0xca, 0xc8, 0x99, 0xf3, 0xa2,
    0x94, 0xc5, 0xaf, 0xfe, 0xfc, 0xad, 0xc7, 0x96, 0x63, 0x32, 0x58, 0x09, 0x0b, 0x5a, 0x30, 0x61,
    0xd7, 0x86, 0xec, 0xbd, 0xbf, 0xee, 0x84, 0xd5, 0x20, 0x71, 0x1b, 0x4a, 0x48, 0x19, 0x73, 0x22,
    0xff, 0xae, 0xc4, 0x95, 0x97, 0xc6, 0xac, 0xfd, 0x08, 0x59, 0x33, 0x62, 0x60, 0x31, 0x5b, 0x0a,
    0xbc, 0xed, 0x87, 0xd6, 0xd4, 0x85, 0xef, 0xbe, 0x4b, 0x1a, 0x70, 0x21, 0x23, 0x72, 0x18, 0x49,
    0x7f, 0x2e, 0x44, 0x15, 0x17, 0x46, 0x2c, 0x7d, 0x88, 0xd9, 0xb3, 0xe2, 0xe0, 0xb1, 0xdb, 0x8a,
    0x3c, 0x6d, 0x07, 0x56, 0x54, 0x05, 0x6f, 0x3e, 0xcb, 0x9a, 0xf0, 0xa1, 0xa3, 0xf2, 0x98, 0xc9,
    0xc1, 0x90, 0xfa, 0xab, 0xa9, 0xf8, 0x92, 0xc3, 0x36, 0x67, 0x0d, 0x5c, 0x5e, 0x0f, 0x65, 0x34,
    0x82, 0xd3, 0xb9, 0xe8, 0xea, 0xbb, 0xd1, 0x80, 0x75, 0x24, 0x4e, 0x1f, 0x1d, 0x4c, 0x26, 0x77,
    0x41, 0x10, 0x7a, 0x2b, 0x29, 0x78, 0x12, 0x43, 0xb6, 0xe7, 0x8d, 0xdc, 0xde, 0x8f, 0xe5, 0xb4,
    0x02, 0x53, 0x39, 0x68, 0x6a, 0x3b, 0x51, 0x00, 0xf5, 0xa4, 0xce, 0x9f, 0x9d, 0xcc, 0xa6, 0xf7,
    0x2a, 0x7b, 0x11, 0x40, 0x42, 0x13, 0x79, 0x28, 0xdd, 0x8c, 0xe6, 0xb7, 0xb5, 0xe4, 0x8e, 0xdf,
    0x69, 0x38, 0x52, 0x03, 0x01, 0x50, 0x3a, 0x6b, 0x9e, 0xcf, 0xa5, 0xf4, 0xf6, 0xa7, 0xcd, 0x9c,
    0xaa, 0xfb, 0x91, 0xc0, 0xc2, 0x93, 0xf9, 0xa8, 0x5d, 0x0c, 0x66, 0x37, 0x35, 0x64, 0x0e, 0x5f,
    0xe9, 0xb8, 0xd2, 0x83, 0x81, 0xd0, 0xba, 0xeb, 0x1e, 0x4f, 0x25, 0x74, 0x76, 0x27, 0x4d, 0x1c,
]
ROUNDS = 14

def xt(a): return ((a << 1) ^ 0x1b) & 0xff if a & 0x80 else a << 1

def mix(c):
    t = c[0] ^ c[1] ^ c[2] ^ c[3]
    return [c[i] ^ t ^ xt(c[i] ^ c[(i + 1) % 4]) for i in range(4)]

def round_keys(key):
    rks, h = [], key
    for r in range(ROUNDS + 1):
        h = hashlib.sha256(h + bytes([r])).digest()
        rks.append(list(h[:16]))
    return rks

def wyrm_encrypt(key, block):
    rk = round_keys(key)
    s = list(block)
    for r in range(ROUNDS):
        s = [x ^ k for x, k in zip(s, rk[r])]
        s = [SBOX[x] for x in s]
        s = [s[(i + 4 * (i % 4)) % 16] for i in range(16)]           # shift rows
        s = sum((mix(s[4 * j:4 * j + 4]) for j in range(4)), [])      # mix columns
        s = [(x << 3 | x >> 5) & 0xff for x in s]                     # twist
    return bytes(x ^ k for x, k in zip(s, rk[ROUNDS]))

def pad(m):
    n = 16 - len(m) % 16
    return m + bytes([n]) * n

# ----------------------------------------------------------------- lock 2: a curve of my own
def ec_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0: return None
    if P == Q:
        l = (3 * P[0] * P[0] + a) * pow(2 * P[1], -1, p) % p
    else:
        l = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p) % p
    x = (l * l - P[0] - Q[0]) % p
    return (x, (l * (P[0] - x) - P[1]) % p)

def ec_mul(k, P, a, p):
    R = None
    while k:
        if k & 1: R = ec_add(R, P, a, p)
        P = ec_add(P, P, a, p)
        k >>= 1
    return R

# ----------------------------------------------------------------- main
def main():
    from secret import P, A, B, G, D   # the curve y^2 = x^3 + A x + B over GF(P), base point, secret scalar
    assert (G[1] ** 2 - G[0] ** 3 - A * G[0] - B) % P == 0
    Q = ec_mul(D, G, A, P)

    # lock 1
    p, q = get_prime(512), get_prime(512)
    n, e = p * q, 65537
    leak = p ^ int(f"{q:0512b}"[::-1], 2)
    c = pow(P, e, n)

    # lock 3
    k3 = os.urandom(16)
    known = [os.urandom(16) for _ in range(160)]
    vault = {
        "known": [[m.hex(), wyrm_encrypt(k3, m).hex()] for m in known],
        "flag": b"".join(wyrm_encrypt(k3, pad(FLAG)[i:i + 16]) for i in range(0, len(pad(FLAG)), 16)).hex(),
    }
    blob = json.dumps(vault).encode()
    sealed = xor(blob, stream(hashlib.sha256(str(D).encode()).digest(), len(blob)))

    print(f"n = {n}")
    print(f"e = {e}")
    print(f"leak = {leak}")
    print(f"c = {c}")
    print(f"G = {G}")
    print(f"Q = {Q}")
    print(f"sealed = {sealed.hex()}")

if __name__ == "__main__":
    main()
