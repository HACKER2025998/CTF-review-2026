### 19. Curfew — sessions et CAPTCHA — `curfew`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `Pasted text(20261107-180138).txt`, `Pasted text(20261107-180627).txt`.

#### Énoncé, contexte et périmètre

L'application présente `Curfew — La sonnerie qui ferme les sessions`, avec `/login` et `/register`. L'exploration a visé les sessions Flask, la page de connexion, les espaces admin et le CAPTCHA. Un cookie de session décodé révélait `{'captcha_answer':9}`. Ceci montre que des données de l'état client peuvent être visibles sans connaître la clé cryptographique de signature. Les tentatives sur `/admin`, `/api/admin`, `/flag` et diverses routes ne livraient pas de flag.

#### Reconnaissance, commandes et résultats observés

Une nouvelle instance a ensuite rencontré des erreurs DNS/connexion, conservées dans le journal `Pasted text(20261107-180627).txt`. Aucun succès sur les droits de session n'a été démontré.

#### Procédure de reproduction ou reprise technique

```python
# Analyser la première partie d'un cookie signé Flask sans modifier sa signature.
import base64
part='eyJjYXB0Y2hhX2Fuc3dlciI6OX0'
print(base64.urlsafe_b64decode(part+'==='))
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Un cookie lisible n'est pas automatiquement un cookie forgeable.
