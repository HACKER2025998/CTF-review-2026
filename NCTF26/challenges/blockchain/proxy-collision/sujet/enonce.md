# proxy-collision

- **Catégorie :** blockchain
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

`Proxy.sol` place `implementation` au slot 0 ; `Logic.sol` place `uint256 value` au slot 0 et écrit dans cette variable avec `setValue()`. Le `delegatecall` exécute le code de Logic dans le stockage du Proxy : `value` réécrit donc le slot de l'adresse d'implémentation. Le fichier `proxy_storage.json` fournit les valeurs des slots, dont le slot 0 est une chaîne ASCII hexadécimale déguisée en stockage Ethereum.
