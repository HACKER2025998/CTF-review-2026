# Defense Web Agbadja — patching a Flask portal without breaking it

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/defense-web-agbadja/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — This is a defense round, not an exploit one. "Agbadja Express"
> ships a deliberately buggy Flask portal, and a judge bot replays the legit
> customer flows and then a set of attacks. I diff the vulnerable source against
> the flows that must keep working, then apply the tightest patch that fixes four
> bugs (SQLi, IDOR, path traversal, SSRF) while keeping every legit flow green.
> Last box standing scores continuous defense points.

## 1. Briefing

Each team gets SSH (`dev` + sudo) on its own box running the portal at
`/srv/app/app.py`. The scoring bot replays these flows, which must never break:

- customer login (`/connexion`)
- invoice list + per-invoice view (`/espace`, `/facture/<id>`)
- admin space (`/admin`)
- terms download (`/telecharger?fichier=conditions.pdf`)
- package tracking (`/suivi?numero=<N>`)

The catch: restarting the instance from the portal **wipes my patch**, so the fix
has to be reapplied after every relaunch.

## 2. Approach

The whole game is *minimal, non-regressing patches*. I keep the vulnerable copy
as `app_original.py` and diff against it, changing only what closes a bug without
altering a legit flow — same password hashing (unsalted sha256, to match the
existing db), same templates, same admin behaviour.

## 3. The four fixes

| # | Route | Bug | Fix |
|---|-------|-----|-----|
| 1 | `/connexion` | SQL injection (string-formatted query) | Parameterised: `execute("... WHERE username=? AND password_hash=?", (u, h(p)))` |
| 2 | `/facture/<fid>` | IDOR (select by `id` only) | Scope to owner: `WHERE id=? AND owner_id=?` |
| 3 | `/telecharger` | Path traversal in `os.path.join(DOCS, user_input)` | Reject `/ \ .. \x00` and dot-names; `realpath` must stay under `DOCS` |
| 4 | `/suivi` | SSRF + path escape via `?url=` and raw `numero` | Drop the attacker-controllable `?url=`; `quote(numero, safe="")` so `../interne/cles` becomes `%2E%2E%2F…` |

Nothing else is touched.

## 4. Deploy & verify

```bash
./solve.sh                       # dev@<box> — install the patched app.py
./solve.sh --verify-only         # re-run checks without re-uploading
```

The script SSHes in, backs up the original once, installs the patch (gunicorn
`--reload` swaps workers in ~2 s), then runs 11 checks from the box's own
localhost: 3 legit flows, 4 attack payloads, and 4 session-based authz checks
using cookies forged with `/srv/app/secret/session.key`. All green → click
**« Vérifier cette boîte »** to lock the validation.

## 5. Lessons

- **Patch to the contract, not to your taste.** The legit flows are the spec; the
  smallest change that keeps them green and kills the bug is the right one.
- **The classics still win.** Parameterised queries, owner-scoped lookups,
  confined file paths, and no attacker-controlled fetch URLs close the whole set.
- **Persistence matters in defense rounds.** A patch that a relaunch wipes is
  worth nothing unless you automate reapplying it.
