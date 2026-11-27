# bridged-deser

- **Catégorie :** web
- **Auteur :** hibris, Clawd
- **Points :** 500

## Énoncé

L'instance `https://nblujwmm67lhgepc.t.ctf.tg/` expose `GET /fetch?url=<path>&body=<json>` et annonce que le RPC interne n'est pas directement joignable. `GET /fetch?url=/status` renvoie `{'status':'ok'}` ; une requête avec `url=/internal/rpc` et `body={"value":"TEST"}` renvoie `{'result':'record: TEST'}`. Les variantes avec `file:///internal/rpc` ou `http://example.com/internal/rpc` semblaient utiliser le seul chemin de l'URL, suggérant une forme de routage par pathname.
