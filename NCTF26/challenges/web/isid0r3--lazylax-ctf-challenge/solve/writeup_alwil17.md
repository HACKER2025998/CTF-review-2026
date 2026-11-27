# Lazylax — énumérer CouchDB à travers un proxy en lecture seule

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/lazylax/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Lazylax expose un proxy HTTP en lecture vers une base CouchDB
> interne sous `/api/`. `_all_dbs` liste les bases, et la base système `_users` —
> qui ne devrait jamais être exposée — contient un document dont le profil porte le
> flag. **Flag :** `NCTF{…}`.

## 1. Le proxy API

Les images du journal se chargent depuis `/api/media/<id>`, et la nav montre un
lien « ARCHIVE API ». Le préfixe `/api/` est un proxy direct vers CouchDB.

## 2. Lister les bases

```
/api/_all_dbs
```

Me renvoie les bases disponibles, dont `articles` et `_users`.

## 3. La base articles (fausse piste)

```
/api/articles/_all_docs
```

Articles, brouillons, métadonnées — rien pour le flag.

## 4. La base système _users

`_users` est la base système CouchDB des comptes. J'énumère :

```
/api/_users/_all_docs
```

Plusieurs utilisateurs : `mira`, `jonah`, `eli`, `nora`, `archivist`,
`newsletter`, `archive-verification`…

Je lis chaque document (via `?include_docs=true`, ou directement) :

```
/api/_users/org.couchdb.user:archive-verification
```

Le document de `archive-verification` porte un champ `internal_note` dans son
profil — le flag.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- Certains endpoints d'admin (`_config`, `_node`) sont bloqués par le proxy, mais
  les **bases en lecture restent accessibles**, `_users` comprise. Un proxy
  « lecture seule » n'est pas un contrôle d'accès.
- **Ne jamais exposer CouchDB** (même proxifié) sans allow-list des bases et des
  chemins ; `_users` ne doit jamais être lisible, et aucun secret ne doit vivre
  dans un profil utilisateur.
