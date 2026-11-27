# Big Bang — trois couches cachées dans un fichier texte

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/big-bang/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — `challenge.txt` superpose trois canaux : (a) un indice en caractères
> invisibles sur la ligne de titre, (b) une grille de caractères zéro-width lue en
> colonnes, décodée en base 3 puis XORée, et (c) le flag codé dans les **runs de
> lettres** de chaque ligne, pondérés et XORés avec un hash de clé. La ligne de
> titre contient un **faux flag** pour piéger. **Flag :** `NCTF{…}`.

## 1. Repérer les canaux

Le fichier a l'air d'un texte normal, mais il cache :

1. des caractères **invisibles** (zéro-width) dans l'en-tête et dans le corps ;
2. une information dans le **nombre de lettres** par ligne.

Piège : le flag visible dans le titre est **faux**.

## 2. Couche A — en-tête zéro-width

Sur la ligne de titre, deux caractères invisibles codent des bits (`U+2061`→0,
`U+2064`→1), regroupés en octets.

## 3. Couche B — grille zéro-width en colonnes

Dans le corps, trois symboles invisibles (`U+2062`→0, `U+2063`→1, `U+200D`→2)
forment une grille lue **colonne par colonne**, décodée en base 3 (6 chiffres →
1 octet), puis XORée avec une clé.

## 4. Couche C — runs de lettres

Pour chaque ligne, on compte les **runs** de lettres (`itertools.groupby`), on les
pondère par un vecteur fixe décalé selon le numéro de ligne, modulo 257, puis on XOR
avec `SHA-256(clé)`.

Mon script reproduit les trois couches :

```python
import hashlib, sys
from itertools import groupby

def pack(bits):
    return bytes(int(bits[k:k+8], 2) for k in range(0, len(bits), 8))

def first(head):
    table = {"⁡": "0", "⁤": "1"}
    return pack("".join(table[c] for c in head if c in table))

def second(lines, key):
    table = {"⁢": "0", "⁣": "1", "‍": "2"}
    grid = [[table[c] for c in ln if c in table] for ln in lines]
    h = len(grid); total = sum(len(r) for r in grid)
    seq = "".join(grid[n % h][n // h] for n in range(total))
    vals = [int(seq[n:n+6], 3) for n in range(0, len(seq), 6)]
    return bytes(v ^ key[n % len(key)] for n, v in enumerate(vals))

def third(lines, key):
    w = (7, 2, 9, 4, 11, 3, 8, 5)
    pad = hashlib.sha256(key).digest()
    out = bytearray()
    for r, ln in enumerate(lines):
        runs = [sum(1 for _ in g) for _, g in groupby(c for c in ln if c.isalpha())]
        acc = sum(runs[j] * w[(j + r) % 8] for j in range(8)) % 257
        out.append(acc ^ pad[r % len(pad)])
    return bytes(out)
```

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons

- **Un fichier texte a plus de canaux qu'il n'y paraît** : caractères zéro-width,
  longueurs de lignes, runs de lettres. Un `hexdump` révèle les octets invisibles
  que l'œil ne voit pas.
- Le faux flag du titre rappelle de **tout décoder** avant de valider.
