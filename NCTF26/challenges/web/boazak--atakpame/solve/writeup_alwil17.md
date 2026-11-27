# Atakpamé — un flag caché en zéro-width dans une annonce

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/atakpame/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — La page affiche une annonce qui semble anodine, mais le bloc
> `#annonce` contient des caractères invisibles : `U+200B` pour un `0`, `U+200C`
> pour un `1`. Je récupère ces bits, je les regroupe par 8, et j'obtiens de
> l'ASCII — le flag. Le commentaire HTML bien visible est un leurre. **Flag :**
> `NCTF{…}`.

## 1. Briefing

Challenge web de la finale. La page a l'air vide de tout secret, et un
commentaire HTML pointe gentiment vers une fausse piste.

## 2. Reconnaissance

En lisant la source, deux choses sautent aux yeux : un commentaire HTML
« utile » (trop beau pour être vrai) et un bloc `#annonce` dont le texte copié
fait plus d'octets qu'il n'affiche de caractères. Signe classique de caractères
zéro-width glissés entre les lettres visibles.

## 3. Analyse

Les caractères invisibles encodent des bits :

- `U+200B` (zero-width space) → `0`
- `U+200C` (zero-width non-joiner) → `1`

Je ne garde que ces deux points de code, je les traduis en bits, je découpe par
paquets de 8, et chaque octet est un caractère ASCII du flag.

## 4. Exploitation

```python
raw = open("annonce.html", encoding="utf-8").read()
bits = "".join("0" if c == "​" else "1" for c in raw if c in "​‌")
flag = "".join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits) - len(bits) % 8, 8))
print(flag)   # NCTF{…}
```

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- **Toujours comparer le texte affiché et le texte source** : un écart de taille
  trahit des caractères invisibles.
- **Ignorer le leurre évident** : le commentaire HTML était là pour attirer le
  regard ; le vrai message était dans ce que l'œil ne voit pas.
- Côté défense, normaliser/supprimer les caractères de contrôle Unicode dans tout
  contenu rendu évite ce canal caché.
