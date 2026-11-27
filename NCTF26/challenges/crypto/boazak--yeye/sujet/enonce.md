# boazak--yeye

- **Catégorie :** crypto
- **Auteur :** boazak
- **Points :** —

## Énoncé

MAC maison SHA256(secret || data). Forger un paiement user=admin sans connaître le secret. Endpoints: GET /challenge (donne msg + mac), GET /pay?msg=&mac=.
/challenge : msg="amount=1000&user=guest", mac=sha256(secret||msg).
