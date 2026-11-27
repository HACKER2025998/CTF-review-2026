# Coupure à Sokodé — exfiltration DNS dans un incident SCADA

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/coupure-sokode/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un bundle d'incident (pcap + logs auth/SCADA + traces USB). La
> timeline pointe un login anormal suivi d'un `COIL_WRITE` ; les pistes USB/FTP sont
> des leurres. Les vraies données partent en **exfiltration DNS** :
> `pXX.<chunk>.exfil.ppg-lab.tg`. Je trie les sous-domaines par index `pXX`, je
> concatène les chunks et je décode en base32. **Flag :** `NCTF{…}`.

## 1. Inventaire

Le ZIP contient un pcap, des logs d'authentification et SCADA, et des traces USB.
Beaucoup de bruit — il faut une timeline.

## 2. Timeline

Je corrèle les logs : un **login anormal** précède immédiatement un ordre
`COIL_WRITE` sur l'automate. Les événements USB et un transfert FTP sont des
**leurres** placés pour détourner l'analyse.

## 3. L'exfiltration DNS

Dans le pcap, une rafale de requêtes DNS vers des sous-domaines de la forme :

```
pXX.<chunk>.exfil.ppg-lab.tg
```

`pXX` est un index d'ordonnancement, `<chunk>` un fragment de données. Je trie par
`pXX`, je concatène les `<chunk>`, et je décode l'ensemble en **base32** :

```python
chunks = sorted(dns_labels, key=lambda r: r.idx)
data   = base64.b32decode("".join(c.chunk for c in chunks).upper())
```

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons & remédiation

- **Le DNS est un canal d'exfiltration** : surveiller le volume et l'entropie des
  requêtes, bloquer la résolution récursive vers des domaines non approuvés.
- En forensics, **dater d'abord** : la timeline écarte les leurres (USB, FTP) et
  relie le login au `COIL_WRITE`.
