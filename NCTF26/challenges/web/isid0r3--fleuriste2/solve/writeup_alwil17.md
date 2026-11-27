# Fleurs & Co — de la LFI au PIN de la console Werkzeug

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/fleuriste/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un paramètre `desc=` charge un fichier de description : LFI par
> traversal. L'app Flask tourne en `debug=True` avec la console `/console`
> protégée par PIN. Le PIN Werkzeug est déterministe : je récupère tous ses
> ingrédients via la LFI (user, chemin de Flask, machine-id, cgroup, MAC), je
> recalcule le PIN, j'ouvre la console et je lis le flag. **Flag :** `NCTF{…}`.

## 1. La LFI

Je choisis un bouquet puis un type de carte. L'URL devient
`/carte?bouquet=roses-rouges&desc=amour.txt` — `desc` charge un fichier texte. Je
tente un traversal :

```
/carte?bouquet=roses-rouges&desc=../../../../etc/passwd
```

`/etc/passwd` s'affiche. LFI confirmée, et je note l'utilisateur qui exécute l'app
(ex. `fleuriste`).

## 2. Le mode debug

`/estimation?bouquet=roses-rouges&qty=abc` (valeur non numérique) déclenche une
page d'erreur **Werkzeug** complète : stack trace, chemins absolus, code source.
Je relève le chemin exact de `flask/app.py` (ex.
`/usr/local/lib/python3.12/site-packages/flask/app.py`). La console `/console`
existe, protégée par PIN.

## 3. Collecter les ingrédients du PIN

Le PIN Werkzeug est dérivé d'éléments déterministes. Via la LFI (`desc=`) je lis :

- l'utilisateur de l'app — déjà via `/etc/passwd` ;
- le chemin du `app.py` **de la librairie Flask** — via la stack trace ;
- `/etc/machine-id` (ou `/proc/sys/kernel/random/boot_id` à défaut) ;
- `/proc/self/cgroup` — le segment après le dernier `/` de la 1ʳᵉ ligne, à
  concaténer au machine-id ;
- `/sys/class/net/eth0/address` — l'adresse MAC.

## 4. Lire l'algorithme exact

Plutôt que me fier à un write-up externe peut-être périmé, je récupère
`werkzeug/debug/__init__.py` via la même LFI (même dossier `site-packages`) pour
confirmer l'algo de cette version (SHA-1 vs MD5, ordre des éléments).

## 5. Calculer le PIN et exécuter

Je reproduis la génération du PIN en local avec ces valeurs, je le saisis sur
`/console`, la console Python interactive s'ouvre. Le flag a un nom aléatoire
(`/flag_<hex>.txt`) :

```python
import os; os.listdir('/')
```

J'identifie le fichier et je lis son contenu.

## 6. Flag

```text
NCTF{…}
```

## 7. Leçons & remédiation

- **Jamais `debug=True` en production.** La console Werkzeug est une RCE dès que
  le PIN est reconstituable — et tous ses ingrédients fuient via une simple LFI.
- **Confiner les chemins** (`desc=`) : pas de `..`, racine verrouillée, et ne
  jamais exposer une page d'erreur qui dévoile chemins et code source.
