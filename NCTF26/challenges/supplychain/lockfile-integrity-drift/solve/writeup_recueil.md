### 27. npm package-lock — vérification SRI — `npm-lockfile`

**Statut :** PAS DE FLAG DOCUMENTÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `package-lock(2).json`, `left-pad-1.3.0(1).tgz`, `ansi-styles-6.2.1(1).tgz`, `semver-7.5.4(1).tgz`.

#### Énoncé, contexte et périmètre

`package-lock(2).json` décrit une application `acme-cli` avec les dépendances `left-pad`, `ansi-styles`, `semver` et leurs empreintes Subresource Integrity `sha512-...`. Trois tarballs npm sont fournis. Le procédé consiste à comparer les octets exacts de ces archives aux digests du lockfile ; cela permet de détecter une substitution ou des métadonnées trompeuses.

#### Reconnaissance, commandes et résultats observés

Les archives sont conservées avec le lockfile. Aucune sortie finale ni valeur `NCTF` associée n'est certaine à ce stade.

#### Procédure de reproduction ou reprise technique

```python
import pathlib,hashlib,base64,json
obj=json.load(open('package-lock(2).json'))
for k,v in obj['packages'].items():print(k, v.get('integrity'))
# Calculez sha512 et convertissez en base64 pour une comparaison exacte.
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

`integrity` doit être validé sur le tarball original, sans recompression ni modification des octets.
