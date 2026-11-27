# KDS — un commit Git qui cache des octets dans l'indentation

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/kds-whitespace-commit/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un dépôt Git fourni en tarball. Un commit innocent
> (`chore: normalize indent`) change l'indentation d'un fichier de config. L'astuce :
> `git diff -w` masque ces changements. En regardant le diff **sans** `-w`,
> l'indentation (espace = 0, tab = 1) code le flag. **Flag :** `NCTF{…}`.

## 1. Le dépôt

J'extrais `kds-policy.git.tgz` et je parcours l'historique. Un commit attire
l'attention : `chore: normalize indent` sur `policy/indent.conf` — exactement le
genre de changement qu'on survole sans lire.

## 2. Le piège du -w

Par défaut beaucoup d'outils ignorent les blancs. Il faut forcer l'affichage des
changements d'espacement :

```bash
git show <commit> -- policy/indent.conf      # sans -w : on voit les tabs/espaces
```

Les lignes modifiées ne diffèrent **que** par leur caractère d'indentation :
tantôt espace, tantôt tabulation.

## 3. Décoder

Convention **espace = 0, tab = 1**, un bit par ligne, regroupés en octets :

```python
bits = "".join("1" if l.startswith("\t") else "0" for l in changed_lines)
flag = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits)//8*8, 8))
```

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons

- **`-w` cache l'attaque.** En revue de code, les changements purement
  d'espacement méritent un regard : ils peuvent encoder des données.
- Un hook de normalisation d'indentation est le camouflage parfait pour un payload
  stégo.
