# LinkCard — SSRF via l'aperçu de liens

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/linkcard/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — LinkCard récupère côté serveur toute URL postée pour en faire un
> aperçu : SSRF. Le filtre anti-locale repose sur `ipaddress` et ne voit que les
> IP en notation stricte ; je passe en décimal (`2130706433`) pour atteindre le
> loopback. Le statut de l'aperçu me sert d'oracle de ports, je trouve un dashboard
> admin interne sur `:8081`, et son titre contient le flag. **Flag :** `NCTF{…}`.

## 1. La fonctionnalité

Dans le feed, un message qui contient une URL déclenche une visite serveur pour
extraire titre + image Open Graph. Le statut est affiché : « ok », « bloqué »,
« injoignable », « timeout »… Comportement typique de SSRF.

## 2. Le filtre

`http://127.0.0.1` ou `http://localhost` → « Hôte non autorisé ». Les adresses
locales et privées sont bloquées.

## 3. Contourner

Le filtre utilise `ipaddress` qui ne reconnaît que la notation décimale pointée
stricte. Les encodages IPv4 hérités passent le filtre mais sont résolus
normalement :

- **Décimal** : `http://2130706433` (= 127.0.0.1)
- **Octal** : `http://0177.0.0.1`
- **Hexa** : `http://0x7f000001`
- **Forme courte** : `http://127.1`

## 4. Scanner les ports via l'oracle

Le statut renseigne sur l'état des ports :

- « injoignable » = port fermé ;
- « timeout » = filtré / sans réponse ;
- « http_XXX » = port ouvert, réponse HTTP reçue.

Je balaie les ports classiques sur l'adresse de contournement :

- **80** — vitrine « LinkCard » (leurre) ;
- **8081** — un dashboard admin interne.

## 5. Lire le flag

Je poste `http://2130706433:8081/admin` : le serveur fait la requête et extrait le
titre de la page. Le flag est dans le titre du dashboard, et apparaît dans
l'aperçu.

## 6. Flag

```text
NCTF{…}
```

## 7. Leçons & remédiation

- **Normaliser l'adresse avant de filtrer**, puis re-vérifier l'IP **résolue**
  juste avant la connexion (anti-rebind), et refuser tout ce qui n'est pas public.
- Un **oracle de statut** (ouvert/fermé/timeout) suffit à cartographier le réseau
  interne : renvoyer un message d'erreur uniforme.
