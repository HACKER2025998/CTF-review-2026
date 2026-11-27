# PAL — Maintenance : du path traversal au SUID root

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/pal-maintenance/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un path traversal sur `/rapport?id=` me livre `agent.conf`. Un portail
> « badge » calcule un PIN que je dérive, et le couple seed+PIN donne le mot de
> passe SSH de `pal-ops`. En local, un binaire SUID `pal_check` lit un fichier cible
> arbitraire : je pointe `TARGET=/root/flag.txt`. **Flag :** `NCTF{…}`.

## 1. Path traversal

Le endpoint de rapports concatène un identifiant à un chemin sans contrôle :

```
/rapport?id=../../../../opt/pal/agent.conf
```

Je récupère `agent.conf` — il contient une graine (`seed`) et la logique du badge.

## 2. Badge gate → PIN

L'accès suivant est protégé par un « badge » : un PIN dérivé de la graine lue.
Je reproduis le calcul en local et j'obtiens le PIN.

## 3. SSH pal-ops

Le mot de passe de `pal-ops` est dérivé de `seed` + `PIN`. Je le reconstitue et je
me connecte en SSH.

## 4. SUID vers root

Sur la machine, `pal_check` est SUID root et lit un fichier passé en paramètre :

```bash
TARGET=/root/flag.txt ./pal_check     # lit le fichier avec les droits root
```

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- **Confiner `id=`** (pas de `..`, racine verrouillée) : la fuite de `agent.conf`
  débloque toute la chaîne.
- **Un SUID qui lit un chemin arbitraire = lecture root arbitraire.** Fixer la
  cible, laisser tomber les privilèges, et ne jamais dériver un mot de passe SSH
  d'une graine lisible.
