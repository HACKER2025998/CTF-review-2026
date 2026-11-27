# foodctf

- **Catégorie :** ?
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

La reconnaissance du service FoodCTF sur `10.113.159.109` a trouvé `GET /backdoor/shell/backdoor.js`. Ce JavaScript mentionnait `//TODO Get the error output of commands - plague` et comportait une fonction `postData()` réalisant un fetch en POST. Le test direct vers `/api/cmd` avec un corps brut `id` a renvoyé `HTTP/1.1 401 Unauthorized` et `Unauthenticated`. L'API existe donc, mais l'exécution de commande n'est pas démontrée.
