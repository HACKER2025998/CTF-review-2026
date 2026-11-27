# isid0r3--linkcard

- **Catégorie :** web
- **Auteur :** isid0r3
- **Points :** —

## Énoncé

Le service Flask `https://fi4agjy6hdth5oom.t.ctf.tg/` propose inscription/connexion avec CAPTCHA de calcul, un fil de liens et un fetch de titre HTML des liens partagés. Les essais SSRF ont testé les variantes loopback `http://127.1/` et `http://2130706433/` (notation décimale complète). Les variantes ont franchi certaines protections d'URL et déclenché des requêtes vers les services internes. Le port 80 présentait LinkCard ; le port 5000 une application Flask de connexion.
