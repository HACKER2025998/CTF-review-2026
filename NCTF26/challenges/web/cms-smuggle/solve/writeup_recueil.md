### 14. NovaCMS — ingestion, cache et admin 403 — `cms-smuggle`

**Statut :** NON RÉSOLU · **Points :** 500 · **Instance :** `https://a4x4sp4q4x3rup7w.t.ctf.tg/`

**Fichiers d’origine associés :** `Pasted text(20261107-230220).txt`.

#### Énoncé, contexte et périmètre

**Énoncé communiqué :** « NovaCMS expose une console d'ingestion : tu lui soumets un corps de requête brut, un cache garde en mémoire les pages déjà rendues, et une zone d'administration répond fièrement 403 aux visiteurs ordinaires. Regarde comment ce qui entre par l'ingestion finit par ressortir du cache. » Catégorie Web medium, 500 points, instance éphémère `https://a4x4sp4q4x3rup7w.t.ctf.tg/`. Le HTML du front présente une zone de texte pré-remplie avec `POST /ingest` puis `content=bonjour tout le monde`, un bouton d'envoi à `/ingest` et un lecteur `GET /page?p=<chemin>`. La route protégée est `/admin/flag`.

#### Reconnaissance, commandes et résultats observés

**Faits directs :** `GET /admin/flag` renvoie `403 {"error":"admin only"}` ; `GET /page?p=/admin/flag` renvoie `200 {"cached":null,"path":"/admin/flag"}`. Tous les corps envoyés à `/ingest`, y compris le corps vide, produisent `200 {"cache_poisoned":[],"ingested":true}`. Les essais furent nombreux : 80 variantes de LF/CRLF/NUL/JSON (`nova_parser.py`), ~20 variantes de `Content-Length` (`nova_boundary.py`), 95 variantes de séparateurs (`nova_new_angle.py`), chemins encodés `%2f`, segments `..`, réécritures de routes et lots HTTP complets. Aucun cache public ou admin n'a changé. Quelques erreurs de connexion sont également apparues. Nginx 1.27.5 a servi HTTP/2 ; `OPTIONS /ingest` annonce POST/OPTIONS ; `/swagger.json` et `/openapi.json` donnent 404.

#### Procédure de reproduction ou reprise technique

```bash
BASE='https://a4x4sp4q4x3rup7w.t.ctf.tg'
curl -ksSi "$BASE/admin/flag"
curl -ksS "$BASE/page?p=/admin/flag"
curl -ksS -X POST "$BASE/ingest" -H 'Content-Type: text/plain' --data-binary $'POST /ingest
content=bonjour'
# Attendu : pas de cache modifié, sauf exploit nouveau et vérifié.
```
La méthode de reprise serait d'identifier la grammaire réelle du parseur, de créer d'abord un cache public témoin, puis d'étudier les confusions d'interprétation du cache. Ne pas promettre un flag par simple variation de Content-Length.

#### Résultat / flag

**Aucun ; cache_poisoned reste []**

#### Pièges, interprétation et enseignement

L'affirmation `ingested:true` n'atteste pas qu'une page soit mise en cache. Un 200 HTTP ne prouve pas une attaque réussie.
