# cms-smuggle

- **Catégorie :** web
- **Auteur :** inconnu (à compléter)
- **Points :** 500

## Énoncé

**Énoncé communiqué :** « NovaCMS expose une console d'ingestion : tu lui soumets un corps de requête brut, un cache garde en mémoire les pages déjà rendues, et une zone d'administration répond fièrement 403 aux visiteurs ordinaires. Regarde comment ce qui entre par l'ingestion finit par ressortir du cache. » Catégorie Web medium, 500 points, instance éphémère `https://a4x4sp4q4x3rup7w.t.ctf.tg/`. Le HTML du front présente une zone de texte pré-remplie avec `POST /ingest` puis `content=bonjour tout le monde`, un bouton d'envoi à `/ingest` et un lecteur `GET /page?p=<chemin>`. La route protégée est `/admin/flag`.
