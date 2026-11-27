### 16. LinkCard — URL preview et SSRF partiel — `isid0r3--linkcard`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `https://fi4agjy6hdth5oom.t.ctf.tg/`

**Fichiers d’origine associés :** aucun fichier local directement relié, données tirées des échanges précédents.

#### Énoncé, contexte et périmètre

Le service Flask `https://fi4agjy6hdth5oom.t.ctf.tg/` propose inscription/connexion avec CAPTCHA de calcul, un fil de liens et un fetch de titre HTML des liens partagés. Les essais SSRF ont testé les variantes loopback `http://127.1/` et `http://2130706433/` (notation décimale complète). Les variantes ont franchi certaines protections d'URL et déclenché des requêtes vers les services internes. Le port 80 présentait LinkCard ; le port 5000 une application Flask de connexion.

#### Reconnaissance, commandes et résultats observés

L'extracteur d'aperçu renvoyait surtout la balise `<title>`, et les chemins supposés secrets testés ne révélaient rien. Aucun `NCTF{...}` n'a été obtenu. Il reste une différence entre prouver que le serveur a effectué un fetch et prouver qu'une ressource interne confidentielle est exposable par cette extraction limitée.

#### Procédure de reproduction ou reprise technique

```text
SSRF : 127.1 -> 127.0.0.1
SSRF : 2130706433 -> 127.0.0.1
Aucune réponse de titre contenant le flag n'a été observée.
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Une SSRF qui n'expose que les titres HTML peut masquer le contenu du corps et rendre certaines cibles inexfiltrables.
