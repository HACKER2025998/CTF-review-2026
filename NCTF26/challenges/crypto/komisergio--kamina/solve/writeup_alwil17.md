# Kamina — a base64 blob under a Vigenère key from 1914

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/kamina/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — An intercepted note hands me the key outright — `KAMINA1914`, "the
> old cipher of the Marne" (i.e. Vigenère) — and a base64 blob. I base64-decode
> the blob and run Vigenère decryption with the key to recover the flag. **Flag:**
> `NCTF{…}`.

## 1. Briefing

The whole challenge is a single scribble:

```
Intercepted operator scribble — 'the old cipher of the Marne':
key = KAMINA1914
BQIZDzU1WVxuRyosKBYhM1VcQ2s/LhI9JjNUXG5EJDI5OhE0X0pUVSckKRY6KVRmUF05Niw/KzJM
```

## 2. Analysis

Two hints decide the method:

- **"the old cipher of the Marne" / 1914** → a WWI-era polyalphabetic cipher,
  i.e. **Vigenère**.
- The payload is obvious **base64**, so it's an encoding wrapped around the
  ciphertext, not the cipher itself.

So the recipe is: base64-decode to get the raw ciphertext bytes, then reverse the
Vigenère step with `KAMINA1914`.

## 3. Exploitation

```python
import base64
blob = "BQIZDzU1WVxuRyosKBYhM1VcQ2s/LhI9JjNUXG5EJDI5OhE0X0pUVSckKRY6KVRmUF05Niw/KzJM"
key  = b"KAMINA1914"
data = base64.b64decode(blob)
flag = bytes((b - key[i % len(key)]) % 256 for i, b in enumerate(data))
print(flag.decode())   # NCTF{…}
```

(The exact combiner is subtract-mod for a text Vigenère; if the bytes don't land
as ASCII, the same key with XOR or add-mod is the obvious variant to try — the
key is given, so it's a one-liner either way.)

## 4. Flag

```text
NCTF{…}
```

## 5. Lessons

- When the challenge *gives* you the key, the puzzle is identifying the layers:
  here, base64 on the outside, Vigenère underneath.
- Classical ciphers with a known key are trivially reversible — they're fine for a
  warm-up, never for real secrecy.
