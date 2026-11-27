# Marché de Lomé — IDOR en chaîne vers une note confidentielle

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/marche-lome/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Une place de marché dont l'API ne contrôle pas la propriété des
> ressources. Depuis un compte commerçant, un IDOR sur `/api/carnet/{uuid}/extrait`
> me donne une `ref_juridique` et une `cle_agent`, que je rejoue sur
> `/api/service-juridique/{ref}` avec l'en-tête `X-Cle-Agent` pour lire la note
> confidentielle. **Flag :** `NCTF{…}`.

## 1. Reconnaissance

Les annonces et un PDF destiné aux agents révèlent la convention d'API : en-têtes
`Accept: text/csv` et `X-Locale: fr-TG` attendus. Je crée un **compte commerçant**
standard.

## 2. Premier IDOR

`GET /api/carnet/{uuid}/extrait` ne vérifie pas que le `uuid` m'appartient. En
énumérant les identifiants, je récupère les extraits d'autres carnets, dont une
`ref_juridique` et une `cle_agent`.

## 3. Rejouer vers le service juridique

Ces deux valeurs débloquent un second endpoint :

```http
GET /api/service-juridique/{ref_juridique}
X-Cle-Agent: {cle_agent}
Accept: text/csv
X-Locale: fr-TG
```

La réponse est la **note confidentielle** — le flag.

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons & remédiation

- **Contrôle d'accès par ressource**, pas seulement par authentification : chaque
  `uuid`/`ref` doit être vérifié contre le propriétaire de la session.
- Une `cle_agent` exposée par un premier IDOR sert de clé au suivant : les fuites
  se chaînent. Ne jamais renvoyer de secret d'autorisation dans un extrait de
  données.
