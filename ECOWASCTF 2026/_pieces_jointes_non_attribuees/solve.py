#!/usr/bin/env python3
import re
import hashlib
from pathlib import Path
from sage.all import (
    GF, BooleanPolynomialRing, matrix, vector
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

N = 57

print("[+] QUADRATIC I - NCTF26", flush=True)

# 1. Lire les equations
lines = [
    s.strip()
    for s in Path("system.txt").read_text().splitlines()
    if s.strip() and not s.startswith("#")
]
assert len(lines) == 81

# 2. Construire le systeme polynomial GF(2)
R = BooleanPolynomialRing(
    N,
    names=[f"x{i}" for i in range(N)],
    order="degrevlex"
)
x = R.gens()

polys = []
terms = []

for line in lines:
    p = R.zero()
    eq = []

    for token in line.split("+"):
        token = token.strip()

        if token == "1":
            p += R.one()
            eq.append(())

        elif re.fullmatch(r"x\d+", token):
            i = int(token[1:])
            p += x[i]
            eq.append((i,))

        elif re.fullmatch(r"x\d+\*x\d+", token):
            a, b = map(
                lambda t: int(t[1:]),
                token.split("*")
            )
            p += x[a] * x[b]
            eq.append((a, b))

        else:
            raise ValueError(token)

    polys.append(p)
    terms.append(eq)

print("[+] 81 equations chargees", flush=True)
print("[+] Calcul de la base de Groebner...", flush=True)

# 3. Resolution algebrique avec PolyBoRi
I = R.ideal(polys)
gb = I.groebner_basis()

print("[+] Base calculee :", len(gb), flush=True)

# 4. Extraire les equations lineaires
rows = []
rhs = []

for p in gb:
    if p.degree() > 1:
        continue

    row = [0] * N
    constant = 0

    for monomial in p.monomials():
        if monomial == R.one():
            constant ^= 1
        else:
            for j in range(N):
                if monomial == x[j]:
                    row[j] ^= 1
                    break
            else:
                raise ValueError("Monome inattendu")

    if any(row):
        rows.append(row)
        rhs.append(constant)

A = matrix(GF(2), rows)

print("[+] Equations lineaires :", len(rows))
print("[+] Rang :", A.rank(), "/", N, flush=True)

if A.rank() != N:
    raise RuntimeError(
        "La base n'a pas donne 57 equations "
        "lineaires independantes."
    )

sol = list(A.solve_right(vector(GF(2), rhs)))
bits = [int(v) for v in sol]

# 5. Verification des 81 equations
for idx, eq in enumerate(terms):
    value = 0

    for term in eq:
        if len(term) == 0:
            value ^= 1
        elif len(term) == 1:
            value ^= bits[term[0]]
        else:
            a, b = term
            value ^= bits[a] & bits[b]

    assert value == 0, f"Equation {idx} invalide"

print("[+] 81/81 equations validees !", flush=True)

bitstring = "".join(map(str, bits))
print("[+] Solution :", bitstring, flush=True)

# 6. Lire le coffre
vault = Path("vault.txt").read_text()

nonce = bytes.fromhex(
    re.search(r"nonce\s*=\s*([0-9a-f]+)", vault).group(1)
)

ciphertext = bytes.fromhex(
    re.search(
        r"ciphertext\s*=\s*([0-9a-f]+)", vault
    ).group(1)
)

# 7. Tester les alignements des 57 bits
candidates = {
    "MSB pad left":
        int(bitstring, 2).to_bytes(8, "big"),

    "MSB pad right":
        int(bitstring + "0" * 7, 2).to_bytes(8, "big"),

    "LSB representation":
        sum(
            bit << i for i, bit in enumerate(bits)
        ).to_bytes(8, "big"),
}

for name, raw in candidates.items():
    key = hashlib.sha256(raw).digest()

    try:
        plaintext = AESGCM(key).decrypt(
            nonce, ciphertext, None
        )

        print("\n" + "=" * 55)
        print("[+] DECHIFFREMENT REUSSI :", name)
        print("[+] MESSAGE :", plaintext.decode(
            "utf-8", errors="replace"
        ))

        flags = re.findall(rb"NCTF\{[^}]+\}", plaintext)

        for flag in flags:
            print("FLAG :", flag.decode())

        print("=" * 55)
        break

    except Exception:
        print("[-] Echec GCM :", name, flush=True)

else:
    print("[!] Aucun alignement valide")
