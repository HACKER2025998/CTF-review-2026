# php-unserialize

- **Catégorie :** web
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Le fichier source `index.php` est un handout : le cookie est `base64(serialize($obj))` et l'application envoie la donnée vers `unserialize()`. La classe de session de l'exemple possède `uid` et `role`. Une classe `FlagReveal` déclenche dans `__wakeup()` une décryption liée à un seed de maintenance `rot-2026-maintenance`. Le cookie invité `session_cookie.b64` est fourni comme base de travail.
