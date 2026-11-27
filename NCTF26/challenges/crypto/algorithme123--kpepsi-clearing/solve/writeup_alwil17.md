# Kpéssi Clearing — réutilisation de nonce ECDSA

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/kpepsi-clearing/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Deux transactions signées ECDSA partagent le même `r` dans
> `transactions.log` : même nonce `k`. À partir des deux signatures je récupère `k`,
> puis la clé privée `d`. Je signe alors un ordre légitime vers `NCTF-OPS` et le
> service le valide. **Flag :** `NCTF{…}`.

## 1. L'indice

`transactions.log` contient des transactions signées. Deux d'entre elles ont le
**même `r`** — en ECDSA, `r` ne dépend que du nonce `k`, donc deux `r` égaux = même
`k` réutilisé.

## 2. Récupérer k puis d

Avec deux signatures `(r, s1)` et `(r, s2)` sur les hachés `z1`, `z2` et le même
`k` :

```
k = (z1 - z2) / (s1 - s2)  mod n
d = (s1 · k - z1) / r      mod n
```

```python
k = (z1 - z2) * inverse(s1 - s2, n) % n
d = (s1 * k - z1) * inverse(r, n) % n
```

## 3. Forger un ordre valide

Avec `d`, je signe un body d'ordre `TO=NCTF-OPS REF=NCTF` avec un `TS`/`NONCE`
frais (pour passer l'anti-rejeu) et je l'envoie au `VERIFY` du service, qui
l'accepte.

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons & remédiation

- **Un nonce ECDSA ne doit jamais être réutilisé** : deux signatures sous le même
  `k` révèlent la clé privée. Utiliser un nonce déterministe (RFC 6979) ou un RNG
  cryptographique.
- Horodatage + nonce anti-rejeu ne protègent pas une clé déjà compromise.
