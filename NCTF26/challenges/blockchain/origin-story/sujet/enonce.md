# origin-story

- **Catégorie :** blockchain
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Le contrat `Vault.sol` contient une méthode `initialize(address)` publique sans contrôle `initializer` et une vérification `onlyOwner` basée sur `tx.origin` plutôt que `msg.sender`. Un acteur contrôlant l'adresse `0x00000000000000000000000000000000a77ac6e5` peut théoriquement modifier le propriétaire. `vault.json` apporte un ciphertext hexadécimal et indique `XOR key = keccak256(exploit calldata)`.
