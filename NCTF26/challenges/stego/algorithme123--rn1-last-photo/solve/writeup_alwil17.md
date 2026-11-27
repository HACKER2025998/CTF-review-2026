# RN1 — Dernière photo : XMP, chunk APP2 chiffré et ZIP à reconstituer

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/rn1-last-photo/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Une photo JPEG. Le commentaire `COM` est un leurre ; les vraies
> données sont dans le **XMP** (GPS, numéro de séquence, indice de mot de passe) et
> dans un chunk **APP2** marqué `RN1ENC1`. Je XOR le chunk APP2 avec la clé dérivée
> de l'indice pour obtenir un ZIP, et j'assemble les parties `01`+`02`+`03`.
> **Flag :** `NCTF{…}`.

## 1. Écarter le leurre

Le segment `COM` du JPEG contient un message qui n'apporte rien — un leurre
classique. Les données utiles sont ailleurs.

## 2. Lire le XMP

Les métadonnées XMP fournissent trois choses : des coordonnées **GPS**, un numéro
de **Sequence** (il y a plusieurs photos à ordonner), et un **indice de mot de
passe** pour la partie chiffrée.

## 3. Déchiffrer le chunk APP2

Un segment `APP2` commence par le marqueur `RN1ENC1`. Je le XOR avec la clé dérivée
de l'indice XMP, ce qui produit un **fragment de ZIP** :

```python
blob = app2_payload[len(b"RN1ENC1"):]
part = bytes(b ^ key[i % len(key)] for i, b in enumerate(blob))
```

## 4. Assembler

Chaque photo (ordonnée par `Sequence`) donne un fragment `01`, `02`, `03`. Je les
concatène dans l'ordre pour reformer le ZIP complet, que j'ouvre pour lire le flag.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons

- **Un JPEG a plusieurs cachettes** : `COM`, `XMP`, `APPn`. Il faut inspecter tous
  les segments (`exiftool`, lecture binaire) plutôt que se fier au commentaire
  visible, souvent un leurre.
