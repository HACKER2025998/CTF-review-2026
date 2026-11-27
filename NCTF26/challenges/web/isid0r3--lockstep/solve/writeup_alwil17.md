# Lockstep — SSRF Gopher vers Redis pour voler la session admin

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/lockstep/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — `/preview` accepte `gopher://`. Je contourne le filtre anti-locale
> avec un encodage IPv4 hérité, puis je parle à Redis en RESP via Gopher : `KEYS *`
> révèle `adminsession`, `GET` me donne le SID admin. Je colle ce SID dans mon
> cookie et `/admin` affiche le flag. **Flag :** `NCTF{…}`.

## 1. Reconnaissance

Je me connecte (`amina` / `welcome2026`). `/admin` renvoie 403 — il faut une
session admin. Le formulaire `/preview` va chercher l'URL fournie et supporte non
seulement `http(s)://` mais aussi **`gopher://`**.

## 2. Le filtre

`gopher://127.0.0.1:6379/` → « Hôte bloqué » (`127.0.0.1` et `localhost` rejetés).

## 3. Contourner

Comme pour LinkCard, le filtre s'appuie sur `ipaddress.ip_address()` et ne voit que
les notations strictes. J'utilise un encodage hérité : `2130706433`,
`0x7f000001`, `127.1`, `0177.0.0.1`.

## 4. Parler à Redis via Gopher

Gopher envoie des octets bruts à un socket TCP. Redis parle RESP, terminé par CRLF
(`%0D%0A` en URL-encoding). Je liste les clés :

```
gopher://0x7f000001:6379/_KEYS *%0D%0A
```

Le sélecteur Gopher est URL-décodé puis envoyé au socket. Je découvre une clé :
`adminsession`.

## 5. Récupérer le SID admin

```
gopher://0x7f000001:6379/_GET adminsession%0D%0A
```

La réponse contient le SID admin (ex. `adm_7d9f2a8c4b1e6f30`).

## 6. Usurper la session

Je mets cette valeur dans mon cookie `sid` et je visite `/admin`. Le flag s'affiche.

## 7. Flag

```text
NCTF{…}
```

## 8. Leçons & remédiation

- **Restreindre les schémas** à `http`/`https` : `gopher://` transforme une SSRF en
  écriture de commandes arbitraires sur n'importe quel service TCP interne.
- **Redis sans auth sur le loopback** reste joignable par SSRF ; exiger un mot de
  passe (`requirepass`) et isoler le service. Même remède de normalisation d'IP
  que pour [LinkCard](/ctf-writeups/posts/linkcard/).
