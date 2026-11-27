#!/usr/bin/env python3
import os
import re
import time
import requests

URL = os.environ.get(
    "URL", "https://knyfhp57al3hs5ob.t.ctf.tg"
).rstrip("/")

S = requests.Session()
S.headers.update({"User-Agent": "NCTF26-Enye-BB98"})


def ceildiv(a, b):
    return -(-a // b)


def get_challenge():
    r = S.get(URL + "/challenge", timeout=15)
    r.raise_for_status()
    obj = r.json()
    return int(obj["n"]), int(obj["e"]), int(obj["c"])


class Oracle:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.t0 = time.monotonic()

    def __call__(self, c):
        for attempt in range(6):
            try:
                res = S.get(
                    URL + "/oracle",
                    params={"c": str(c % self.n)},
                    timeout=15
                )
                res.raise_for_status()

                obj = res.json()

                if "valid" not in obj or not isinstance(obj["valid"], bool):
                    raise ValueError("Unexpected reply: " + str(obj))

                self.count += 1

                if self.count % 1000 == 0:
                    elapsed = time.monotonic() - self.t0
                    print(
                        f"[*] {self.count} oracle calls; "
                        f"elapsed {elapsed:.0f}s",
                        flush=True
                    )

                return obj["valid"]

            except (requests.RequestException, ValueError) as exc:
                print(
                    "[!] HTTP error:", exc,
                    "retry", attempt + 1,
                    flush=True
                )
                time.sleep(min(1 + attempt, 5))

        raise RuntimeError("Oracle unreachable")


def merge(iv):
    if not iv:
        return []

    iv.sort()
    out = [list(iv[0])]

    for a, b in iv[1:]:
        if a <= out[-1][1] + 1:
            out[-1][1] = max(b, out[-1][1])
        else:
            out.append([a, b])

    return [tuple(x) for x in out]


def bb98(n, e, c, oracle):
    k = (n.bit_length() + 7) // 8
    B = 1 << (8 * (k - 2))

    print(
        "[+] RSA bits:", n.bit_length(),
        "block bytes:", k,
        flush=True
    )

    print("[+] Checking original ciphertext...", flush=True)

    if oracle(c):
        s0 = 1
        c0 = c
        print(
            "[+] Original ciphertext is PKCS compliant.",
            flush=True
        )
    else:
        print(
            "[!] Original ciphertext not accepted. "
            "Searching for blinding factor...",
            flush=True
        )

        s0 = 2

        while not oracle(c * pow(s0, e, n) % n):
            s0 += 1

        c0 = c * pow(s0, e, n) % n
        print("[+] Blinding factor:", s0, flush=True)

    iv = [(2 * B, 3 * B - 1)]
    s = ceildiv(n, 3 * B)
    iteration = 1

    while True:
        if iteration == 1:
            while not oracle(c0 * pow(s, e, n) % n):
                s += 1

        elif len(iv) > 1:
            s += 1

            while not oracle(c0 * pow(s, e, n) % n):
                s += 1

        else:
            a, b = iv[0]
            r = ceildiv(2 * (b * s - 2 * B), n)

            while True:
                low = ceildiv(2 * B + r * n, b)
                high = (3 * B - 1 + r * n) // a
                low = max(low, s + 1)

                found = False

                for candidate in range(low, high + 1):
                    if oracle(
                        c0 * pow(candidate, e, n) % n
                    ):
                        s = candidate
                        found = True
                        break

                if found:
                    break

                r += 1

        new = []

        for a, b in iv:
            r_min = ceildiv(a * s - (3 * B - 1), n)
            r_max = (b * s - 2 * B) // n

            for r in range(r_min, r_max + 1):
                aa = max(
                    a, ceildiv(2 * B + r * n, s)
                )
                bb = min(
                    b, (3 * B - 1 + r * n) // s
                )

                if aa <= bb:
                    new.append((aa, bb))

        iv = merge(new)

        if not iv:
            raise RuntimeError(
                "Empty interval: wrong oracle semantics "
                "or wrong data"
            )

        if iteration % 10 == 0 or (
            len(iv) == 1 and iteration < 5
        ):
            remaining = max(
                b - a for a, b in iv
            ).bit_length()

            print(
                f"[+] round {iteration} | "
                f"intervals {len(iv)} | "
                f"remaining bits {remaining} | "
                f"queries {oracle.count}",
                flush=True
            )

        if len(iv) == 1 and iv[0][0] == iv[0][1]:
            m0 = iv[0][0]
            m = m0 * pow(s0, -1, n) % n

            assert pow(m, e, n) == c % n, (
                "RSA check failed"
            )

            print(
                "[+] RSA ciphertext VERIFIED!",
                flush=True
            )

            return m, k

        iteration += 1


def decode_v15(block):
    if not block.startswith(b"\x00\x02"):
        raise ValueError("not PKCS#1 v1.5")

    i = block.find(b"\x00", 2)

    if i < 10:
        raise ValueError("invalid padding separator")

    return block[i + 1:]


def main():
    print("[+] Target", URL, flush=True)

    n, e, c = get_challenge()
    oracle = Oracle(n)

    m, k = bb98(n, e, c, oracle)

    block = m.to_bytes(k, "big")

    print(
        "[+] Complete block hex:",
        block.hex(),
        flush=True
    )

    payload = decode_v15(block)

    print(
        "[+] Decrypted message:",
        repr(payload),
        flush=True
    )

    match = re.search(rb"NCTF\{[^}]+\}", payload)

    if match:
        print(
            "\n" + "=" * 60
            + "\nFLAG: "
            + match.group().decode()
            + "\n" + "=" * 60,
            flush=True
        )
    else:
        print(
            "[?] No NCTF flag inside plaintext; "
            "inspect decrypted bytes",
            flush=True
        )


if __name__ == "__main__":
    main()
