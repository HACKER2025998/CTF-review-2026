# layered-image-leak

- **Catégorie :** supplychain
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Une image Docker exportée sous `image.tar` possède trois couches. La première ajoute `app/config/secret.env`, la seconde une application Node minimaliste `app/server.js`, et la troisième un whiteout `app/config/.wh.secret.env`, qui masque le fichier dans le système de fichiers final sans effacer le contenu de la première couche. `manifest.json` permet d'identifier les `layer.tar` individuels. Le fichier secret contient `DEPLOY_KEY` encodée en Base64.
