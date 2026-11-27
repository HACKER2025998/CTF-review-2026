### 15. Bridged Deser — /fetch et RPC interne — `bridged-deser`

**Statut :** NON RÉSOLU · **Points :** 500 · **Instance :** `https://nblujwmm67lhgepc.t.ctf.tg/`

**Fichiers d’origine associés :** aucun fichier local directement relié, données tirées des échanges précédents.

#### Énoncé, contexte et périmètre

L'instance `https://nblujwmm67lhgepc.t.ctf.tg/` expose `GET /fetch?url=<path>&body=<json>` et annonce que le RPC interne n'est pas directement joignable. `GET /fetch?url=/status` renvoie `{'status':'ok'}` ; une requête avec `url=/internal/rpc` et `body={"value":"TEST"}` renvoie `{'result':'record: TEST'}`. Les variantes avec `file:///internal/rpc` ou `http://example.com/internal/rpc` semblaient utiliser le seul chemin de l'URL, suggérant une forme de routage par pathname.

#### Reconnaissance, commandes et résultats observés

Plusieurs centaines de variations JSON, de désérialisation supposée, d'encodages et de champs `op` / `action` ont été essayées sans retour contenant un flag. Aucun effet dangereux n'est démontré par `record: TEST` : c'est seulement le comportement de l'API observé. Nous avons changé de challenge.

#### Procédure de reproduction ou reprise technique

```bash
curl -Gs 'https://<instance>/fetch' --data-urlencode 'url=/status'
curl -Gs 'https://<instance>/fetch' --data-urlencode 'url=/internal/rpc' --data-urlencode 'body={"value":"TEST"}'
```
Prochaine reprise : source du routeur, format de sérialisation réellement utilisé, preuve d'une différence de comportement.

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Ne pas déclarer un RCE pickle juste parce que le nom du challenge contient « deser ».
