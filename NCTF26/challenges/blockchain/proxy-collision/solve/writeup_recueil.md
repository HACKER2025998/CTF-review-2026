### 29. Delegatecall — collision du stockage slot 0 — `proxy-collision`

**Statut :** FLAG VÉRIFIÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `Proxy.sol`, `Logic.sol`, `proxy_storage.json`.

#### Énoncé, contexte et périmètre

`Proxy.sol` place `implementation` au slot 0 ; `Logic.sol` place `uint256 value` au slot 0 et écrit dans cette variable avec `setValue()`. Le `delegatecall` exécute le code de Logic dans le stockage du Proxy : `value` réécrit donc le slot de l'adresse d'implémentation. Le fichier `proxy_storage.json` fournit les valeurs des slots, dont le slot 0 est une chaîne ASCII hexadécimale déguisée en stockage Ethereum.

#### Reconnaissance, commandes et résultats observés

La conversion du slot zéro en octets, puis la suppression des NUL de padding à droite, a été reproduite localement.

#### Procédure de reproduction ou reprise technique

```python
import json
S=json.load(open('proxy_storage.json'))
w=S['0x'+'0'*64]
print(bytes.fromhex(w[2:]).rstrip(bytes([0])).decode())
```

#### Résultat / flag

**NCTF{delegatecall_hits_slot0}**

#### Pièges, interprétation et enseignement

Les layouts de stockage doivent être compatibles entre proxy et implémentation ; le modèle EIP-1967 évite cette collision triviale.
