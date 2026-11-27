### 43. Hôtes, notes de vitrine et leurres résiduels — `host-inventory`

**Statut :** PIÈCES NON ATTRIBUÉES · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `hosts.json`, `courses(1).log`, `README_vitrine(1).txt`, `old-ctf-note.txt`, `old-ctf-note(1).txt`, `wordlist.txt`, `wordlist(1).txt`.

#### Énoncé, contexte et périmètre

Quelques fichiers téléchargés lors des échanges ne possèdent pas un énoncé de challenge associé dans les matériaux disponibles : `hosts.json` (noms d'hôtes/MAC/tags), `courses(1).log`, `README_vitrine(1).txt`, des wordlists et `old-ctf-note.txt`. La dernière note contient la chaîne `NCTF{not_the_flag_internal_only}` : son sens explicite indique **un leurre**, pas une réponse validée.

#### Reconnaissance, commandes et résultats observés

Ils restent archivés dans le dossier pour éviter toute perte ; l'index TXT les identifie sans leur attribuer un solve fictif.

#### Procédure de reproduction ou reprise technique

```bash
cat old-ctf-note.txt
head -15 hosts.json
wc -l wordlist.txt
```

#### Résultat / flag

**Non applicable**

#### Pièges, interprétation et enseignement

Inventaire et préservation des preuves ne sont pas synonymes d'une résolution.
