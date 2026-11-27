# NCTF26 — Battlebook opérationnel

> Édition 1.0 — 4 novembre 2026 — 19 catégories / 331 challenges annoncés.
> **Périmètre** : uniquement les challenges, instances et plages réseau autorisés par l'organisateur. Ne jamais tester la plateforme `arena.ctf.tg` elle-même, d'autres équipes ou une infrastructure tierce sans autorisation explicite.
> **Règles à vérifier avant le départ** : aide IA permise ou non, limites de scans, brute force, partage de solutions, jetons KOTH, restrictions réseau.

## Sommaire

1. [Stratégie pour gagner des points](#1-stratégie-pour-gagner-des-points)
2. [Préparation de la machine](#2-préparation-de-la-machine)
3. [Connexions aux instances NCTF26](#3-connexions-aux-instances-nctf26)
4. [Protocole universel de résolution](#4-protocole-universel-de-résolution)
5. [Playbooks des 19 catégories](#5-playbooks-des-19-catégories)
6. [King of the Hill et Boot2Root](#6-king-of-the-hill-et-boot2root)
7. [Méthode d'équipe et gestion du temps](#7-méthode-déquipe-et-gestion-du-temps)
8. [Modèle de write-up](#8-modèle-de-write-up)
9. [Checklist avant lancement](#9-checklist-avant-lancement)
10. [Références utiles](#10-références-utiles)

---

## 1. Stratégie pour gagner des points

| Catégorie | Nombre | Priorité de préparation | Raison |
|---|---:|---|---|
| Crypto | 69 | P1 | 21 % des challenges, beaucoup de petits solveurs automatisables |
| Web | 67 | P1 | 20 %, variété importante de vulnérabilités et de niveaux |
| Reverse | 16 | P2 | Outils communs avec Pwn et Mobile |
| AI | 15 | P3 | Compréhension des consignes et des modèles plutôt qu'outils coûteux |
| Boot2Root | 14 | P2 | Bon terrain pour systèmes/réseaux et méthodologie |
| Cloud | 14 | P2 | IAM, stockage, conteneurs, configurations |
| Stego | 14 | P3 | Triages rapides sur fichiers |
| Supplychain | 14 | P3 | Dépendances, pipelines et artefacts |
| Sysadmin | 13 | P2 | Linux/Windows, permissions, services, logs |
| Pwn | 12 | P2 | Analyse ELF et exploitation mémoire |
| Blockchain | 11 | P4 | Spécialiste EVM/contrats |
| ML | 11 | P4 | Analyse de jeux de données et de modèles |
| Misc | 10 | P3 | Épreuves atypiques, souvent rapides |
| Networking | 10 | P2 | PCAP, protocoles, services réseau |
| PPC | 10 | P3 | Programmation, parsing, algorithmes, automation |
| OSINT | 9 | P3 | Vérification croisée de sources publiques |
| Hardware | 8 | P4 | Firmware, UART, captures logiques |
| Mobile | 8 | P4 | APK, Android, application/reverse |
| Chains | 6 | P4 | Chaînes de résolution multi-étapes; sens exact à confirmer dans les énoncés |
| **Total** | **331** | | |

**Attention** : le nombre de défis ne dit rien sur leurs points ou leur difficulté. Reclasser après découverte du scoreboard. Ne pas tenter les 331 en série : l'objectif est de maximiser les points à l'heure.

### Stratégie d'ouverture (une fois les épreuves disponibles)

1. Pendant les **10–15 premières minutes**, parcourir la liste : catégories, intitulés, points, téléchargements, difficulté apparente et dépendances.
2. Résoudre immédiatement les défis « premiers pas », encodages simples, informations en métadonnées, scripts PPC courts.
3. Attribuer un propriétaire à chaque problème : éviter que 3 joueurs fassent la même reconnaissance.
4. Prioriser **points potentiels / temps estimé**, réévaluer après 20–30 min de blocage.
5. Revenir sur les défis abandonnés lorsqu'un nouvel indice ou write-up autorisé apparaît.
6. Conserver les commandes, scripts, captures et preuves dans un dossier par défi.

---

## 2. Préparation de la machine

### Environnement conseillé

- **Arch Linux** comme poste principal (terminal, Python, scripts, navigateur, Burp/CyberChef).
- **Kali VM** comme boîte à outils secondaire pour les utilitaires moins faciles à installer. Éviter de faire tourner simultanément GNS3, plusieurs Windows Server et plusieurs VM lourdes pendant la compétition.
- **Firefox ou Chromium**, Burp Suite Community (proxy), DevTools, extension JSON si désiré.
- **Git + terminal multiplexeur** (`tmux`) et un gestionnaire de notes Markdown.
- Python en **environnement virtuel**, pas de `sudo pip install` sur Arch.

### Installation de base sur Arch (paquets officiels)

```bash
sudo pacman -Syu
sudo pacman -S --needed \
  git curl wget jq file binutils vim unzip 7zip \
  python python-pip python-pwntools python-sympy python-z3-solver \
  nmap wireguard-tools openssl gdb binwalk wireshark-cli \
  perl-image-exiftool tmux hashcat
```

> Si un paquet est introuvable, vérifier avec `pacman -Ss <mot>` et installer séparément. Sur Arch, le paquet qui fournit l’utilitaire `exiftool` s’appelle **`perl-image-exiftool`**, et `vim` fournit normalement `xxd` ; `wireguard-tools` fournit `wg` et `wg-quick`. `python-pwntools` existe dans les dépôts Arch. Ghidra et SageMath sont **facultatifs** et plus volumineux.

```bash
# Outils spécialisés, au besoin et non obligatoirement la veille
sudo pacman -S --needed ghidra sagemath

# Librairies Python de challenge, sans modifier le Python système
python -m venv ~/ctf-venv
source ~/ctf-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests beautifulsoup4 pycryptodome pillow numpy sympy z3-solver
```

**Nuance importante** : utiliser `python-pwntools` depuis Python système, OU l'installer dans le venv (`pip install pwntools`) si tes scripts y sont lancés. Un paquet système n'est pas forcément visible depuis un venv isolé.

### Boîte à outils web et de référence

- [CyberChef](https://gchq.github.io/CyberChef/) : décodages, conversions, hash, détection d'encodages.
- [Burp Suite Community](https://portswigger.net/burp/communitydownload) : interception et rejeu HTTP.
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) : références par vulnérabilité.
- [Ghidra](https://ghidra-sre.org/) : décompilation/désassemblage.
- [CyberChef GitHub](https://github.com/gchq/CyberChef) : option hors ligne.
- [pwntools docs](https://docs.pwntools.com/) : services TCP, exploitation de binaires.
- [Wireshark](https://www.wireshark.org/) : PCAP et protocoles.
- [SageMath](https://www.sagemath.org/) : cryptographie/math.

### Test préalable

```bash
bash ./preflight.sh
```

---

## 3. Connexions aux instances NCTF26

**Ne pas figer une adresse de challenge** : elle est propre à l'équipe et peut changer quand l'instance redémarre.

### Web

```text
https://<identifiant>.t.ctf.tg/
```

Ouvrir la vraie URL donnée par le challenge. Pour HTTP brut :

```bash
curl -i 'https://<identifiant>.t.ctf.tg/'
```

### Service TCP avec TLS (1337)

```bash
ncat --ssl <identifiant>.t.ctf.tg 1337
# ou
openssl s_client -quiet \
  -connect <identifiant>.t.ctf.tg:1337 \
  -servername <identifiant>.t.ctf.tg
```

Ne pas utiliser `nc` sans TLS.

Avec pwntools :

```python
from pwn import remote
HOST = 'REMPLACER.t.ctf.tg'
r = remote(HOST, 1337, ssl=True, sni=HOST)
print(r.recv(timeout=3))
r.close()
```

### Instance privée via WireGuard

1. Télécharger **sa propre** configuration via la page VPN de l'équipe.
2. Garder le `.conf` privé : les clés doivent **jamais** être copiées dans un chat, dépôt ou write-up.
3. Sous Linux, placer le fichier dans un répertoire local sûr :

```bash
chmod 600 ./nctf-vpn.conf
sudo wg-quick up ./nctf-vpn.conf
sudo wg show
ip route get 10.100.x.y  # remplacer par l'IP autorisée
# En fin de session :
sudo wg-quick down ./nctf-vpn.conf
```

4. Scan restreint à **l'IP / la plage explicitement attribuée à l'équipe**, jamais l'infrastructure centrale ni les réseaux d'autres équipes :

```bash
nmap -sV -Pn -p 22,80,443 10.100.x.y
```

**Accès réseau** : d'après la documentation transmise, les instances sont joignables depuis le Togo ; désactiver les VPN commerciaux étrangers. Le VPN WireGuard d'équipe n'est pas un VPN commercial.

---

## 4. Protocole universel de résolution

### Fiche de triage (toujours remplir)

- **ID / nom / catégorie / points** : ...
- **Auteur / équipe / heure début** : ...
- **Entrée** : URL, TLS TCP, VPN, fichier joint, texte, capture, repo.
- **Objectif** : retrouver un secret, réparer un service, contourner une logique de challenge, obtenir le flag.
- **Observations vérifiées** : ...
- **Hypothèses** (distinctes des faits) : ...
- **Outils et commandes exécutés** : ...
- **Résultat / preuve** : ...
- **Prochain test à faible coût** : ...
- **Statut** : Nouveau / Triage / En cours / Bloqué / Résolu.

### Arbre de décision express

1. **Fichier fourni ?** `file`, `sha256sum`, `xxd`, `strings`, `exiftool`, `binwalk`, puis outil spécialisé. Ne pas exécuter un binaire inconnu sur l'hôte sans isolation.
2. **Service HTTP ?** Browser DevTools, `curl -i`, cookies, endpoints, scripts JS, méthodes, erreurs; ensuite proxy Burp et hypothèses ciblées.
3. **Service TCP ?** Vérifier TLS, lire l'accueil et le protocole, automatiser l'échange avec pwntools, chercher une relation mathématique ou un parseur.
4. **VM privée ?** Vérifier WireGuard puis découvrir uniquement les ports de **l'instance autorisée**; cartographier les services et analyser la configuration.
5. **Énoncé mathématique / algorithmique ?** Modéliser sur papier, coder un solveur reproductible, tester avec petits cas connus.
6. **Bloqué ?** Relire l'énoncé mot par mot, changer d'hypothèse, documenter la piste rejetée et transmettre à un coéquipier.

### Commandes universelles sur un fichier local

```bash
F=./piece_jointe
file "$F"
sha256sum "$F"
xxd -l 256 "$F"
strings -a -n 5 "$F" | head -80
exiftool "$F" 2>/dev/null || true
binwalk "$F" 2>/dev/null || true
```

**Règle d'or** : aucun scan agressif ou brute force non autorisé. Pas de téléchargement/exécution aveugle de scripts inconnus. Pas de divulgation des clés WireGuard ni du jeton d'équipe.

---

## 5. Playbooks des 19 catégories

### 5.1 WEB — 67

**Boîte à outils** : navigateur + DevTools, `curl`, Burp, `jq`, CyberChef, `ffuf` (option), `sqlmap` (uniquement si autorisé et utile).

**Plan** :
1. Cartographier les pages, API, paramètres, cookies, sessions, fichiers JS, `robots.txt`, messages d'erreurs.
2. Identifier **où une entrée traverse une frontière de confiance** : URL→serveur, utilisateur→base, template, fichier, SSRF, contrôle de rôle.
3. Tester des hypothèses ciblées : IDOR/BOLA, SQLi, SSTI, path traversal, JWT mal validés, upload, SSRF, confusion de types, logique métier.
4. Comprendre l'effet réel (différence de réponse, permissions, comportement), produire une requête minimale reproductible.
5. Relever le flag puis sauvegarder la requête (en masquant secrets/cookies).

```bash
URL='https://REMPLACER.t.ctf.tg/'
curl -i "$URL"
curl -s "$URL" | grep -Eoi 'src="[^"]+"|href="[^"]+"' | head
curl -i "${URL}robots.txt"
# JSON d'une API donnée par l'énoncé : curl -s "$URL/api/..." | jq .
```

**Alertes fréquentes** : base64 ≠ chiffrement, token JWT mal configuré, API moins protégée que l'interface, pagination et IDs prévisibles, conditions de course. Ne pas conclure qu'un scan a prouvé une faille : il faut vérifier manuellement.

### 5.2 CRYPTO — 69

**Boîte à outils** : Python, `pycryptodome`, `sympy`, SageMath, CyberChef, `openssl`, `hashcat` pour exercices de récupération de mots de passe, Z3.

**Plan** :
1. Reconnaître le **format** : hex, base64, base32, byte array, entier, PEM, ASN.1.
2. Séparer **encodage**, **hash**, **chiffrement**, **signature**, et **pseudo-aléatoire**.
3. Identifier la primitive et ses paramètres (`n,e,c` RSA, IV/nonce AES/CTR/GCM, clés, rounds, réutilisations).
4. Chercher l'erreur mathématique ou d'implémentation : petits facteurs, nonce réutilisé, XOR à clé répétée, oracle, padding, PRNG prédictible, mauvais `e` RSA.
5. Construire un solveur et **vérifier** la solution par ré-encodage/déchiffrement avant soumission.

```python
import base64
s = 'SGVsbG8='
print(base64.b64decode(s))

# XOR entre deux chaînes de même longueur
x = bytes.fromhex('010203')
y = bytes.fromhex('616263')
print(bytes(a ^ b for a, b in zip(x, y)))
```

**Arbre RSA** : regarder `gcd(n_i,n_j)` entre moduli ; `factor(n)` si petit ; `e` faible et message non rembourré ; `p,q` proches ; `d` exposé ; mauvaise génération de nombres premiers ; CRT mal utilisé.

**Arbre AES** : identifier mode ECB/CBC/CTR/GCM ; IV/nonce réutilisé ? padding incorrect ? oracle ? authentification ignorée ? Ne jamais supposer qu'« AES cassé » est la vraie piste.

### 5.3 REVERSE — 16

**Boîte à outils** : `file`, `strings`, `readelf`, `objdump`, `gdb`, Ghidra, `ltrace`/`strace` (option), Z3.

**Plan** :
1. Identifier architecture, format, protections et dépendances.
2. Examiner les chaînes, `main`, fonctions de vérification, comparaisons, boucles de transformation.
3. Retrouver la logique de validation dans le pseudo-code Ghidra.
4. Reproduire l'algorithme en Python, inverser les opérations quand possible, ou résoudre les contraintes avec Z3.
5. Tester la candidate localement et tracer le raisonnement.

```bash
file ./challenge
sha256sum ./challenge
strings -a ./challenge | head
readelf -h ./challenge
objdump -d ./challenge | less
# Si le binaire est jugé sûr et lancé EN VM : gdb --args ./challenge
```

### 5.4 BOOT2ROOT — 14

**Boîte à outils** : WireGuard, `nmap`, `curl`, SSH, Burp, `smbclient`, `linpeas`/`winpeas` si autorisés, journaux système, outils manuels d'énumération.

**Plan** :
1. Valider l'IP fournie et le routage VPN. Démarrer par le scan de ports autorisé.
2. Énumérer les services et versions ; inspecter les pages et partages exposés ; chercher des identifiants dans les fichiers du challenge.
3. Obtenir un accès utilisateur uniquement par la vulnérabilité prévue par le labo.
4. Énumérer permissions, tâches planifiées, services, secrets en clair, `sudo -l`, binaires SUID, capabilities, PATH, volumes/montages.
5. Élever les privilèges dans la VM cible, récupérer les flags utilisateur et root, documenter les modifications.

```bash
IP='10.100.x.y'
nmap -sV -Pn -p 22,80,443 "$IP"  # étendre les ports si l'instance et les règles le permettent
# Après accès légitime au challenge :
id; uname -a; sudo -l; find / -perm -4000 -type f 2>/dev/null
```

### 5.5 CLOUD — 14

**Boîte à outils** : `jq`, AWS CLI, Azure CLI, `gcloud`, Terraform, Docker, `kubectl`, `yq` et outils IAM selon le scénario.

**Plan** :
1. Identifier la plateforme **simulée/autorisé**e : AWS, Azure, GCP, Kubernetes ou environnement conteneurisé.
2. Inspecter les artefacts fournis : `terraform.tfstate`, YAML, fichiers `.env`, logs, manifestes, policies IAM, rôles, buckets et ACL.
3. Construire le graphe identités → permissions → ressources → secrets accessibles.
4. Vérifier les erreurs de configuration **dans le tenant ou simulateur de challenge uniquement**.
5. Écrire un chemin d'attaque minimal et vérifier les privilèges réellement obtenus.

```bash
# Sur un fichier d'état fourni, éviter d'afficher et partager les secrets
jq 'keys' terraform.tfstate
kubectl config current-context  # vérifier le CONTEXTE avant toute commande !
kubectl auth can-i --list       # seulement sur le cluster du challenge
```

**Caution** : ne jamais essayer des clés trouvées sur un vrai compte cloud non inclus dans le périmètre. Ne pas exécuter `terraform apply` sur une infrastructure extérieure.

### 5.6 STEGO — 14

**Boîte à outils** : `file`, `exiftool`, `binwalk`, `xxd`, `strings`, `zsteg` (PNG/BMP), `steghide` (JPEG/audio), Audacity, Sonic Visualiser, Pillow.

**Plan** : reconnaître le type réel → vérifier métadonnées → fichiers concaténés/embarqués → couches/canaux/LSB → spectrogramme audio → hypothèse sur un mot de passe fourni par des indices.

```bash
file image.png
exiftool image.png
binwalk image.png
strings -a -n 6 image.png | head
# zsteg image.png      # si installé et adapté au format
# steghide info image.jpg
```

### 5.7 SUPPLYCHAIN — 14

**Boîte à outils** : Git, `jq`, `git log`, `git diff`, `npm`, `pip`, `cargo`, `syft`, `grype`, `trivy`, `semgrep` si installés.

**Plan** :
1. Identifier l'écosystème (npm, pip, Maven, Cargo, Go, Docker, GitHub Actions).
2. Lire manifestes, lockfiles, scripts de post-install, workflows CI, Dockerfiles et historique Git.
3. Repérer dépendance trompeuse, substitution de paquet, version vulnérable, secrets incorporés, étape de pipeline modifiée.
4. Reconstituer la chaîne d'exécution en analyse statique d'abord (sandbox pour le reste).
5. Localiser l'artefact ou le secret du challenge.

```bash
git log --all --oneline --decorate -20
git diff HEAD~1 HEAD --stat
grep -RniE 'postinstall|preinstall|curl|wget|token|secret' . --exclude-dir=.git | head
```

### 5.8 AI — 15

**Boîte à outils** : Python, client HTTP selon API, fichiers JSON, scripts de tests, inspection des prompts/consignes du challenge.

**Plan** : identifier le rôle du modèle (oracle, classifieur, chatbot, agent ou parseur) → reconnaître objectif et restrictions → tester entrée/sortie avec **prompts minimaux** → mesurer les différences → isoler une erreur de priorité d'instructions, de validation, de contexte ou de sortie → automatiser les variantes si permis. Une injection de prompt n'est pas équivalente à une RCE.

**Caution** : pas de données réelles d'autres utilisateurs ni de secrets externes ; respecter les limites de requêtes et les règles relatives à l'assistance IA.

### 5.9 SYSADMIN — 13

**Boîte à outils** : Bash, PowerShell, `systemctl`, `journalctl`, `ps`, `ss`, `find`, `getcap`, `sudo`, `getfacl`, `openssl`.

**Plan** : comprendre le service demandé → vérifier utilisateurs/groupes/ACL → processus et ports → journaux → configuration des services → tâches cron/systemd → conteneurs/permissions → reproduire et corriger ou exploiter le défaut **dans la VM de challenge**.

```bash
id; groups
ss -lntup
systemctl --failed
find / -perm -4000 -type f 2>/dev/null
getcap -r / 2>/dev/null
```

### 5.10 PWN — 12

**Boîte à outils** : pwntools, GDB + pwndbg/GEF, `checksec`, `readelf`, `objdump`, ROPgadget, `patchelf` (au besoin).

**Plan** :
1. Récupérer binaire, libc et loader éventuellement fournis ; vérifier architecture, PIE, NX, canary, RELRO.
2. Lire les entrées utilisateur, tailles de buffers, conversions et fonctions vulnérables.
3. Reproduire en local (VM), développer un PoC non destructif, calculer offsets et contraintes.
4. Construire l'exploit avec pwntools, puis l'adapter au service TLS avec SNI.
5. Vérifier la stabilité et enregistrer le script final.

```bash
file ./vuln
readelf -W -l ./vuln | grep GNU_STACK
checksec --file=./vuln   # si checksec disponible
# gdb --args ./vuln       # isoler avant exécution
```

### 5.11 BLOCKCHAIN — 11

**Boîte à outils** : Foundry (`forge`, `cast`), `solc`, Slither, Remix, explorateur local/testnet, RPC du challenge.

**Plan** : identifier chaîne/EVM, contrat et ABI → lire fonctions publiques et rôles → vérifier logique de permission, `delegatecall`, appels externes, arrondis, signatures et nonce → reproduire en fork/local si autorisé → soumettre la transaction requise dans le réseau de jeu.

**Caution** : utiliser exclusivement réseau de test/instance du challenge ; pas de wallet personnel avec fonds, jamais de seed phrase partagée.

### 5.12 ML — 11

**Boîte à outils** : Python, pandas, numpy, scikit-learn, Jupyter, PyTorch/TensorFlow si le modèle l'exige, inspecteurs ONNX/HDF5.

**Plan** : comprendre l'entrée/sortie → déterminer si c'est un défi de données, modèle, robustesse ou sérialisation → vérifier colonnes, labels, fuite de données et contraintes → construire des tests reproductibles → optimiser une métrique imposée.

**Caution** : traiter modèles sérialisés et notebooks comme du code potentiellement dangereux ; ne jamais désérialiser aveuglément un pickle inconnu sur l'hôte.

### 5.13 MISC — 10

**Boîte à outils** : Python, Bash, CyberChef, `file`, archives, `strings`, `jq`, tableurs si données tabulaires.

**Plan** : reconnaître la nature exacte de l'entrée → chercher structure, encodage, formats non standard, suites logiques, bots de dialogue → écrire le plus petit script qui élimine la répétition manuelle.

### 5.14 NETWORKING — 10

**Boîte à outils** : Wireshark, `tshark`, `tcpdump`, `nmap`, `dig`, `openssl`, Scapy.

**Plan** : identifier capture vs service actif → inspecter protocoles TCP/UDP/HTTP/DNS/ICMP/TLS → suivre les flux → extraire objets ou champs suspects → vérifier fragmentation, tunneling, encodage ou traces d'authentification.

```bash
tshark -r traffic.pcapng -q -z io,phs
tshark -r traffic.pcapng -Y 'dns' -T fields -e dns.qry.name | head
tshark -r traffic.pcapng -Y 'http' -T fields -e http.host -e http.request.uri | head
```

### 5.15 PPC — 10

**PPC = Programmation / Problem-solving** dans l'usage CTF (vérifier l'intitulé réel). **Boîte à outils** : Python, `collections`, `itertools`, `heapq`, `math`, `networkx` (option), pwntools pour les services interactifs.

**Plan** : décoder l'énoncé → identifier type d'algorithme (graphe, combinatoire, DP, nombres, chaînes, tri) → calculer complexité → coder petit solveur → vérifier exemples et cas extrêmes → gérer plusieurs manches et délais.

```python
from pwn import remote
# Remplacer par le service de TON challenge.
# Adapter le parsing et le protocole observé avant d'envoyer des réponses.
```

### 5.16 OSINT — 9

**Boîte à outils** : moteurs de recherche, recherche inversée d'image, OpenStreetMap, archives web, EXIF, chronologies, vérification croisée.

**Plan** : extraire les indices précis (langue, région, bâtiment, date, événement, pseudo fictif) → chercher avec plusieurs combinaisons → vérifier au moins deux sources publiques → distinguer géolocalisation/date/dénomination → répondre exactement au format demandé.

**Éthique** : rester sur les personnes/scénarios et informations autorisés du challenge, ne pas récolter de données privées de personnes réelles ni publier d'informations sensibles.

### 5.17 HARDWARE — 8

**Boîte à outils** : `binwalk`, `xxd`, Ghidra, PulseView/sigrok, outils UART/SPI/I2C, analyseur logique si fichier/signal physique fourni.

**Plan** : reconnaître firmware/EEPROM/capture logique → identifier architecture et encapsulation → chercher partitions et chaînes → décoder protocole ou trace UART → extraire la clé/commande attendue.

### 5.18 MOBILE — 8

**Boîte à outils** : `jadx`, `apktool`, `adb`, MobSF (isoler), Frida (si disponible), Ghidra pour bibliothèques natives.

**Plan** : identifier APK/iOS → lire manifestes, permissions, endpoints et certificats → inspection statique des ressources et du code → exécution en émulateur isolé si nécessaire → tester logique d'authentification et stockage local → récupérer le secret du défi.

**Caution** : ne pas installer un APK inconnu sur ton téléphone principal.

### 5.19 CHAINS — 6

**Définition exacte à confirmer** dans le NCTF : cela peut désigner une chaîne d'exploitation en plusieurs étapes ou un format propre à la compétition.

**Plan générique** : construire un graphe **entrée → transformation → artefact intermédiaire → prochaine étape → flag** ; conserver chaque sortie et ses dépendances ; écrire un script/pipeline déterministe, réexécutable depuis le début. Éviter les étapes manuelles impossibles à reproduire.

---

## 6. King of the Hill et Boot2Root

### Particularité KOTH

- Les collines sont **partagées** et concurrentielles : ce n'est pas un défi classique à flag unique.
- D'après les instructions fournies, il faut une équipe **complète de 4 à 5 joueurs** pour marquer.
- Le jeton d'équipe est une valeur **secrète** : ne pas l'envoyer ici et ne pas l'ajouter à un dépôt.
- Les points tombent par tours pendant la possession. Sur les boot2root, le fichier `root` rapporte le double du fichier utilisateur (selon la notice fournie).
- Vérifier **sur le site officiel** la date exacte et les modalités : la notice reçue écrit « jeudi 6 novembre » alors que le 6 novembre 2026 est un **vendredi**.

### Approche KOTH si les règles le permettent

1. **Avant l'ouverture** : rôle de chaque joueur, plan de communication, script de connexion, horloge locale synchronisée.
2. **Capture** : inventorier la surface de la colline explicitement fournie, exploiter la faille du jeu, écrire le jeton secret dans le fichier « king » requis.
3. **Validation** : vérifier que le jeton est pris en compte et que les points progressent, sans copier le secret dans les logs.
4. **Tenue** : comprendre les reconquêtes autorisées, privilégier services stables et contrôles non destructeurs, surveiller les tours et le scoreboard.
5. **Récupération** : en cas de perte, garder les étapes de reprise reproductibles.

Ne pas attaquer les machines d'équipes, panneaux de gestion ou service VPN hors périmètre. Ne jamais effacer les données ou dégrader les services communs à moins que le règlement l'autorise explicitement.

---

## 7. Méthode d'équipe et gestion du temps

### Organisation de 5 joueurs (à adapter selon les points forts)

| Rôle | Catégories principales | Renfort |
|---|---|---|
| J1 | Web, API, Burp | AI, supplychain |
| J2 | Crypto, PPC | Blockchain, ML |
| J3 | Reverse, Pwn | Mobile, hardware |
| J4 | Boot2Root, Cloud, Sysadmin | Networking, KOTH |
| J5 | OSINT, Stego, Misc | Web/Crypto et coordination |

**Pour ton profil systèmes/réseaux/cloud/DevOps**, prends J4 comme position naturelle, mais prépare les bases Web et Crypto car ce sont les volumes les plus élevés.

### Temps conseillés (heuristiques, pas des règles fixes)

- **0–5 min** : compréhension / fichiers / premières observations.
- **5–15 min** : deux hypothèses simples, outils standards.
- **15–30 min** : preuve d'une piste, prototype de solveur ou exploitation.
- **30 min sans progrès** : passer la main / documenter / changer de problème.
- **Toutes les 45–60 min** : mini-synchronisation sur blocages, points et nouvelles découvertes.

### Tracker

Tenir `tracker.csv` à jour : chaque challenge appartient à **un seul responsable actif**, avec statut et prochaine action. Le fichier livré dans le kit est prêt à remplir.

### Hygiène opérationnelle

- Dossier `NCTF26/challenges/<cat>/<nom>/` avec `README.md`, `files/`, `solve.py`, `notes.md`, `evidence/`.
- Historique terminal (`script` ou redirection vers log) **sans** capturer clés privées, mots de passe ou jetons d'équipe.
- Sauvegardes régulières (Git privé si règlement le permet). Ne pas publier les solutions pendant l'événement si interdit.
- Préparer un hotspot 4G/5G en secours si le réseau campus/entreprise bloque WireGuard UDP.

---

## 8. Modèle de write-up

```markdown
# [CAT] Nom du challenge

## Contexte
- Points :
- Lien/instance (sans jeton) :
- Objectif :
- Fichiers :

## Observation et reconnaissance
- Faits observés :
- Commandes et résultats :

## Hypothèse et validation
- Vulnérabilité / propriété mathématique :
- Pourquoi elle marche :
- Preuve :

## Solveur / exploitation
- Commandes ou script reproductibles :
- Prérequis :

## Résultat
- Flag : **ne pas publier tant que le règlement l'interdit**
- Temps investi :
- Ce que nous avons appris :
```

---

## 9. Checklist avant lancement

- [ ] Règles de compétition lues ; **usage de l'IA** explicitement confirmé.
- [ ] Équipe complète et rôles attribués ; canal de communication prêt.
- [ ] Connexion depuis le Togo ; pas de VPN/proxy commercial étranger.
- [ ] `ncat --ssl` testé sur un challenge réellement ouvert (pas d'adresse inventée).
- [ ] WireGuard téléchargé, fichier privé en `chmod 600`, test d'une IP autorisée si accessible.
- [ ] Python, venv, nmap, Ghidra au besoin, Burp, CyberChef prêts.
- [ ] Répertoire de travail créé ; `tracker.csv` partagé entre coéquipiers de manière privée.
- [ ] Format du flag, soumissions, horaires et KOTH vérifiés sur le site.
- [ ] Machine allégée : fermer GNS3 et VM de labo inutiles pour préserver RAM/CPU.
- [ ] Un coéquipier garde la vue d'ensemble sur les points et les blocages.

---

## 10. Références utiles

- [Portail de compétition](https://arena.ctf.tg/)
- [Guide de connexion NCTF26](https://arena.ctf.tg/connexion) (peut requérir une session connectée)
- [VPN de l'équipe](https://arena.ctf.tg/plugins/team_instancer/vpn)
- [King of the Hill](https://arena.ctf.tg/plugins/koth/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [CryptoHack](https://cryptohack.org/)
- [pwn.college](https://pwn.college/)
- [OverTheWire](https://overthewire.org/wargames/)
- [picoCTF practice](https://play.picoctf.org/)
- [CTFtime](https://ctftime.org/)
- [ArchWiki — Python virtual environments](https://wiki.archlinux.org/title/Python)

> **Versionner ce document pendant le tournoi** : chaque résolution crée une nouvelle procédure plus utile que la liste d'outils initiale.
