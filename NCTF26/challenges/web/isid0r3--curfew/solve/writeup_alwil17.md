# Curfew — JWT non vérifié, SQLi dans le jti, puis LFI

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/curfew/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Le JWT de Curfew n'est pas vérifié : je peux le re-signer avec
> n'importe quelle clé. Mais changer `role` ne sert à rien — c'est le `jti` qui
> est injecté tel quel dans une requête SQL. Un `jti` du type `' OR 1=1-- -` me
> ramène la session admin. Ensuite, l'export de logs admin a un `?file=` vulnérable
> à une LFI, et je lis le flag. **Flag :** `NCTF{…}`.

## 1. Analyse du JWT

Après inscription, le cookie `curfew_session` contient un JWT HS256. Payload :
`sub` (user_id), `jti` (identifiant de session), `iat`.

Je modifie le payload, je re-signe avec une clé bidon — **le serveur l'accepte**.
La signature n'est pas vérifiée.

## 2. Fausse piste : le rôle

Réflexe : ajouter `"role": "admin"`. Ça ne marche pas. Le rôle n'est **pas** lu
depuis le JWT. Seul le `jti` sert à retrouver la session en base, et c'est la
jointure avec la table `users` qui décide du rôle.

## 3. SQLi via le jti

Le `jti` est concaténé directement dans la requête SQL sans échappement. Je forge
un JWT dont le `jti` vaut :

```
' OR 1=1-- -
```

La clause `WHERE` devient toujours vraie. La requête renvoie la première session
active triée par ID — la session de l'**admin**, créée au démarrage et jamais
révoquée. Je remplace le cookie (signé avec n'importe quelle clé) et `/admin`
s'ouvre.

## 4. LFI dans l'export de logs

Le panel admin propose un export : `/admin/logs/export?file=platform.log`. Le
paramètre `file` est collé à un répertoire de logs sans contrôle. Un chemin absolu
écrase le préfixe :

```
/admin/logs/export?file=/flag.txt
```

Le traversal classique `../../../../flag.txt` marche aussi.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- **Vérifier la signature des JWT**, systématiquement, et ne jamais réutiliser une
  valeur de token dans une requête sans la paramétrer.
- **Requêtes préparées** pour le `jti` ; **canonicaliser et confiner** tout chemin
  de fichier (pas de chemin absolu, pas de `..`, racine verrouillée).
