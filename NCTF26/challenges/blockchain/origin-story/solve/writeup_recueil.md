### 30. Vault.sol — initializer public et tx.origin — `vault-initialize`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `Vault.sol`, `vault.json`.

#### Énoncé, contexte et périmètre

Le contrat `Vault.sol` contient une méthode `initialize(address)` publique sans contrôle `initializer` et une vérification `onlyOwner` basée sur `tx.origin` plutôt que `msg.sender`. Un acteur contrôlant l'adresse `0x00000000000000000000000000000000a77ac6e5` peut théoriquement modifier le propriétaire. `vault.json` apporte un ciphertext hexadécimal et indique `XOR key = keccak256(exploit calldata)`.

#### Reconnaissance, commandes et résultats observés

La chaîne de résolution envisagée : reconstruire la calldata ABI exacte de l'appel gagnant `initialize(address)`, calculer son Keccak-256 Ethereum puis déchiffrer le blob par XOR. Aucun décodage final fiable n'est fourni dans les traces ; ne pas inscrire un flag inventé.

#### Procédure de reproduction ou reprise technique

```text
calldata = selector[4] || leftpad_32(attacker_address)
key = keccak256(calldata)           # Keccak Ethereum != SHA3-256 NIST
plaintext = ciphertext XOR repeated(key)
```
Le script de preuve doit confirmer à la fois l'état de contrat voulu et les octets de calldata.

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Un mauvais sélecteur ou la confusion SHA3/Keccak produirait une réponse fausse.
