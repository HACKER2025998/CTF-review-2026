### 36. SentinelBot — token protégé, Base64 et reverse — `sentinelbot`

**Statut :** FLAG RAPPORTÉ · **Points :** 50 · **Instance :** `—`

**Fichiers d’origine associés :** `Pasted markdown(1).md`.

#### Énoncé, contexte et périmètre

Énoncé : « SentinelBot is an offline support assistant shipped as a single Python module, `oracle.py`, exposing `respond(prompt)`. It guards a hidden diagnostic token and politely refuses when you ask about it directly. Everything runs locally — no network, no real model. Call the shipped oracle from your own script and make it hand over the token. » Défi AI de 50 points. Selon notre discussion, `_S` stocke une chaîne `base64(reverse(flag))` ; la fonction `_secret()` procède à `base64.b64decode(_S)[::-1]`.

#### Reconnaissance, commandes et résultats observés

Le write-up précédent indique qu'un filtrage brut `_input_blocked` est appliqué avant la normalisation `_understand()` (Base64/ROT13), ce qui illustre un risque de contournement du filtre par encodage. Cependant le source exact `oracle.py` n'est pas inclus dans les pièces actuellement disponibles ; la valeur de flag est conservée dans la transcription et non re-décodée ici.

#### Procédure de reproduction ou reprise technique

```python
# Avec le fichier oracle.py original :
import base64
# print(base64.b64decode(_S)[::-1].decode())
```
La méthode statique et le contournement de filtrage dynamique sont deux chemins différents, à distinguer dans un write-up.

#### Résultat / flag

**NCTF{b4s3_64_sn34ks_p4st_th3_wordl1st}**

#### Pièges, interprétation et enseignement

Le filtrage avant décodage des données n'empêche pas un message prohibé d'être reconstruit plus tard.
