# Togocel Legacy — length-extension sur un MAC MD5(key‖msg)

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/togocel-legacy/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Le service authentifie ses messages avec `MAC = MD5(key ‖ msg)` au
> lieu d'un vrai HMAC. C'est vulnérable à une **length-extension** : à partir d'un
> `ISSUE partner` signé, j'ajoute `|escalate=ops` et je recalcule le MAC sans
> connaître la clé (longueur 16 octets). Le `VERIFY` accepte. **Flag :** `NCTF{…}`.

## 1. Le MAC fait maison

Le service signe chaque message par `MD5(key ‖ msg)`. Comme MD5 est une
construction de Merkle–Damgård, connaître `MAC(msg)` et `len(key)` permet de
calculer `MAC(msg ‖ padding ‖ suffixe)` **sans la clé** — c'est la faille de
length-extension.

## 2. Obtenir un couple de base

Je demande un jeton légitime : `ISSUE partner` me renvoie `msg` + son MAC. La clé
fait 16 octets (deviné / confirmé en testant plusieurs longueurs).

## 3. Étendre le message

Avec un outil de length-extension (ex. `hashpumpy`), j'ajoute le suffixe
`|escalate=ops` :

```python
import hashpumpy
new_mac, new_msg = hashpumpy.hashpump(orig_mac, orig_msg, b"|escalate=ops", 16)
# new_msg = orig_msg + glue_padding + b"|escalate=ops"
```

J'envoie `new_msg` + `new_mac` au `VERIFY`.

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons & remédiation

- **Ne jamais utiliser `H(key ‖ msg)` comme MAC.** Utiliser **HMAC**, qui résiste à
  la length-extension par sa double imbrication.
- Un suffixe attaquant (`|escalate=ops`) accepté par le parseur montre aussi qu'il
  faut une grammaire stricte, pas une simple concaténation de champs.
