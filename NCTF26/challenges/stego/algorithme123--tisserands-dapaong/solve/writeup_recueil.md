### 35. QR, affiche et documents visuels annexes — `qr-festival`

**Statut :** NON ATTRIBUÉ / NON RÉSOLU · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `affiche(1).png`, `image(20261107-154328).png`, `guidepdf-1.png`, `guide-motifs-1.pdf`, `README_vitrine(1).txt`.

#### Énoncé, contexte et périmètre

Plusieurs documents visuels ont été transmis : `affiche(1).png`, une capture datée du 7 novembre, `guidepdf-1.png` et `guide-motifs-1.pdf`. Une note indique que `vitrine.local` est un site public de festival hors périmètre CTF et que son fichier n'a pas de message secret. Aucun numéro exact d'épreuve ni flag fiable n'est disponible dans les traces, donc ces sources sont conservées comme annexes sans les associer artificiellement à une solution.

#### Reconnaissance, commandes et résultats observés

Vérifier les QR présents, les métadonnées et les structures de fichiers seulement si l'énoncé correspondant est retrouvé ; ne pas croire qu'un QR signifie forcément un secret.

#### Procédure de reproduction ou reprise technique

```bash
file affiche\(1\).png guide-motifs-1.pdf
exiftool 'affiche(1).png'
# zbarimg affiche\(1\).png (si un QR est réellement présent)
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

La note fournie exclut explicitement le site vitrine du périmètre CTF.
