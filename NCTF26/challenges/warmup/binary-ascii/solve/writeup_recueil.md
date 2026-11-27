### 02. Groupes de huit bits — ASCII — `binary-bits`

**Statut :** FLAG EXTRAIT · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `bits.txt`.

#### Énoncé, contexte et périmètre

Le fichier `bits.txt` fournit une série de groupes binaires de huit caractères. L'objectif est d'interpréter chaque octet comme un caractère ASCII et de reconstituer le message complet. Le premier octet `01001110` représente `N`, les suivants démarrent `CTF{`.

#### Reconnaissance, commandes et résultats observés

La lecture des octets dans l'ordre du fichier a été reproduite localement. Le résultat répond au format CTF.

#### Procédure de reproduction ou reprise technique

```python
from pathlib import Path
bits=Path('bits.txt').read_text().split()
assert all(len(x)==8 and set(x)<={'0','1'} for x in bits)
print(bytes(int(x,2) for x in bits).decode())
```

#### Résultat / flag

**NCTF{binary_ones_and_zeros}**

#### Pièges, interprétation et enseignement

Conserver l'ordre MSB-first des huit bits ; ne pas inverser les octets.
