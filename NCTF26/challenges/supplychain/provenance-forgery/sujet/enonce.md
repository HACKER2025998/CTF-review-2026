# provenance-forgery

- **Catégorie :** supplychain
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Les quatre versions `acme-app-1.0.0.tgz` à `1.3.0.tgz` ont chacune une déclaration in-toto/SLSA. Dans la version `1.2.0`, `dist/app.js` diffère des autres : une chaîne Base64 `_t` figure dans un commentaire de hotfix. `1.2.0.intoto.json` prétend utiliser `acme-ci` et porte une signature codée entièrement en zéros. La présence formelle d'un document de provenance ne valide ni l'identité du builder ni l'intégrité de son sujet.
