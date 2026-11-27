### 03. Tap code — carré de Polybe — `tap-code`

**Statut :** MESSAGE EXTRAIT SANS FLAG · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `taps.txt`.

#### Énoncé, contexte et périmètre

Le fichier `taps.txt` contient `44 11 35 13 34 14 15 35 34 31 54 12 24 45 43`. Chaque paire désigne une ligne et une colonne d'un carré 5×5. La variante courante fusionne I et J ; il n'existe donc que 25 caractères différents.

#### Reconnaissance, commandes et résultats observés

Le décodage des coordonnées du fichier original donne `TAPCODEPOLYBIUS`, une expression descriptive de l'algorithme et non un flag.

#### Procédure de reproduction ou reprise technique

```python
alpha='ABCDEFGHIKLMNOPQRSTUVWXYZ'
pairs=open('taps.txt').read().split()
print(''.join(alpha[(int(t[0])-1)*5+int(t[1])-1] for t in pairs))
```

#### Résultat / flag

**TAPCODEPOLYBIUS (pas de format NCTF)**

#### Pièges, interprétation et enseignement

La sortie ne doit pas être réemballée arbitrairement dans `NCTF{...}` sans consigne.
