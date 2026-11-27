### 09. RSA — Fermat, deux facteurs proches — `boazak--venovi`

**Statut :** FLAG VÉRIFIÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `challenge.txt`.

#### Énoncé, contexte et périmètre

Le fichier `challenge.txt` donne le défi « RSA — Fermat factorization » avec les paramètres entiers RSA `n`, `e=65537` et `c`. Comme `n=pq` avec `p` et `q` proches, la factorisation de Fermat est particulièrement efficace : chercher un entier `a≥√n` tel que `a²−n` soit un carré parfait. Alors `p=a-b`, `q=a+b`, ce qui fournit la clé privée via `φ(n)`.

#### Reconnaissance, commandes et résultats observés

Résolution **rejouée dans cet environnement** à partir du `n,e,c` fourni : recherche terminée dès `a=ceil(sqrt(n))`, différence `q-p=4852`. Le déchiffrement `c^d mod n` donne les octets ASCII du flag.

#### Procédure de reproduction ou reprise technique

```python
from math import isqrt
from pathlib import Path
import re
P=dict(re.findall(r'^([nec])\s*=\s*(\d+)',Path('challenge.txt').read_text(),re.M))
n,e,c=(int(P[x]) for x in 'nec')
a=isqrt(n)+(isqrt(n)**2<n)
while True:
 b=isqrt(a*a-n)
 if b*b==a*a-n:break
 a+=1
p,q=a-b,a+b
assert p*q==n
m=pow(c,pow(e,-1,(p-1)*(q-1)),n)
print(m.to_bytes((m.bit_length()+7)//8,'big').decode())
```
Le dossier contient un solveur Python exécutable et corrigé : `solveurs/04_rsa_fermat.py`.

#### Résultat / flag

**NCTF{VEN0V1_613548868}**

#### Pièges, interprétation et enseignement

RSA reste difficile quand les paramètres sont bons ; la faille ici est le choix de deux nombres premiers presque égaux.
