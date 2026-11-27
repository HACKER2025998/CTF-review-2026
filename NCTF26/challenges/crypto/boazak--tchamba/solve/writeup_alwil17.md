# Tchamba — an RSA least-significant-bit oracle

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/tchamba/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — The server's `/oracle` decrypts any ciphertext I send and leaks a
> single bit: the parity (least significant bit) of the plaintext. By sending
> `c · 2^e mod n`, `c · 4^e`, … I learn the parity of `2m`, `4m`, … which is a
> binary search that narrows the plaintext to a single value. A PoW gates each
> query, so I just grind it. **Flag:** the recovered plaintext.

## 1. Briefing

An oracle service: `POST /oracle` with a ciphertext `c` returns one bit. Each call
is gated by a proof-of-work (`/pow` → find a nonce so `sha256(prefix+nonce)` has
`difficulty` leading zeros). The target ciphertext decrypts to the flag.

## 2. Analysis

This is the textbook **RSA LSB (parity) oracle**. The oracle returns
`Dec(c) mod 2`. RSA is homomorphic for multiplication, so:

```
Dec(c · 2^e mod n) = 2·m mod n
```

The parity of `2m mod n` tells me whether `2m` wrapped around `n` — i.e. whether
`m` is above or below `n/2`. Multiplying by `2^e` again halves the interval each
round, so after `log2(n)` queries the interval collapses onto the plaintext.

## 3. Exploitation

```python
# query(c) -> parity bit of Dec(c), each call paying the PoW
lo, hi = 0, n
c = c0
mult = pow(2, e, n)
for _ in range(n.bit_length()):
    c = (c * mult) % n
    if query(c) == 0:        # Dec doubled is even -> m in lower half
        hi = (lo + hi) // 2
    else:                    # odd -> wrapped -> upper half
        lo = (lo + hi) // 2
m = hi                       # converges to the plaintext
print(bytes.fromhex(format(m, "x")))   # NCTF{…}
```

The PoW solver is a simple loop:

```python
def solve_pow(prefix, d):
    i = 0
    while not sha256((prefix + str(i)).encode()).hexdigest().startswith("0"*d):
        i += 1
    return i
```

## 4. Flag

```text
NCTF{…}
```

## 5. Lessons & remediation

- **Never leak plaintext bits.** A one-bit side channel (parity, padding
  validity, error vs success) is enough to recover the whole message.
- Use RSA-OAEP and reject malformed ciphertexts uniformly; don't expose a raw
  textbook-RSA decrypt. The PoW slows the attack but doesn't stop it — `log2(n)`
  queries is small.
