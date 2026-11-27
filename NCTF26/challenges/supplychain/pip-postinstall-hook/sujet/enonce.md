# pip-postinstall-hook

- **Catégorie :** supplychain
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Le fichier `setup.py` de `acme-license-check` contient un hook `PostInstall` appelé à l'installation du paquet. `_run()` lit une chaîne hexadécimale `_B`, applique un XOR avec la constante `_K=91`, puis exécute le texte obtenu via `exec(compile(...))`. Le code décodé écrit un fichier `.acme_licence` dans le répertoire utilisateur contenant la réponse CTF. La fonction métier apparente `check()` du module se contente de renvoyer `True`.
