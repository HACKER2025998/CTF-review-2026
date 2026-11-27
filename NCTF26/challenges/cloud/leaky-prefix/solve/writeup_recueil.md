### 31. Kekeli bucket — wildcard sur mauvais préfixe — `cloud-public-prefix`

**Statut :** FLAG DANS ARTEFACT · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `bucket-policy.json`, `bucket-policy(1).json`, `object-index.json`, `object-index(1).json`, `db-snapshot-note.txt`, `logo.txt`, `logo(1).txt`, `banner.txt`, `press-kit.txt`, `press-kit(1).txt`, `roadmap.txt`, `roadmap(1).txt`.

#### Énoncé, contexte et périmètre

Le bucket fictif `kekeli-media-prod` fournit un index d'objets : `assets/public/...` pour les contenus censés être publics et `assets/public-backup/...` pour un contenu de restauration plus sensible. La politique `bucket-policy.json` doit être analysée en comparant son pattern de ressources à chaque clé d'objet ; une expression de préfixe trop permissive couvre involontairement les backups.

#### Reconnaissance, commandes et résultats observés

Le fichier `db-snapshot-note.txt` commence par `INTERNAL RESTORE NOTE -- do not distribute`, puis contient le flag. Il a été directement lu depuis la pièce jointe et la relation de nommage est concordante avec la faille de préfixe.

#### Procédure de reproduction ou reprise technique

```bash
cat bucket-policy.json
cat object-index.json
cat db-snapshot-note.txt
```
Une règle destinée à `assets/public/*` ne doit pas être généralisée accidentellement à `assets/public*`.

#### Résultat / flag

**NCTF{public_read_on_the_wrong_prefix}**

#### Pièges, interprétation et enseignement

La hiérarchie de dossiers dans un bucket S3 n'est qu'une nomenclature de clés ; les permissions sont évaluées sur des chemins et motifs.
