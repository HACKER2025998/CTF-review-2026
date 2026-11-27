# sentinelbot

- **Catégorie :** ?
- **Auteur :** inconnu (à compléter)
- **Points :** 50

## Énoncé

Énoncé : « SentinelBot is an offline support assistant shipped as a single Python module, `oracle.py`, exposing `respond(prompt)`. It guards a hidden diagnostic token and politely refuses when you ask about it directly. Everything runs locally — no network, no real model. Call the shipped oracle from your own script and make it hand over the token. » Défi AI de 50 points. Selon notre discussion, `_S` stocke une chaîne `base64(reverse(flag))` ; la fonction `_secret()` procède à `base64.b64decode(_S)[::-1]`.
