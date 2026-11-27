### 10. RSA e=3 — suffixe inconnu, Coppersmith — `rsa-coppersmith`

**Statut :** NON CONFIRMÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `challenge(2).txt`.

#### Énoncé, contexte et périmètre

L'énoncé fourni dit : « Un message = préfixe connu || secret a été chiffré avec e=3 : c=(préfixe_connu·2^b+x)^3 mod n, avec x secret (<2^b). » Le fichier fournit n,c, un préfixe ASCII exact `CONFIDENTIAL - access granted for user admin - token = ` et `suffix_bits=127`. C'est une équation polynomiale modulaire univariée à petite racine.

#### Reconnaissance, commandes et résultats observés

Aucun calcul SageMath réussi ni flag final n'est visible dans les traces ; c'est une procédure d'attaque documentée et non une victoire revendiquée.

#### Procédure de reproduction ou reprise technique

```python
# Pseudocode SageMath (adapter aux valeurs du fichier)
# P = entier big-endian du préfixe, b=127, A=P*2**b
# R.<x> = PolynomialRing(Zmod(n))
# f = (A+x)**3 - c
# for r in f.monic().small_roots(X=2**b,beta=1.0):
#    if pow(A+int(r),3,n)==c: print((A+int(r)).to_bytes(...,'big'))
```
La vérification `pow(m,3,n)==c` est indispensable avant de décoder les octets.

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Une petite racine est limitée par des bornes mathématiques ; aucun essai aléatoire ne remplace Coppersmith.
