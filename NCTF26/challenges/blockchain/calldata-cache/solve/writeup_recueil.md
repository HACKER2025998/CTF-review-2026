### 28. NotesRegistry — ABI transaction calldata — `calldata-cache`

**Statut :** FLAG VÉRIFIÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `calldata.txt`, `abi.json`, `NotesRegistry.sol`.

#### Énoncé, contexte et périmètre

Le contrat `NotesRegistry` définit `store(uint256 id, address who, string note)`. La transaction brute est donnée dans `calldata.txt` et son ABI est contenu dans `abi.json`. Un appel ABI commence par 4 octets de sélecteur, puis trois mots de 32 octets. Le troisième argument est dynamique et l'emplacement initial contient l'offset de son véritable bloc. Le premier argument vaut 42 et l'adresse se termine par `c0ffee99` ; le décalage pour la chaîne est `0x60`.

#### Reconnaissance, commandes et résultats observés

Nous avons décodé les octets de la chaîne dynamique et obtenu la réponse. On peut vérifier le résultat sans blockchain accessible puisque tout est dans les octets de calldata.

#### Procédure de reproduction ou reprise technique

```python
raw=bytes.fromhex(open('calldata.txt').read().strip()[2:])
args=raw[4:]
off=int.from_bytes(args[64:96],'big')
length=int.from_bytes(args[off:off+32],'big')
print(args[off+32:off+32+length].decode())
```

#### Résultat / flag

**NCTF{abi_calldata_decoded_by_hand}**

#### Pièges, interprétation et enseignement

L'offset d'un argument dynamique est relatif au début de la zone des arguments, pas au sélecteur de quatre octets.
