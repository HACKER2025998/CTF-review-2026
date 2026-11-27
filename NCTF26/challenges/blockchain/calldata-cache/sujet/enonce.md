# calldata-cache

- **Catégorie :** blockchain
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Le contrat `NotesRegistry` définit `store(uint256 id, address who, string note)`. La transaction brute est donnée dans `calldata.txt` et son ABI est contenu dans `abi.json`. Un appel ABI commence par 4 octets de sélecteur, puis trois mots de 32 octets. Le troisième argument est dynamique et l'emplacement initial contient l'offset de son véritable bloc. Le premier argument vaut 42 et l'adresse se termine par `c0ffee99` ; le décalage pour la chaîne est `0x60`.
