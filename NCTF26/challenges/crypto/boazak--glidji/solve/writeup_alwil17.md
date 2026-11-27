# Glidji — length-extension SHA-256 + réutilisation de keystream

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/glidji/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — La passerelle signe les commandes avec un MAC de type `SHA256(secret || message)`, vulnérable à une extension de longueur SHA-256. En forgeant `role=admin`, le coffre renvoie deux chiffrés. La bannière publique fournit un texte clair connu de même longueur que `banner_ct`, ce qui permet de récupérer le keystream et de déchiffrer `secret_ct` par XOR. Le flag est `NCTF{0b72…}`.


## 1. Briefing

### Description

> La passerelle de Glidji exécute des commandes signées (MAC) et donne accès à un coffre d'archives pour les administrateurs.
>
> « Chaque commande est authentifiée par un MAC. La bannière du coffre, elle, est publique. »

### Assets fournis

| Fichier | Taille | SHA-256 | Type |
|---------|--------|---------|------|
| aucun | — | — | Service web distant |

Le dossier de travail contenait aussi `cinkasse_annuaire_2026.pdf` (52 octets) et `procedure_onboarding.docx` (27 octets). Ces deux fichiers sont des leurres explicites (`annuaire decoy`, `decoy onboarding`) et n'ont pas été utilisés.

### Cible

| Élément | Valeur |
|---------|--------|
| URL | `https://irgnsqdnlxqsoi2z.t.ctf.tg/` |
| Credentials | aucun |
| Format du flag | `NCTF{...}` |

### Contraintes

- Instance distante limitée dans le temps.
- Accès HTTP(S) uniquement.

## 2. Environnement et prérequis

| Outil | Version | Usage |
|-------|---------|-------|
| Python | 3.14.9 | Script d'exploitation |
| requests | 2.34.2 | Requêtes HTTP |
| hashpumpy | 1.2 | Extension de longueur SHA-256 |
| curl | 8.21.0 | Reconnaissance manuelle |

```bash
python3 -m pip install requests hashpumpy
```

Le scan réseau initial de `10.100.13.101` a été abandonné : les ports étaient filtrés et l'accès direct expirait. L'instance HTTPS fournie a donc servi de cible pour toute la suite.

## 3. Reconnaissance

### 3.1 Surface initiale

**Objectif :** identifier les routes exposées et le format des données.

```bash
curl -sS -i https://irgnsqdnlxqsoi2z.t.ctf.tg/
```

```text
HTTP/2 200
server: nginx/1.27.5
content-type: text/html; charset=utf-8

<html><body><h1>Glidji</h1><p>/token (commande signee par defaut), /cmd?msg=&lt;hex&gt;&amp;mac=&lt;hex&gt;. Banniere publique via /banner.</p></body></html>
```

**Interprétation :** trois routes sont annoncées : `/token`, `/cmd` et `/banner`. Les paramètres `msg` et `mac` sont attendus en hexadécimal.

### 3.2 Récupération du jeton par défaut

**Objectif :** obtenir un message signé valide et observer son format.

```bash
curl -sS https://irgnsqdnlxqsoi2z.t.ctf.tg/token
```

```text
{"msg": "726f6c653d6775657374", "mac": "ddeb7ec7f98234ab15e592f1d37606b61de57b5836ab0f20c524ea4cd1944610"}
```

Décodage du message :

```text
726f6c653d6775657374  ->  role=guest
```

**Interprétation :** le serveur signe une chaîne de type `role=guest` avec un MAC de 32 octets. Le contrôle d'accès semble reposer sur ce champ.

### 3.3 Validation du jeton et bannière publique

**Objectif :** confirmer le comportement de `/cmd` et récupérer la bannière en clair.

```bash
curl -sS 'https://irgnsqdnlxqsoi2z.t.ctf.tg/cmd?msg=726f6c653d6775657374&mac=ddeb7ec7f98234ab15e592f1d37606b61de57b5836ab0f20c524ea4cd1944610'
curl -sS https://irgnsqdnlxqsoi2z.t.ctf.tg/banner
```

```text
{"role": "guest", "note": "acces standard"}
{"banner": "=== COFFRE GLIDJI v1 : archives operationnelles internes ===  "}
```

**Interprétation :** le MAC valide donne un accès `guest`. Le message signé est interprété comme des paramètres clé-valeur. La bannière est publique, donc son texte clair est connu.

### 3.4 Résumé des constats

| # | Constat | Preuve | Pertinence |
|---|---------|--------|------------|
| 1 | Message signé `role=guest` | `/token` | Point de départ pour forger un rôle |
| 2 | MAC de 32 octets | `/token` | Compatible SHA-256 |
| 3 | `msg` et `mac` en hexadécimal | page d'accueil | Format des requêtes |
| 4 | Bannière publique connue | `/banner` | Texte clair pour analyser un chiffrement |
| 5 | Contrôle d'accès basé sur `role` | `/cmd` | Cible de la forgery |

