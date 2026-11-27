### 11. Quadratic I — système GF(2) de poids 30 — `quadratic-i`

**Statut :** NON RÉSOLU / SOLVEUR DISPONIBLE · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `public.json`, `system.txt`, `system(1).txt`, `system(2).txt`, `vault.txt`, `vault(1).txt`, `vault(2).txt`, `Quadratic_I_Solver_Kit.zip`.

#### Énoncé, contexte et périmètre

Le fichier `public.json` définit `C7 -- GF(2) bounded-weight system` avec `n=276`, `k=138`, `w=30`, une matrice H, un syndrome s et la convention `col 0 = LSB`. L'objectif est de déterminer un vecteur e de longueur 276 et de poids de Hamming 30 vérifiant `H*eᵀ=s`. Le secret est ensuite dérivé par AES-256-GCM : clé `SHA-256` des octets de e en ordre MSB-first, nonce du fichier `vault.txt`, ciphertext et tag. Le fichier `system.txt` est volumineux et indispensable.

#### Reconnaissance, commandes et résultats observés

Un kit antérieur `Quadratic_I_Solver_Kit.zip` contient un solveur et un README. Aucun flag déchiffré authentifié n'apparaît dans les traces disponibles. Le kit et les trois copies du système ont été conservés.

#### Procédure de reproduction ou reprise technique

```bash
unzip -l Quadratic_I_Solver_Kit.zip
head -30 public.json
head -5 vault.txt
# Le solveur du kit doit être utilisé sur données authentiques,
# puis l'authentification AES-GCM doit réussir avant tout flag.
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Ne pas confondre SHA3 et SHA256 ; ne pas inverser les conventions de bits ni perdre le tag d'authentification.
