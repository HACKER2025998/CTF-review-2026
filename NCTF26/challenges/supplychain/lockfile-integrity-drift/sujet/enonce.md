# lockfile-integrity-drift

- **Catégorie :** supplychain
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

`package-lock(2).json` décrit une application `acme-cli` avec les dépendances `left-pad`, `ansi-styles`, `semver` et leurs empreintes Subresource Integrity `sha512-...`. Trois tarballs npm sont fournis. Le procédé consiste à comparer les octets exacts de ces archives aux digests du lockfile ; cela permet de détecter une substitution ou des métadonnées trompeuses.