## 4. Analyse

### 4.1 Hypothèse

Le MAC pourrait être `SHA256(secret || msg)` plutôt qu'un HMAC. Ce schéma est vulnérable à une extension de longueur : connaissant `SHA256(secret || msg)` et la longueur du secret, il est possible de calculer le MAC de `secret || msg || padding || append` sans connaître `secret`.

### 4.2 Validation

Le MAC a été recalculé avec `hashpumpy` pour plusieurs longueurs de secret, en ajoutant `&role=admin`. Seule la longueur 16 a été acceptée par `/cmd` :

```text
n=16  status 200  {"vault": {"banner_ct": "...", "secret_ct": "..."}}
n=0   status 403  {"error": "mac invalide"}
n=8   status 403  {"error": "mac invalide"}
n=32  status 403  {"error": "mac invalide"}
```

**Conclusion :** le serveur utilise bien un MAC à préfixe secret de 16 octets, construit avec SHA-256. Le message forgé contient `role=guest`, le padding SHA-256, puis `&role=admin`. Le parseur retient la dernière valeur de `role`, ce qui donne un accès administrateur.

### 4.3 Cause racine

Le schéma `SHA256(secret || message)` n'est pas un MAC sûr. SHA-256 est un algorithme de Merkle-Damgård : l'état interne après le premier bloc peut être repris pour hacher la suite. Le padding ajouté par l'implémentation est précisément ce qui rend l'attaque possible.

De plus, le coffre chiffre la bannière et le secret avec le même keystream. La bannière étant publique, elle fournit un couple clair/chiffré connu, donc le keystream. Le secret est ensuite déchiffré par simple XOR.

## 5. Exploitation

### Étape 1 : forger un MAC administrateur

**Objectif :** transformer `role=guest` en `role=admin` avec un MAC valide.

```python
import hashpumpy

msg = bytes.fromhex("726f6c653d6775657374")
mac = "ddeb7ec7f98234ab15e592f1d37606b61de57b5836ab0f20c524ea4cd1944610"
new_mac, new_msg = hashpumpy.hashpump(mac, msg, b"&role=admin", 16)
print(new_msg.hex())
print(new_mac)
```

Résultat :

```text
726f6c653d677565737480000000000000000000000000000000000000000000000000000000000000000000000000d026726f6c653d61646d696e
2d666ff6299490531fbfa1c6a9cf741348f05be538f018b925be5e4e5fdc86b1
```

Le message forgé fait 59 octets. Il contient `role=guest`, le padding SHA-256 (`80 00...` puis la longueur en bits), puis `&role=admin`.

### Étape 2 : obtenir le coffre

**Objectif :** envoyer le message forgé et récupérer les données chiffrées.

```bash
curl -sS 'https://irgnsqdnlxqsoi2z.t.ctf.tg/cmd?msg=<NEW_MSG_HEX>&mac=<NEW_MAC>'
```

Résultat :

```json
{
  "vault": {
    "banner_ct": "66510cc433b07cb2792ba4560fd9ffde69296723300e28a4b888afafc98bd2c249d2dac3feb7d944d7e9aa5c92c8ab94fbd5b8892f63fa3b56a5247051ec",
    "secret_ct": "152f65a20bcf58c31957e02722f583a7456a257375026af7acdff0f58793"
  }
}
```

`banner_ct` fait 62 octets, exactement la longueur de la bannière publique. Cela suggère un chiffrement par flot ou un XOR avec un keystream réutilisé.

### Étape 3 : récupérer le keystream

**Objectif :** utiliser la bannière connue pour retrouver le keystream.

```python
banner = b"=== COFFRE GLIDJI v1 : archives operationnelles internes ===  "
banner_ct = bytes.fromhex("66510cc433b07cb2792ba4560fd9ffde69296723300e28a4b888afafc98bd2c249d2dac3feb7d944d7e9aa5c92c8ab94fbd5b8892f63fa3b56a5247051ec")
keystream = bytes(c ^ p for c, p in zip(banner_ct, banner))
print(keystream.hex())
```

Résultat :

```text
5b6c31e470ff3af42b6e84114390bb9420091112103408c5caebc7c6bfeea1e226a2bfb19fc3b02bb987cf30feadd8b492bbccec5d0d9f487698194d71cc
```

### Étape 4 : déchiffrer le secret

**Objectif :** appliquer le même keystream au chiffré du secret.

```python
secret_ct = bytes.fromhex("152f65a20bcf58c31957e02722f583a7456a257375026af7acdff0f58793")
secret = bytes(c ^ k for c, k in zip(secret_ct, keystream))
print(secret.decode())
```

Résultat :

```text
NCTF{0b72…}
```

Le secret fait 30 octets et le préfixe du keystream suffit. Le déchiffrement produit un texte ASCII cohérent avec le format du flag.

## 6. Flag

