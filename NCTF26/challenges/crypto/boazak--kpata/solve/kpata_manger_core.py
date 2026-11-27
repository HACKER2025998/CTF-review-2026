
#!/usr/bin/env python3
"""Attaque de Manger contre RSA-OAEP avec oracle de premier octet nul."""

from __future__ import annotations
from typing import Callable
import hashlib


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def manger(
    n: int,
    e: int,
    c: int,
    leading_zero: Callable[[int], bool],
    log=print
) -> tuple[int, int]:
    """Retrouve le bloc OAEP à partir d'un oracle.

    leading_zero(ciphertext) doit renvoyer True si le premier
    octet du bloc RSA déchiffré est 0x00, False sinon.
    """

    k = (n.bit_length() + 7) // 8
    B = 1 << (8 * (k - 1))

    if 2 * B >= n:
        raise ValueError("Condition 2*B < n non satisfaite")

    queries = 0

    def ask(f: int) -> bool:
        nonlocal queries
        queries += 1
        ct = c * pow(f, e, n) % n
        return bool(leading_zero(ct))

    if not leading_zero(c):
        raise ValueError("Le ciphertext original ne commence pas par 0x00")

    # Phase 1
    log("[+] Phase 1 : recherche de f1")

    f1 = 2

    while ask(f1):
        f1 *= 2

        if queries > 2000:
            raise RuntimeError("Trop de requêtes en phase 1")

    log(f"[+] f1 = {f1}, requêtes = {queries}")

    # Phase 2
    log("[+] Phase 2 : recherche de f2")

    f2 = ((n + B) // B) * (f1 // 2)

    while not ask(f2):
        f2 += f1 // 2

        if queries > 2000:
            raise RuntimeError("Trop de requêtes en phase 2")

    log(f"[+] f2 = {f2}, requêtes = {queries}")

    # Phase 3
    log("[+] Phase 3 : réduction de l'intervalle")

    lo = ceil_div(n, f2)
    hi = ceil_div(n + B, f2)

    iteration = 0

    while hi - lo > 1:

        f = (2 * B) // (hi - lo)
        i = ceil_div(f * lo, n)
        f3 = ceil_div(i * n, lo)

        if f3 <= 0:
            raise RuntimeError("Multiplicateur f3 invalide")

        threshold = ceil_div(i * n + B, f3)

        if ask(f3):
            hi = min(hi, threshold)
        else:
            lo = max(lo, threshold)

        if lo >= hi:
            raise RuntimeError("Intervalle incohérent : vérifier l'oracle")

        iteration += 1

        if iteration % 64 == 0:
            log(
                f"[+] Tour {iteration}, "
                f"bits restants = {(hi-lo).bit_length()}, "
                f"requêtes = {queries}"
            )

        if queries > 2000:
            raise RuntimeError("Trop de requêtes en phase 3")

    m = lo

    if pow(m, e, n) != c % n:
        raise RuntimeError("Vérification RSA échouée")

    log(f"[+] Bloc RSA récupéré : {queries} requêtes")

    return m, queries


def mgf1(seed: bytes, length: int, hashname: str) -> bytes:
    hlen = hashlib.new(hashname).digest_size

    return b"".join(
        hashlib.new(
            hashname,
            seed + i.to_bytes(4, "big")
        ).digest()
        for i in range((length + hlen - 1) // hlen)
    )[:length]


def oaep_decode(
    em: bytes,
    hashname: str = "sha256",
    label: bytes = b""
) -> bytes:

    hlen = hashlib.new(hashname).digest_size

    if len(em) < 2 * hlen + 2 or em[0] != 0:
        raise ValueError("Bloc OAEP invalide")

    masked_seed = em[1:1 + hlen]
    masked_db = em[1 + hlen:]

    seedmask = mgf1(masked_db, hlen, hashname)

    seed = bytes(
        a ^ b for a, b in zip(masked_seed, seedmask)
    )

    dbmask = mgf1(seed, len(masked_db), hashname)

    DB = bytes(
        a ^ b for a, b in zip(masked_db, dbmask)
    )

    expected_hash = hashlib.new(hashname, label).digest()

    if DB[:hlen] != expected_hash:
        raise ValueError("Hash OAEP incorrect")

    rest = DB[hlen:]

    if b"\x01" not in rest:
        raise ValueError("Séparateur OAEP absent")

    i = rest.index(b"\x01")

    if any(rest[:i]):
        raise ValueError("Padding OAEP invalide")

    return rest[i + 1:]


def decode_candidates(m: int, n: int):
    k = (n.bit_length() + 7) // 8
    EM = m.to_bytes(k, "big")

    for hashname in ("sha256", "sha1", "sha384", "sha512"):

        try:
            data = oaep_decode(EM, hashname)

            print(f"[+] OAEP {hashname} : {data!r}")

            try:
                print("[FLAG]", data.decode("utf-8"))
            except UnicodeError:
                pass

        except ValueError:
            pass

    return EM


if __name__ == "__main__":
    print("[+] Manger core prêt.")
    print("[+] Importer manger et decode_candidates.")
