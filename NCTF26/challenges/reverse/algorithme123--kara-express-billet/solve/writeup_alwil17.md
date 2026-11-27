# Kara Express — reverse the validator, forge a VIP ticket signature

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/kara-express/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Tickets look like `KE|HHMM|DEST|sig`, where `sig` is a homemade
> keyed hash over `KE|HHMM|DEST` using an hour-dependent key. The `validator`
> binary embeds the whole per-hour key table, so I reverse it, recompute the
> signature for `DEST=KARA-VIP` at a valid slot, and hand the gate a ticket it
> accepts. **Flag:** `NCTF{…}`.

## 1. Briefing

A ticketing service. `horaires.csv` lists the schedule, including a VIP slot, and
the gate validates tickets of the form `KE|HHMM|DEST|sig`. I need a VIP ticket I
never bought.

## 2. Analysis

The signature is a custom djb2-style rolling hash, keyed per hour:

```python
def sig(hhmm, dest):
    hour = int(hhmm[:2])
    body = f"KE|{hhmm}|{dest}".encode()
    key = KEYS[hour]          # hour-dependent key byte
    h = 5381
    for c in body:
        h = ((h << 5) + h) + (c ^ key)
    return format(h & 0xFFFFFFFF, "08x")
```

There's no real secret here — it's "security by the key table being hidden in a
binary". The `validator` binary carries `KEYS`, so once I reverse it, I can sign
anything.

## 3. Exploitation

1. Pull the VIP slot (`HHMM`) from `horaires.csv`.
2. Reverse `validator` to recover the per-hour `KEYS` table (and confirm the hash
   construction above).
3. Recompute the signature for `KE|HHMM|KARA-VIP` with `KEYS[hour]` and assemble
   the ticket:

```python
hhmm = "<VIP slot>"; dest = "KARA-VIP"
ticket = f"KE|{hhmm}|{dest}|{sig(hhmm, dest)}"
```

The gate recomputes the same hash, it matches, and the VIP ticket is accepted.

## 4. Flag

```text
NCTF{…}
```

## 5. Lessons & remediation

- **A keyed hash is only as secret as its key.** Shipping `KEYS` inside a client
  binary is not secrecy — it's obfuscation, and it reverses in minutes.
- **Use a real MAC** (HMAC-SHA256) with a server-side key the client never sees,
  and verify server-side. The client should never be able to mint valid tickets.
