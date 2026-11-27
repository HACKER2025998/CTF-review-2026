### 22. FoodCTF — JS backdoor.js et API /api/cmd — `foodctf`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** aucun fichier local directement relié, données tirées des échanges précédents.

#### Énoncé, contexte et périmètre

La reconnaissance du service FoodCTF sur `10.113.159.109` a trouvé `GET /backdoor/shell/backdoor.js`. Ce JavaScript mentionnait `//TODO Get the error output of commands - plague` et comportait une fonction `postData()` réalisant un fetch en POST. Le test direct vers `/api/cmd` avec un corps brut `id` a renvoyé `HTTP/1.1 401 Unauthorized` et `Unauthenticated`. L'API existe donc, mais l'exécution de commande n'est pas démontrée.

#### Reconnaissance, commandes et résultats observés

La prochaine étape aurait été d'examiner le contrôle d'authentification de l'environnement de compétition autorisé, au lieu d'inférer une RCE du seul nom `backdoor.js`. Aucun flag capturé.

#### Procédure de reproduction ou reprise technique

```bash
curl -s http://10.113.159.109/backdoor/shell/backdoor.js
curl -i -X POST http://10.113.159.109/api/cmd -H 'Content-Type: text/plain' --data-binary 'id'
# HTTP 401 : Unauthenticated
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Le service doit rester isolé au périmètre du jeu ; ne pas extrapoler à une cible tierce.
