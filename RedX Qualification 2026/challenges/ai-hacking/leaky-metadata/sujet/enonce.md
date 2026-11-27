# Leaky Metadata

- **Category:** AI Hacking
- **Author:** unknown
- **Difficulty:** —
- **Points:** 100 (dynamic, initial 500)
- **Solves:** 135
- **Instance:** none

## Statement

During an internal audit, our ML team exported a small classifier used to
approve access requests. The model was supposed to contain no secrets, but
the deployment pipeline may have left something behind.

Recover the sealed token from flag.enc.

Python 3 with the `cryptography` package is enough. Never torch.load() a
checkpoint you don't trust - pickle can run code.

Flag format: `RxR{...}`
