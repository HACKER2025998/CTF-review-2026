# isid0r3--curfew

- **Catégorie :** web
- **Auteur :** isid0r3
- **Points :** —

## Énoncé

L'application présente `Curfew — La sonnerie qui ferme les sessions`, avec `/login` et `/register`. L'exploration a visé les sessions Flask, la page de connexion, les espaces admin et le CAPTCHA. Un cookie de session décodé révélait `{'captcha_answer':9}`. Ceci montre que des données de l'état client peuvent être visibles sans connaître la clé cryptographique de signature. Les tentatives sur `/admin`, `/api/admin`, `/flag` et diverses routes ne livraient pas de flag.