```text
NCTF{0b72…}
```

**Vérification :** le flag a été obtenu par déchiffrement XOR indépendant, avec un keystream dérivé de la bannière publique. Le format `NCTF{...}` est respecté et la chaîne déchiffrée est entièrement ASCII imprimable. Le flag n'a pas été soumis à la plateforme depuis cet environnement.

## 7. Impasse et dépannage

| Tentative | Résultat observé | Raison probable | Pivot |
|-----------|------------------|-----------------|-------|
| Scan de `10.100.13.101` | Ports filtrés, timeouts | Cible non joignable depuis le réseau courant | Utiliser l'instance HTTPS fournie |
| Modification directe de `msg` en `role=admin` | `403 mac invalide` | Le MAC dépend du message | Chercher une faiblesse dans le MAC |
| `hashpumpy` avec une mauvaise longueur de secret | `403 mac invalide` | Longueur de secret incorrecte | Tester les longueurs et retenir 16 |
| Fichiers `annuaire` et `onboarding` locaux | Contenu factice | Leurres volontaires | Ignorer |

## 8. Leçons et remédiation

### Cause racine

Le service construit son MAC avec `SHA256(secret || message)`, un schéma vulnérable à l'extension de longueur. Le même keystream est réutilisé pour chiffrer la bannière publique et le secret, ce qui permet de retrouver le keystream par known-plaintext.

### Recommandations défensives

1. Utiliser un HMAC standard, par exemple `HMAC-SHA256(secret, message)`, et non `SHA256(secret || message)`.
2. Comparer les MAC avec une fonction à temps constant.
3. Ne jamais réutiliser un keystream de chiffrement par flot avec la même clé et le même nonce.
4. Chiffrer chaque donnée avec un nonce/IV aléatoire et authentifier le chiffré (AES-GCM ou ChaCha20-Poly1305).
5. Ne pas exposer de texte clair choisi à côté de données chiffrées avec le même keystream.

### Technique transférable

Lorsqu'un service signe des données avec un hash à préfixe secret et renvoie un couple message/MAC, tester l'extension de longueur. Lorsqu'un service renvoie un chiffré de même longueur qu'une donnée publique, tester la réutilisation de keystream par XOR.

## Annexe A : script complet

```python
#!/usr/bin/env python3
"""Résout Glidji : extension de longueur SHA-256 puis réutilisation de keystream."""

import sys

import hashpumpy
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://irgnsqdnlxqsoi2z.t.ctf.tg"
SECRET_LEN = 16

session = requests.Session()

token = session.get(f"{BASE}/token", timeout=15).json()
old_msg = bytes.fromhex(token["msg"])
old_mac = token["mac"]

new_mac, new_msg = hashpumpy.hashpump(
    old_mac,
    old_msg,
    b"&role=admin",
    SECRET_LEN,
)

response = session.get(
    f"{BASE}/cmd",
    params={"msg": new_msg.hex(), "mac": new_mac},
    timeout=15,
)
response.raise_for_status()
vault = response.json()["vault"]

banner = session.get(f"{BASE}/banner", timeout=15).json()["banner"].encode()
banner_ct = bytes.fromhex(vault["banner_ct"])
secret_ct = bytes.fromhex(vault["secret_ct"])

if len(banner_ct) != len(banner):
    raise SystemExit("longueurs bannière/chiffré incompatibles")

keystream = bytes(c ^ p for c, p in zip(banner_ct, banner))
flag = bytes(c ^ k for c, k in zip(secret_ct, keystream))

print(flag.decode())
```

## Annexe B : preuves brutes

### Jeton par défaut

```json
{"msg": "726f6c653d6775657374", "mac": "ddeb7ec7f98234ab15e592f1d37606b61de57b5836ab0f20c524ea4cd1944610"}
```

### Bannière publique

```json
{"banner": "=== COFFRE GLIDJI v1 : archives operationnelles internes ===  "}
```

### Message forgé

```text
msg = 726f6c653d677565737480000000000000000000000000000000000000000000000000000000000000000000000000d026726f6c653d61646d696e
mac = 2d666ff6299490531fbfa1c6a9cf741348f05be538f018b925be5e4e5fdc86b1
```

### Coffre retourné

```json
{"vault": {"banner_ct": "66510cc433b07cb2792ba4560fd9ffde69296723300e28a4b888afafc98bd2c249d2dac3feb7d944d7e9aa5c92c8ab94fbd5b8892f63fa3b56a5247051ec", "secret_ct": "152f65a20bcf58c31957e02722f583a7456a257375026af7acdff0f58793"}}
```

### Keystream récupéré

```text
5b6c31e470ff3af42b6e84114390bb9420091112103408c5caebc7c6bfeea1e226a2bfb19fc3b02bb987cf30feadd8b492bbccec5d0d9f487698194d71cc
```

### Flag déchiffré

```text
NCTF{0b72…}
```
