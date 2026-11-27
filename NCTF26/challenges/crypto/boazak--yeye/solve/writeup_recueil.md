### 12. Yeye — attaque length extension SHA-256 — `yeye`

**Statut :** NON CONFIRMÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `yeye_solve.py`.

#### Énoncé, contexte et périmètre

Le script `yeye_solve.py` livré dans la conversation décrit un MAC vulnérable construit à partir de `SHA256(secret || message)`. En connaissant un message et le digest correspondant, il est parfois possible de calculer le digest d'un message prolongé, sans le secret, en reconstituant l'état de hachage et le padding SHA-256. Cette technique ne marche pas contre HMAC-SHA256 correctement utilisé.

#### Reconnaissance, commandes et résultats observés

Le fichier contient un solveur autonome ciblant une instance CTF par défaut `https://bwitph2ipsyqdnbr.t.ctf.tg`. Aucun résultat `NCTF{...}` n'est joint.

#### Procédure de reproduction ou reprise technique

```bash
python3 yeye_solve.py 'https://<instance-ctf-autorisee>.t.ctf.tg'
```
La longueur inconnue de la clé doit être explorée avec parcimonie et les réponses de l'API doivent être conservées.

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Un message correctement prolongé ne garantit rien si l'application normalise ou signe autrement les paramètres.
