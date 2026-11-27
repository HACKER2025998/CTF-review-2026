### 08. ZIP chiffré — images Sylvanus Olympio — `archive-olympio`

**Statut :** NON CONFIRMÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `archive(1).zip`.

#### Énoncé, contexte et périmètre

Cette archive est **distincte** du challenge ZIP-comment. Son contenu a été inspecté : `Sylvanus_Olympio.jpg`, `Armoiries_du_Togo.svg` et `flag.txt` chiffré. Les noms des images semblent former un indice historique, mais aucun mot de passe exact n'a été prouvé par les traces.

#### Reconnaissance, commandes et résultats observés

Une lecture Python sans mot de passe a levé `RuntimeError: File 'flag.txt' is encrypted, password required for extraction`. Aucun flag n'a été récupéré.

#### Procédure de reproduction ou reprise technique

```bash
unzip -l 'archive(1).zip'
7z l -slt 'archive(1).zip'
# Si une clé est trouvée à partir de l'énoncé : 7z x 'archive(1).zip' -p'...'
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Attention à ne pas réutiliser automatiquement le mot de passe d’un autre ZIP du challenge Git.
