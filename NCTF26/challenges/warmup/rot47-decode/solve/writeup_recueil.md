### 01. ROT47 — rotation ASCII imprimable — `rot47-decode`

**Statut :** FLAG EXTRAIT · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `secret(1).txt`.

#### Énoncé, contexte et périmètre

Un cryptogramme constitué de caractères ASCII imprimables doit être ramené en texte clair. Le fichier `secret(1).txt` contient `}r%uLC@Ecf0D9:7ED0E9608=JA9DN`. L'indice de forme est un ROT47, substitution sur la plage 33–126. Contrairement à ROT13, la rotation agit aussi sur la ponctuation et les chiffres.

#### Reconnaissance, commandes et résultats observés

La rotation a été appliquée au contenu authentique du fichier et révèle la chaîne attendue. La transformation est involutive : ROT47(ROT47(s)) = s.

#### Procédure de reproduction ou reprise technique

```python
from pathlib import Path
s=Path('secret(1).txt').read_text()
print(''.join(chr(33+(ord(c)-33+47)%94) if 33<=ord(c)<=126 else c for c in s))
```
Ne pas déduire le format par supposition seule : comparer la sortie au préfixe `NCTF{` et à l'accolade finale.

#### Résultat / flag

**NCTF{rot47_shifts_the_glyphs}**

#### Pièges, interprétation et enseignement

Une solution par ROT13 serait incorrecte ; la méthode ne dépend d'aucune clé secrète.
