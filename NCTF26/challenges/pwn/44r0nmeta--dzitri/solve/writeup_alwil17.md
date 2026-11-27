# Dzitri — rejouer Heartbleed sur un faux TLS pour fuiter le flag

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/dzitri/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Le service sur le port `4433` reproduit Heartbleed (CVE-2014-0160) :
> une requête *Heartbeat* annonce une longueur de payload, et le serveur la croit
> sur parole. J'annonce 4096 octets mais je n'en envoie qu'un : le serveur
> complète sa réponse avec la mémoire adjacente, où se trouve le flag. **Flag :**
> `NCTF{…}`.

## 1. Briefing

Un service réseau qui parle un TLS minimal. Il s'annonce `OpenSSL/1.0.1f` — la
version emblématique de Heartbleed. Autant dire que le thème est posé.

## 2. Reconnaissance

Le protocole est un TLS simplifié :

- un enregistrement dont le premier octet est `22` (Handshake) déclenche un
  *Server Hello* ;
- un enregistrement de type `24` (Heartbeat) part dans le handler vulnérable.

## 3. La vulnérabilité

Après l'en-tête TLS de 5 octets, une requête Heartbeat ressemble à :

```
[ type:1 ][ payload_length:2 ][ payload... ]
```

Le serveur fait confiance à `payload_length` sans vérifier qu'il correspond à la
taille réellement reçue :

```python
if payload_length > len(actual_payload):
    over_read = payload_length - len(actual_payload)
    response_data = actual_payload + MEMORY_BUFFER[:over_read]
```

C'est le bug d'origine : un **over-read mémoire**. Je demande plus que ce que
j'envoie, le serveur me rend ce qui traîne après mon payload.

## 4. Exploitation

1. Envoyer un Handshake bidon pour amorcer la connexion.
2. Envoyer un Heartbeat qui **annonce 4096 octets** mais n'en envoie qu'**un**.
3. Lire la réponse : elle contient le bloc mémoire leaké, flag compris.

```text
type=1, payload_length=4096, payload="A"
```

Un petit script envoie le handshake, forge le Heartbeat déséquilibré et extrait
le flag avec `NCTF\{[^}]+\}`.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- **Toujours valider les longueurs déclarées** par rapport aux données réellement
  reçues — c'est précisément le correctif d'OpenSSL 1.0.1g.
- Ne jamais renvoyer un tampon mémoire sans l'avoir initialisé/bornes vérifiées ;
  un `payload_length` attaquant ne doit jamais piloter une copie.
