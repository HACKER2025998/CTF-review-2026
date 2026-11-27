### 32. Forum → admin-portal — réutilisation du mot de passe — `cred-reuse`

**Statut :** FLAG RAPPORTÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `services.csv`, `dump.txt`, `wordlist(2).txt`, `admin_portal.enc`.

#### Énoncé, contexte et périmètre

`services.csv` indique quels comptes sont enregistrés sur forum/admin-portal et services annexes. `dump.txt` donne des hashes SHA-1 pour des comptes de forum. `wordlist(2).txt` contient une courte liste de mots de passe. Le compte `afi.doe@webmail.tg` apparaît à la fois sur le forum et sur le portail d'administration, ce qui ouvre la voie à une réutilisation de mot de passe.

#### Reconnaissance, commandes et résultats observés

La valeur `Lome228!` a été rapportée pour cet utilisateur et fait partie du dictionnaire fourni. L'étape complémentaire impliquait `admin_portal.enc`, documenté comme des données AES-256-CBC, mais la reproduction détaillée des options KDF/IV n'est pas préservée. Le flag de résolution a été communiqué dans une réponse précédente ; sa validation scoreboard ne figure pas dans les originaux montés.

#### Procédure de reproduction ou reprise technique

```python
import hashlib
hashes=dict(line.strip().split(':',1) for line in open('dump.txt') if ':' in line)
for pwd in open('wordlist(2).txt'):
 p=pwd.strip()
 if hashlib.sha1(p.encode()).hexdigest()==hashes['afi.doe@webmail.tg']:
  print('Correspondance:',p)
```

#### Résultat / flag

**NCTF{cr3d_reuse_forum_to_admin_portal}**

#### Pièges, interprétation et enseignement

Ne pas inventer les paramètres AES. Utiliser les indices officiels ou l'en-tête du fichier chiffré.
