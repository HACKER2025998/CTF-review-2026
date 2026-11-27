### 04. ZIP comment — commentaire global — `zip-comment`

**Statut :** FLAG EXTRAIT · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `archive.zip`.

#### Énoncé, contexte et périmètre

Une archive `archive.zip` ne comporte qu'un fichier banal, mais le format ZIP stocke un commentaire global indépendant des entrées. L'énigme consiste à regarder les métadonnées de l'archive plutôt que seulement les fichiers décompressés.

#### Reconnaissance, commandes et résultats observés

Le champ `ZipFile.comment` contient directement la réponse complète et a été lu sur l'archive originale.

#### Procédure de reproduction ou reprise technique

```bash
unzip -l archive.zip
unzip -z archive.zip
```
```python
from zipfile import ZipFile
with ZipFile('archive.zip') as z:print(z.comment.decode())
```

#### Résultat / flag

**NCTF{look_inside_the_zip_comment}**

#### Pièges, interprétation et enseignement

Ne pas confondre `archive.zip` et `archive(1).zip`, cette dernière comportant un `flag.txt` chiffré.
