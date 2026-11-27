### 24. Docker — secret présent dans une couche supprimée — `layered-image-leak`

**Statut :** FLAG VÉRIFIÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `image.tar`.

#### Énoncé, contexte et périmètre

Une image Docker exportée sous `image.tar` possède trois couches. La première ajoute `app/config/secret.env`, la seconde une application Node minimaliste `app/server.js`, et la troisième un whiteout `app/config/.wh.secret.env`, qui masque le fichier dans le système de fichiers final sans effacer le contenu de la première couche. `manifest.json` permet d'identifier les `layer.tar` individuels. Le fichier secret contient `DEPLOY_KEY` encodée en Base64.

#### Reconnaissance, commandes et résultats observés

La lecture de la couche d'origine, puis le décodage Base64 de `DEPLOY_KEY` ont été rejoués localement et restituent la réponse attendue.

#### Procédure de reproduction ou reprise technique

```python
import tarfile,io,base64
with tarfile.open('image.tar') as outer:
 for m in outer:
  if not m.name.endswith('/layer.tar'):continue
  with tarfile.open(fileobj=io.BytesIO(outer.extractfile(m).read())) as inner:
   for f in inner:
    if f.isfile() and f.name.endswith('secret.env'):
     env=inner.extractfile(f).read().decode()
     print(base64.b64decode(env.split('=',1)[1].strip()).decode())
```

#### Résultat / flag

**NCTF{d0cker_layer_secret_survives_rm_6c15}**

#### Pièges, interprétation et enseignement

Ne jamais stocker un secret dans un `COPY` de build puis le supprimer via `RUN rm` : les couches restent dans l'image distribuée.
