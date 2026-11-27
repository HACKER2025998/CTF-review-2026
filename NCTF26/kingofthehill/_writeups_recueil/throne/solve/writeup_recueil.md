### 38. The Throne — contournement debug et HMAC-SHA1 — `koth-throne`

**Statut :** PRISE CONFIRMÉE · **Points :** 5 points/tick · **Instance :** `http://13.37.197.230:28490`

**Fichiers d’origine associés :** `Pasted markdown(1).md`, `throne_safe.py`, `throne_wrk_loop.sh`, `throne.lua`.

#### Énoncé, contexte et périmètre

La colline KOTH `The Throne` était accessible sur `13.37.197.230:28490` (HTTP) et rapportait cinq points par tick. Un diagnostic `/debug` était censé être interne, mais un en-tête `X-Forwarded-For: 127.0.0.1` a permis d'obtenir une clé HMAC et le format de signature `HMAC_SHA1(HILL_KEY, team + '|' + ts)` avec tolérance d'horloge d'environ 45 secondes. Le jeton d'équipe est un secret opérationnel du jeu et n'est pas reproduit dans ce résumé.

#### Reconnaissance, commandes et résultats observés

**Preuve de prise rapportée par l'utilisateur :** `python3 throne_claim.py` a renvoyé `[key=str] 200 {"ok": true, "king": "242cb7b1…"}`. La bonne interprétation de `HILL_KEY` était la **chaîne hexadécimale** utilisée comme octets ASCII, pas le binaire `bytes.fromhex`. `throne_safe.py` et les fichiers de la boucle de réclamation sont archivés. Cela prouve une prise à l'instant t, pas une domination permanente (d'autres équipes peuvent reprendre la colline).

#### Procédure de reproduction ou reprise technique

```text
GET /debug + X-Forwarded-For: 127.0.0.1
→ renseignements HMAC
HMAC_SHA1(key-as-string, team + '|' + ts)
POST /throne → 200 {"ok":true,"king":"..."}
```
Conserver la fréquence autorisée par les règles, ne pas faire de flood/DoS.

#### Résultat / flag

**Pas de flag classique ; prise KOTH confirmée**

#### Pièges, interprétation et enseignement

Les fichiers de trace contiennent potentiellement de vrais jetons d'équipe de l'époque ; conserver le ZIP en privé.
