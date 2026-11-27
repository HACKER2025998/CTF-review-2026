# vault-reuse — an Ansible Vault password derived from public metadata

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/vault-reuse/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — The Ansible Vault that "protects" `secrets.yml` gets its password
> from a script, and that script derives the password from **committed, public**
> metadata (`project` and `deploy_env` in `group_vars/all.yml`). Anyone with the
> repo can reproduce the exact password, so I regenerate it and decrypt the vault.
> **Flag:** inside the decrypted `secrets.yml`.

## 1. Briefing

An Ansible project with an `ansible-vault`-encrypted `secrets.yml`. The config
points the vault password at a script instead of a prompt:

```ini
# ansible.cfg
vault_password_file = bin/get-vault-pass.sh
```

## 2. Analysis

The script is the whole vulnerability:

```sh
# bin/get-vault-pass.sh
proj=$(awk '/^project:/ {print $2}' group_vars/all.yml)
env=$(awk '/^deploy_env:/ {print $2}' group_vars/all.yml)
printf '%s-%s-vault-v1' "$proj" "$env"
```

Both `project` and `deploy_env` live in `group_vars/all.yml`, which is committed
in the clear. So the vault password is a deterministic function of values anyone
reading the repo already has — the encryption protects nothing.

## 3. Exploitation

```bash
# reproduce the password from the public metadata
proj=$(awk '/^project:/ {print $2}' group_vars/all.yml)
env=$(awk '/^deploy_env:/ {print $2}' group_vars/all.yml)
printf '%s-%s-vault-v1' "$proj" "$env" > /tmp/vp

# decrypt the "protected" secrets
ansible-vault view --vault-password-file /tmp/vp secrets.yml
```

The decrypted `secrets.yml` holds the flag.

## 4. Flag

```text
NCTF{…}
```

## 5. Lessons & remediation

- **A secret derived from non-secrets is not a secret.** The vault password must
  come from something not in the repo — a real secret manager, a prompt, or an
  env var injected at deploy time.
- **Don't commit the key-derivation inputs** next to the ciphertext. If
  `group_vars/all.yml` is public, nothing derived from it can guard `secrets.yml`.
- Rotate the vault password and re-encrypt once the derivation is known.
