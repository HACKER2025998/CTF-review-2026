# Leaky Metadata — Write-up

- **Category:** AI Hacking
- **Flag:** `RxR{m3t4d4t4_n3v3r_l13s}`

## TL;DR

A PyTorch checkpoint (`model.pt`) leaks everything needed to rebuild the Fernet
key that "sealed" the flag. The CI log states the key-derivation function, the
build manifest gives the `build_id`, and the checkpoint's own `meta` dict carries
the `commit_salt`. Two ciphertexts are shipped: one is a decoy sealed with the
`staging_key`, the other is the real flag sealed with the derived key.

## Files

- `model.pt` — a PyTorch checkpoint (really a ZIP archive).
- `flag.enc` — two `gAAAAA…` tokens (Fernet), one per line.
- `README.txt` — "recover the sealed token from flag.enc. Not every key you find
  is the right key."

## Step 1 — unzip the checkpoint and read the metadata

```bash
unzip model.pt -d model
```

Interesting extra files:

`model/extra/deploy.log`
```
step=seal_artifact kdf="fernet_key = urlsafe_b64encode(sha256(build_id + ':' + commit_salt).digest())"
WARN build_manifest.json still lists staging_key (CI-4471)
```

`model/extra/build_manifest.json`
```json
{
  "build_id": "rel-2026.04.27-b4471",
  "staging_key": "1flx3mAm_bnaSCx258i45aZVymCW0Pf0Qo9p2-Q_Cn0=",
  "notes": "secrets scrubbed from log; commit_salt moved to checkpoint meta"
}
```

The `commit_salt` was moved into the checkpoint's `meta` dict. Unpickle safely
(stub out the tensor rebuild — never `torch.load` an untrusted checkpoint):

```python
import pickle, collections
class Any:
    def __init__(s,*a,**k): pass
    def __setitem__(s,k,v): pass
    def __setstate__(s,st): pass
    def __call__(s,*a,**k): return Any()
class U(pickle.Unpickler):
    def find_class(self,m,n):
        return collections.OrderedDict if n=="OrderedDict" else Any
    def persistent_load(self,pid): return Any()
meta = U(open("model/data.pkl","rb")).load()["meta"]
# meta['export']['commit_salt'] == '7c1e09d4ab52f3e8'
```

## Step 2 — derive the Fernet key

```
fernet_key = urlsafe_b64encode( sha256( build_id + ':' + commit_salt ).digest() )
build_id    = "rel-2026.04.27-b4471"
commit_salt = "7c1e09d4ab52f3e8"
```

```python
import hashlib, base64
key = base64.urlsafe_b64encode(
    hashlib.sha256(b"rel-2026.04.27-b4471:7c1e09d4ab52f3e8").digest())
# -> ueHrBVIxWsJxcpc7MbpNLj_RokCrcCaBjEhXlfsn0T0=
```

## Step 3 — decrypt (mind the decoy)

`flag.enc` has two tokens. The derived key only authenticates **one** of them
(Fernet verifies an HMAC, so the wrong key raises `InvalidToken`). The other
token decrypts with the `staging_key` and is a decoy — exactly the "not every key
you find is the right key" hint.

```python
from cryptography.fernet import Fernet
derived = b"ueHrBVIxWsJxcpc7MbpNLj_RokCrcCaBjEhXlfsn0T0="
staging = b"1flx3mAm_bnaSCx258i45aZVymCW0Pf0Qo9p2-Q_Cn0="
for line in open("flag.enc"):
    t = line.strip().encode()
    for k in (derived, staging):
        try: print(Fernet(k).decrypt(t)); break
        except Exception: pass
```

Output:

```
line 1 [staging] -> RxR{n0t_th1s_0n3_st4g1ng_k3y_1s_4_d3c0y}   # DECOY
line 2 [derived] -> RxR{m3t4d4t4_n3v3r_l13s}                   # REAL
```

## Flag

```
RxR{m3t4d4t4_n3v3r_l13s}
```

> Decoy to avoid: `RxR{n0t_th1s_0n3_st4g1ng_k3y_1s_4_d3c0y}` (sealed with the
> `staging_key`).
