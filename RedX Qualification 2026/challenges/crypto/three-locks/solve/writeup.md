# Three Locks — Write-up

- **Category:** Crypto
- **Author:** DRX0
- **Flag:** `RxR{n0d3s_4nd_m1rr0rs_unl0ck_th3_l1n34r_wyrm_v4ult}`

## Overview

Three nested locks, each gating the next:

1. **RSA with a bit-leak** → recovers the prime `P` (the modulus of lock 2's curve).
2. **ECDLP on a *singular* curve** → recovers the secret scalar `D`.
3. **A custom block cipher "Wyrm-128" that is actually affine** → decrypts the flag.

The three hints map to the three locks:
- *"the path was smooth. The old keeper lied"* → the curve is **singular** (not smooth).
- *"Others open with reflections"* → lock 1's leak is a **bit-reversal**.
- *"The wyrm … never learned to bend"* → Wyrm-128 is **linear/affine** (no bending = no nonlinearity).

## Lock 1 — RSA, recover `P`

```python
n, e, leak, c = ...   # from output.txt
# leak = p ^ int(f"{q:0512b}"[::-1], 2)  = p ^ reverse_bits(q)
```

Because `leak = p ^ reverse_bits(q)`, and bit-reversal is an involution:

```
q = reverse_bits(p ^ leak)
```

So `p` fully determines `q`, and we need `p * reverse_bits(p ^ leak) = n`. Reconstruct
`p` from **both ends at once** with a product branch-and-bound: at step `i` fix bits
`i` (low) and `511-i` (high) of `p`; `q`'s low/high bits follow from the reverse
relation. Prune on `(p·q) mod 2^{i+1} == n mod 2^{i+1}` and on the high-bit product
bound `p_lo·q_lo ≤ n ≤ p_hi·q_hi`. The candidate set stays tiny and yields `p, q`.

Then standard RSA, and the plaintext **is** the curve prime:

```python
d = pow(e, -1, (p-1)*(q-1))
P = pow(c, d, n)      # 255-bit prime
```

## Lock 2 — singular-curve ECDLP, recover `D`

Only `G` and `Q = D·G` are published; `A, B` are secret. Two points give two
equations `y² = x³ + Ax + B`, so:

```python
A = ((Gy*Gy - Gx**3) - (Qy*Qy - Qx**3)) * pow(Gx - Qx, -1, P) % P
B = (Gy*Gy - Gx**3 - A*Gx) % P
disc = (-16*(4*A**3 + 27*B**2)) % P      # == 0  -> SINGULAR curve
```

The discriminant is 0: the cubic has a double root → the curve has a **node**. The
non-singular points of a nodal cubic form a group isomorphic to **GF(P)\***. Find the
double root `α = -3B/(2A)` (simple root `β = -2α`), and the node slope `c = √(3α)`.
Since `3α` is a QR, it's a *split* node → `GF(P)*`. Map points and solve an ordinary
DLP:

```python
def u(x, y): 
    return (y + c*(x-α)) * pow(y - c*(x-α), -1, P) % P
D = discrete_log(P, u(Qx,Qy), u(Gx,Gy))   # Pohlig–Hellman: P-1 is smooth
```

`P-1` factors into ~20-bit primes, so Pohlig-Hellman is instant.

## Lock 3 — the "linear wyrm" vault

```python
sealed = ...                              # from output.txt
blob = xor(sealed, stream(sha256(str(D)), len(sealed)))
vault = json.loads(blob)                  # 160 (plaintext, ciphertext) pairs + flag ciphertext
```

Wyrm-128 looks AES-like (S-box, shift-rows, mix-columns, 14 rounds), **but the S-box
is affine** and every other step is GF(2)-linear → for a fixed key the whole map
`m → E_k(m)` is **affine over GF(2)**:

```
E(m) = M·m ⊕ v
```

Therefore the *inverse* `c → m` is also affine, and we have 160 known `(m, c)`
pairs — more than enough to fit it. Fit the affine map from differences and apply it
to the flag ciphertext blocks:

```python
# basis of ciphertext-diffs with associated plaintext-diffs, then reduce each
# (flag_block ^ c0) over the basis and XOR the matching plaintext-diffs.
```

A held-out pair validates the fit, and all four flag blocks decrypt (then strip
PKCS#7):

```
RxR{n0d3s_4nd_m1rr0rs_unl0ck_th3_l1n34r_wyrm_v4ult}
```

## Flag

```
RxR{n0d3s_4nd_m1rr0rs_unl0ck_th3_l1n34r_wyrm_v4ult}
```
