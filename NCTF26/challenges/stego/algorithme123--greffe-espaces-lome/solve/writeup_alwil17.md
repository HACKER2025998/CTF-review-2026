# Greffe de Lomé — un message caché dans les fins de ligne

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/greffe-espaces-lome/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un arrêté administratif en `.txt` dont les **fins de ligne** portent
> le message : un espace de queue = 0, une tabulation = 1. Je regroupe les bits par
> 8 (MSB d'abord) et je reconstitue le flag. **Flag :** `NCTF{…}`.

## 1. L'indice

Le fichier `arrete-greffe-lome.txt` paraît anodin, mais chaque ligne se termine par
un caractère d'espacement invisible — tantôt une espace, tantôt une tabulation. Un
`cat -A` révèle les `$` (espace) et `^I` (tab) de fin de ligne.

## 2. Décoder

Convention : **espace = 0, tab = 1**. Un bit par ligne, regroupés en octets, MSB en
premier :

```python
bits = "".join("0" if line.rstrip("\n").endswith(" ") else "1"
               for line in open("arrete-greffe-lome.txt"))
flag = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits)-len(bits)%8, 8))
```

## 3. Flag

```text
NCTF{…}
```

## 4. Leçons

- **Les caractères d'espacement invisibles** (espaces de queue, tabulations)
  transportent de l'information sans altérer l'apparence du texte. Un éditeur qui
  affiche les blancs ou `cat -A` les révèle immédiatement.
