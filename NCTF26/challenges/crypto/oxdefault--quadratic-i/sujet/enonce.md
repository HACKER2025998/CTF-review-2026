# oxdefault--quadratic-i

- **Catégorie :** crypto
- **Auteur :** oxdefault
- **Points :** —

## Énoncé

Le fichier `public.json` définit `C7 -- GF(2) bounded-weight system` avec `n=276`, `k=138`, `w=30`, une matrice H, un syndrome s et la convention `col 0 = LSB`. L'objectif est de déterminer un vecteur e de longueur 276 et de poids de Hamming 30 vérifiant `H*eᵀ=s`. Le secret est ensuite dérivé par AES-256-GCM : clé `SHA-256` des octets de e en ordre MSB-first, nonce du fichier `vault.txt`, ciphertext et tag. Le fichier `system.txt` est volumineux et indispensable.
