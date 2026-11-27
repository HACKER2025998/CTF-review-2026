# Tisserands de Dapaong — LSB du canal rouge guidé par un PDF

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/tisserands-dapaong/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un PDF de motifs et une affiche à légende de voyelles disent **où**
> regarder ; le commentaire du PNG pointe le **canal rouge**. J'extrais les LSB du
> canal R (longueur en big-endian, puis motifs UTF-8) et je décode. **Flag :**
> `NCTF{…}`.

## 1. Corréler les indices

Le PDF présente des motifs de tissage ; l'affiche fournit une légende associant des
voyelles aux motifs. Ensemble, ils indiquent la clé de lecture — mais la donnée
brute est dans l'image.

## 2. Le canal rouge

Le commentaire textuel du PNG oriente vers le **canal rouge** : c'est là que sont
cachés les bits.

## 3. Extraire les LSB

Je lis les bits de poids faible du canal R, dans l'ordre des pixels. Le flux
commence par une **longueur** (entier big-endian), suivie des octets du message
(motifs encodés en UTF-8) :

```python
bits = "".join(str(px_r & 1) for px_r in red_channel)
n    = int(bits[:32], 2)                       # longueur BE
data = bytes(int(bits[32+i:32+i+8], 2) for i in range(0, n*8, 8))
print(data.decode("utf-8"))
```

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons

- **LSB sur un seul canal** (ici R) est courant : tester chaque canal séparément.
  Un préfixe de longueur indique un format structuré plutôt qu'un simple texte.
