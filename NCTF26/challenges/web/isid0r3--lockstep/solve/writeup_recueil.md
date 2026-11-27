### 20. Lockstep — login /dashboard /preview — `lockstep`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `Pasted text(20261107-181830).txt`.

#### Énoncé, contexte et périmètre

L'application `Lockstep — Workspace tools` offrait une page `/login`, une redirection après authentification `302 /dashboard`, une route `/preview` et un `/admin` inaccessible (403). Le script de reconnaissance `lockstep.py` a vérifié `/auth/login`, `/api/preview`, `/admin/dashboard`, `/flag` et plusieurs entrées de preview dirigées vers `http://127.0.0.1` ou `http://localhost` sur divers ports. `/api/preview` était absent (404), et beaucoup de réponses 200 correspondaient simplement à la page de présentation du formulaire Preview.

#### Reconnaissance, commandes et résultats observés

Le journal ne contient ni preuve d'un véritable fetch interne distinctif ni flag. Les requêtes loopback testées sur un formulaire ne prouvent pas en elles-mêmes une SSRF quand la réponse reste celle de l'interface.

#### Procédure de reproduction ou reprise technique

```bash
# Ces exemples ont servi à cartographier, pas à prouver le succès :
GET /login
GET /dashboard
GET /preview
GET /admin     # 403
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

L'élément-clé est de différencier la page de formulaire de la réponse distante effectivement récupérée.
