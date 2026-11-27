# Aného manifestd — leak PIE puis écrasement d'un handler

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/aneho-manifestd/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un gestionnaire de notes qui fuit une adresse interne via `show`
> (donc l'adresse de `win` malgré le PIE), et dont `edit_note` déborde un buffer
> `note[32]` jusqu'à un pointeur de fonction `handler`. J'écris l'adresse de `win`
> dans `handler`, j'appelle `run_handler`, et j'obtiens le shell/flag. **Flag :**
> `NCTF{…}`.

## 1. Reconnaissance

Le service propose `add`, `show`, `edit_note`, `run_handler`. Le binaire est en PIE,
donc je n'ai pas d'adresse fixe au départ.

## 2. Fuite de l'adresse

`add` puis `show` renvoie plus que ma note : la lecture déborde et laisse fuir une
adresse interne. À partir d'elle, je calcule la base PIE et donc l'adresse de la
fonction `win`.

## 3. Débordement vers le handler

`edit_note` écrit dans `note[32]` sans borne : au-delà des 32 octets, j'atteins le
pointeur `handler`. Je le remplace par l'adresse de `win` :

```python
leak   = leak_from_show()
base   = leak - OFF_LEAK
win    = base + OFF_WIN
edit_note(b"A"*32 + p64(win))   # note[32] overflow -> handler = win
run_handler()                   # appelle win()
```

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons & remédiation

- **Borner chaque écriture** (`edit_note`) et **ne jamais sur-lire** dans `show` :
  les deux primitives combinées (leak + overflow) suffisent, même avec PIE.
- Séparer les données des pointeurs de fonction, ou passer par une table d'index
  validée plutôt qu'un pointeur brut écrasable.
