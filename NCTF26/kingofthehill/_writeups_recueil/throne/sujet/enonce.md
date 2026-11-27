# throne

- **Catégorie :** kingofthehill/outils
- **Auteur :** inconnu (à compléter)
- **Points :** 5 points/tick

## Énoncé

La colline KOTH `The Throne` était accessible sur `13.37.197.230:28490` (HTTP) et rapportait cinq points par tick. Un diagnostic `/debug` était censé être interne, mais un en-tête `X-Forwarded-For: 127.0.0.1` a permis d'obtenir une clé HMAC et le format de signature `HMAC_SHA1(HILL_KEY, team + '|' + ts)` avec tolérance d'horloge d'environ 45 secondes. Le jeton d'équipe est un secret opérationnel du jeu et n'est pas reproduit dans ce résumé.
