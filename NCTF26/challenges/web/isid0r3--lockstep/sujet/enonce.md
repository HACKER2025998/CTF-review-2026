# isid0r3--lockstep

- **Catégorie :** web
- **Auteur :** isid0r3
- **Points :** —

## Énoncé

L'application `Lockstep — Workspace tools` offrait une page `/login`, une redirection après authentification `302 /dashboard`, une route `/preview` et un `/admin` inaccessible (403). Le script de reconnaissance `lockstep.py` a vérifié `/auth/login`, `/api/preview`, `/admin/dashboard`, `/flag` et plusieurs entrées de preview dirigées vers `http://127.0.0.1` ou `http://localhost` sur divers ports. `/api/preview` était absent (404), et beaucoup de réponses 200 correspondaient simplement à la page de présentation du formulaire Preview.
